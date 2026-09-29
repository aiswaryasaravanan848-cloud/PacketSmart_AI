from urllib.parse import quote_plus

CATALOG = {
    "home": [
        {"name":"Minimalist LED Ceiling Light", "category":"Lighting", "platform":"IKEA", "price":1499},
        {"name":"Modern 3-Seater Sofa", "category":"Furniture", "platform":"Amazon", "price":18999},
        {"name":"Compact Study Table", "category":"Furniture", "platform":"Flipkart", "price":4999},
        {"name":"Decorative Wall Mirror", "category":"Decor", "platform":"IKEA", "price":2499},
        {"name":"Indoor Artificial Plant", "category":"Decor", "platform":"Amazon", "price":899},
        {"name":"Smart LED Bulb Pack", "category":"Lighting", "platform":"Amazon", "price":1299},
    ],
    "party": [
        {"name":"Vegetarian Catering Package", "category":"Catering", "platform":"Swiggy", "price":280},
        {"name":"Mixed Catering Package", "category":"Catering", "platform":"Zomato", "price":350},
        {"name":"Birthday Decoration Set", "category":"Decoration", "platform":"Amazon", "price":1999},
        {"name":"Event Hall Search", "category":"Venue", "platform":"OYO", "price":8000},
        {"name":"Party Lighting Bundle", "category":"Decoration", "platform":"Flipkart", "price":2499},
    ],
    "jewelry": [
        {"name":"Gold-Tone Jhumka Earrings", "category":"Earrings", "platform":"Amazon", "price":799},
        {"name":"Minimal Necklace Set", "category":"Necklace", "platform":"Flipkart", "price":1499},
        {"name":"Pearl Drop Earrings", "category":"Earrings", "platform":"Amazon", "price":999},
        {"name":"Temple-Style Pendant Set", "category":"Necklace", "platform":"Flipkart", "price":2499},
        {"name":"Simple Bangles Set", "category":"Bangles", "platform":"Amazon", "price":699},
    ],
}


def marketplace_url(platform: str, query: str) -> str:
    domains = {
        "Amazon": "https://www.amazon.in/s?k=",
        "Flipkart": "https://www.flipkart.com/search?q=",
        "IKEA": "https://www.ikea.com/in/en/search/?q=",
        "Swiggy": "https://www.swiggy.com/search?query=",
        "Zomato": "https://www.zomato.com/search?q=",
        "OYO": "https://www.oyorooms.com/search?location=",
    }
    return domains.get(platform, "https://www.google.com/search?q=") + quote_plus(query)


def get_candidates(planner_type: str) -> list[dict]:
    return [{**x, "url": marketplace_url(x["platform"], x["name"])} for x in CATALOG[planner_type]]
