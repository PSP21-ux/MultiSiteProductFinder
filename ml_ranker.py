import re
from sentence_transformers import SentenceTransformer, util

# Load the embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

ACCESSORY_KEYWORDS = ["case", "cover", "cable", "wire", "screw", "holder", "mount", "bracket", "connector", "clip"]

def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9 ]', '', text.lower().strip())

def normalize_price(price_str):
    try:
        price = float(price_str.replace(',', '').replace('₹', '').replace('$', '').strip())
        return max(1.0 / price, 0.001)
    except:
        return 0.0

def availability_score(status):
    return 1.0 if status.lower() == "yes" else 0.0

def accessory_penalty(product_name, query):
    query_lower = query.lower()
    if any(word in query_lower for word in ACCESSORY_KEYWORDS):
        return 0.0
    name_lower = product_name.lower()
    return 0.3 if any(word in name_lower for word in ACCESSORY_KEYWORDS) else 0.0

def group_by_clean_name(products):
    grouped = {}
    for product in products:
        clean_name = clean_text(product["name"])
        if clean_name not in grouped:
            grouped[clean_name] = []
        grouped[clean_name].append(product)
    return grouped

def rank_scraped_products(products, query, weights):
    if not products:
        return []

    query_embedding = embedder.encode(query, convert_to_tensor=True)

    for p in products:
        name_price_text = f"{p['name']} {p.get('price', '')}"
        p["embedding"] = embedder.encode(name_price_text, convert_to_tensor=True)
        p["semantic_score"] = float(util.cos_sim(query_embedding, p["embedding"])[0])
        p["price_score"] = normalize_price(p.get("price", ""))
        p["availability_score"] = availability_score(p.get("availability", "unknown"))
        penalty = accessory_penalty(p["name"], query)
        p["final_score"] = (
            weights["relevance"] * p["semantic_score"] +
            weights["price"] * p["price_score"] +
            weights["availability"] * p["availability_score"] -
            penalty
        )

    # Grouping similar products to apply price fairness
    grouped = group_by_clean_name(products)
    for group in grouped.values():
        prices = []
        for p in group:
            try:
                price_val = float(re.sub(r'[^\d.]', '', p.get("price", "").replace(",", "")))
                prices.append(price_val)
                p["price_val"] = price_val
            except:
                p["price_val"] = 0.0

        if not prices:
            continue

        avg_price = sum(prices) / len(prices)
        for p in group:
            if p["price_val"] > 1.2 * avg_price:
                p["final_score"] -= 0.2  # Penalty for being too expensive in the same group

    # Flatten groups and preserve near duplicates
    all_products = []
    for group in grouped.values():
        sorted_group = sorted(group, key=lambda x: (x["final_score"], x["availability_score"]), reverse=True)
        all_products.extend(sorted_group)

    sorted_products = sorted(all_products, key=lambda x: x["final_score"], reverse=True)

    # Cleanup extra keys before returning
    for p in sorted_products:
        for key in ["embedding", "semantic_score", "price_score", "availability_score", "final_score", "price_val"]:
            p.pop(key, None)

    return sorted_products
