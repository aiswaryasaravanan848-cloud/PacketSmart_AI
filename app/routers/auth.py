from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db, User, Recommendation
from ..schemas import RegisterRequest, LoginRequest, SessionInfo
from ..security import hash_password, verify_password, create_access_token
from ..dependencies import get_current_user

router=APIRouter()
COOKIE="pocketsmart_token"

@router.post("/register")
def register(payload:RegisterRequest, response:Response, db:Session=Depends(get_db)):
    email=payload.email.lower()
    if db.query(User).filter(User.email==email).first(): raise HTTPException(409,"Email already registered")
    user=User(name=payload.name.strip(),email=email,password_hash=hash_password(payload.password)); db.add(user); db.commit(); db.refresh(user)
    token=create_access_token(user.id); response.set_cookie(COOKIE,token,httponly=True,samesite="lax",max_age=7200)
    return {"message":"Registration successful","access_token":token,"token_type":"bearer","user":{"id":user.id,"name":user.name,"email":user.email}}

@router.post("/login")
def login(payload:LoginRequest, response:Response, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==payload.email.lower()).first()
    if not user or not verify_password(payload.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    token=create_access_token(user.id); response.set_cookie(COOKIE,token,httponly=True,samesite="lax",max_age=7200)
    return {"message":"Login successful","access_token":token,"token_type":"bearer","user":{"id":user.id,"name":user.name,"email":user.email}}

@router.post("/token")
def token(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==form_data.username.lower()).first()
    if not user or not verify_password(form_data.password,user.password_hash): raise HTTPException(401,"Incorrect username or password")
    return {"access_token":create_access_token(user.id),"token_type":"bearer"}

@router.post("/logout")
def logout(response:Response):
    response.delete_cookie(COOKIE); return {"message":"Logged out"}

@router.get("/session-info",response_model=SessionInfo)
def session_info(request:Request, db:Session=Depends(get_db)):
    token=request.cookies.get(COOKIE)
    if not token: return SessionInfo(logged_in=False)
    from ..security import decode_token
    user_id=decode_token(token); user=db.get(User,user_id) if user_id else None
    return SessionInfo(logged_in=bool(user),user_id=user.id if user else None,email=user.email if user else None,name=user.name if user else None)

@router.get("/session-data")
def session_data(user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    return {"user":{"id":user.id,"name":user.name,"email":user.email},"recommendation_count":db.query(Recommendation).filter_by(user_id=user.id).count()}
