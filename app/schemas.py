from typing import Any, Literal
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    room_type: str = Field(min_length=2, max_length=80)
    style: str = Field(default="Modern", max_length=80)
    quantities: dict[str, int] = Field(default_factory=dict)
    priorities: list[str] = Field(default_factory=list)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guest_count: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="Flexible", max_length=120)
    food_preference: str = Field(default="Mixed", max_length=80)
    city: str = Field(default="", max_length=120)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=80)
    style: str = Field(default="Elegant", max_length=80)
    outfit_color: str = Field(default="Not specified", max_length=80)
    outfit_description: str = Field(default="", max_length=500)

class RecommendationItem(BaseModel):
    name: str
    category: str
    platform: str
    estimated_price: float
    reason: str
    url: str

class RecommendationResponse(BaseModel):
    planner_type: Literal["home", "party", "jewelry"]
    title: str
    summary: str
    budget: float
    allocation: dict[str, float] = Field(default_factory=dict)
    items: list[RecommendationItem]
    tips: list[str] = Field(default_factory=list)
    ai_generated: bool = False
    model: str | None = None
    model_config = ConfigDict(extra="ignore")

class SessionInfo(BaseModel):
    logged_in: bool
    user_id: int | None = None
    email: str | None = None
    name: str | None = None
