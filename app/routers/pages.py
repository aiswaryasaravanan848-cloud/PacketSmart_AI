from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
router=APIRouter(); templates=Jinja2Templates(directory=str(Path(__file__).resolve().parents[1]/"templates"))

def page(request,name,**ctx): return templates.TemplateResponse(request=request,name=name,context=ctx)
@router.get("/",response_class=HTMLResponse)
def home(request:Request): return page(request,"index.html",title="PocketSmart AI")
@router.get("/login",response_class=HTMLResponse)
def login(request:Request): return page(request,"login.html",title="Login")
@router.get("/register",response_class=HTMLResponse)
def register(request:Request): return page(request,"register.html",title="Register")
@router.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request): return page(request,"dashboard.html",title="Dashboard")
@router.get("/history",response_class=HTMLResponse)
def history(request:Request): return page(request,"history.html",title="History")
@router.get("/planner/{planner}",response_class=HTMLResponse)
def planner(request:Request,planner:str):
    if planner not in {"home","party","jewelry"}: planner="home"
    return page(request,"planner.html",title=f"{planner.title()} Planner",planner=planner)
@router.get("/recommendation/{recommendation_id}",response_class=HTMLResponse)
def detail(request:Request,recommendation_id:int): return page(request,"detail.html",title="Recommendation",recommendation_id=recommendation_id)
