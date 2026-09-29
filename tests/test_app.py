import os
os.environ["DATABASE_URL"]="sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"]="test-secret"
os.environ["GEMINI_API_KEY"]=""
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='ok'

def test_register_login_and_home():
    email='tester@example.com'
    client.post('/register',json={'name':'Test User','email':email,'password':'secret123'})
    r=client.post('/login',json={'email':email,'password':'secret123'})
    assert r.status_code==200
    r=client.post('/generate-home',json={'budget':30000,'room_type':'Living Room','style':'Modern','quantities':{'lights':2},'priorities':['comfort']})
    assert r.status_code==200
    assert r.json()['planner_type']=='home'

def test_party():
    email='party@example.com'
    client.post('/register',json={'name':'Party User','email':email,'password':'secret123'})
    client.post('/login',json={'email':email,'password':'secret123'})
    r=client.post('/generate-party',json={'budget':20000,'guest_count':20,'event_type':'Birthday','venue':'Flexible','food_preference':'Vegetarian','city':'Salem'})
    assert r.status_code==200

def test_jewelry():
    email='jewel@example.com'
    client.post('/register',json={'name':'Jewel User','email':email,'password':'secret123'})
    client.post('/login',json={'email':email,'password':'secret123'})
    r=client.post('/generate-jewelry',data={'budget':'5000','occasion':'Festival','style':'Traditional','outfit_color':'Maroon','outfit_description':'Traditional saree'})
    assert r.status_code==200
