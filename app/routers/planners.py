import json
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db, User, Recommendation
from ..dependencies import get_current_user
from ..schemas import HomeRequest, PartyRequest, JewelryRequest, RecommendationResponse
from ..services.recommendation_service import generate

router=APIRouter()

def save(db,user,planner,payload,result):
    row=Recommendation(user_id=user.id,planner_type=planner,request_json=json.dumps(payload),response_json=json.dumps(result)); db.add(row); db.commit(); db.refresh(row); return row.id
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.post("/generate-home", response_model=RecommendationResponse)
def generate_home(payload:HomeRequest,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    result=generate("home",payload.model_dump()); save(db,user,"home",payload.model_dump(),result); return result

@router.post("/generate-party", response_model=RecommendationResponse)
def generate_party(payload:PartyRequest,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    result=generate("party",payload.model_dump()); save(db,user,"party",payload.model_dump(),result); return result

@router.post("/generate-jewelry", response_model=RecommendationResponse)
async def generate_jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form("Elegant"),outfit_color:str=Form("Not specified"),outfit_description:str=Form(""),outfit_image:UploadFile|None=File(None),user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if budget<=0: raise HTTPException(422,"Budget must be positive")
    image_bytes=None; mime=None
    if outfit_image:
        if outfit_image.content_type not in {"image/jpeg","image/png","image/webp"}: raise HTTPException(415,"Only JPG, PNG or WEBP images are supported")
        image_bytes=await outfit_image.read()
        if len(image_bytes)>5*1024*1024: raise HTTPException(413,"Image must be 5 MB or smaller")
        mime=outfit_image.content_type
    payload={"budget":budget,"occasion":occasion,"style":style,"outfit_color":outfit_color,"outfit_description":outfit_description}
    result=generate("jewelry",payload,image_bytes,mime); save(db,user,"jewelry",payload,result); return result

@router.get("/recommendations-details/{recommendation_id}")
def recommendation_details(recommendation_id:int,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    row=db.query(Recommendation).filter_by(id=recommendation_id,user_id=user.id).first()
    if not row: raise HTTPException(404,"Recommendation not found")
    return {"id":row.id,"planner_type":row.planner_type,"request":json.loads(row.request_json),"response":json.loads(row.response_json),"created_at":row.created_at}

@router.get("/api/history")
def history(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    rows=db.query(Recommendation).filter_by(user_id=user.id).order_by(Recommendation.created_at.desc()).all()
    return [{"id":r.id,"planner_type":r.planner_type,"created_at":r.created_at,"summary":json.loads(r.response_json).get("summary","")} for r in rows]
@router.delete("/history/{recommendation_id}")
def delete_history(
    recommendation_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    row = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id,
        Recommendation.user_id == user.id
    ).first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    db.delete(row)
    db.commit()

    return {"message": "History deleted successfully"}