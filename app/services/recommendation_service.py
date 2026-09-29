import json
from typing import Any
from .gemini_service import GeminiService
from .marketplace_service import get_candidates


def _fallback_home(data: dict[str, Any]) -> dict:
    budget = float(data["budget"])
    candidates = get_candidates("home")
    quantities = data.get("quantities") or {}
    items = []
    for c in candidates[:5]:
        items.append({**c, "estimated_price": c["price"], "reason": f"Fits a {data.get('style','modern')} setup and keeps the plan within a controlled budget."})
    return {
        "planner_type":"home", "title":"Smart Home Interior Plan",
        "summary":f"A {data.get('style','modern')} {data.get('room_type','room')} plan for ₹{budget:,.0f}.",
        "budget":budget, "allocation":{"Furniture":round(budget*.45,2),"Lighting":round(budget*.2,2),"Decor":round(budget*.2,2),"Contingency":round(budget*.15,2)},
        "items":items, "tips":["Measure the room before purchasing large furniture.","Keep a contingency amount for delivery or installation."], "ai_generated":False, "model":None
    }


def _fallback_party(data: dict[str, Any]) -> dict:
    budget = float(data["budget"]); guests=int(data["guest_count"])
    candidates=get_candidates("party")
    items=[]
    for c in candidates:
        price=c["price"] * guests if c["category"]=="Catering" else c["price"]
        items.append({**c,"estimated_price":price,"reason":f"Suitable starting point for {guests} guests and a {data['event_type']} event."})
    return {"planner_type":"party","title":"Smart Party Budget Plan","summary":f"A {data['event_type']} plan for {guests} guests within ₹{budget:,.0f}.","budget":budget,"allocation":{"Catering":round(budget*.5,2),"Venue":round(budget*.2,2),"Decoration":round(budget*.2,2),"Contingency":round(budget*.1,2)},"items":items,"tips":["Confirm per-person catering rates before booking.","Reserve a small contingency for last-minute requirements."],"ai_generated":False,"model":None}


def _fallback_jewelry(data: dict[str, Any]) -> dict:
    budget=float(data["budget"]); candidates=get_candidates("jewelry")
    items=[{**c,"estimated_price":c["price"],"reason":f"Works as a {data['style']} option for {data['occasion']} and can complement {data.get('outfit_color','your outfit')}."} for c in candidates]
    return {"planner_type":"jewelry","title":"Smart Jewelry Plan","summary":f"Jewelry ideas for a {data['occasion']} occasion within ₹{budget:,.0f}.","budget":budget,"allocation":{"Jewelry":round(budget*.8,2),"Contingency":round(budget*.2,2)},"items":items,"tips":["Compare material, size and return policy before buying.","For outfit matching, use the uploaded image as a style reference rather than assuming exact product colors."],"ai_generated":False,"model":None}


def build_prompt(planner_type: str, data: dict, candidates: list[dict]) -> str:
    return f"""You are PocketSmart AI, a budget recommendation assistant. Return ONLY valid JSON with keys: planner_type,title,summary,budget,allocation,items,tips. Each item must have name,category,platform,estimated_price,reason,url. Do not invent live inventory or exact stock. Use only the candidate marketplace records supplied below for item names/platforms/URLs. Keep the total suggested spend at or below the user's budget. Explain uncertainty when prices are estimates.\n\nPlanner: {planner_type}\nUser data: {json.dumps(data, ensure_ascii=False)}\nCandidates: {json.dumps(candidates, ensure_ascii=False)}"""


def generate(planner_type: str, data: dict, image_bytes: bytes | None = None, mime_type: str | None = None) -> dict:
    fallback = {"home":_fallback_home,"party":_fallback_party,"jewelry":_fallback_jewelry}[planner_type](data)
    service=GeminiService()
    result, model=service.generate_json(build_prompt(planner_type,data,get_candidates(planner_type)),image_bytes,mime_type)
    if not result:
        return fallback
    result["planner_type"]=planner_type
    result["budget"]=float(data["budget"])
    result["ai_generated"]=True
    result["model"]=model
    # Normalize URLs and reject malformed AI items by rebuilding from candidates.
    allowed={x["name"]:x for x in get_candidates(planner_type)}
    normalized=[]
    for item in result.get("items",[]):
        if item.get("name") in allowed:
            base=allowed[item["name"]]
            normalized.append({**base,"estimated_price":float(item.get("estimated_price",base["price"])),"reason":str(item.get("reason", "Budget-compatible suggestion."))})
    result["items"]=normalized or fallback["items"]
    result.setdefault("allocation",fallback["allocation"])
    result.setdefault("tips",fallback["tips"])
    result.setdefault("title",fallback["title"]); result.setdefault("summary",fallback["summary"])
    return result
