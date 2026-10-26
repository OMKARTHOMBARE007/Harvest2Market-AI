from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

def clean_text(value: str) -> str:
    value = value.strip()
    if not value: raise ValueError("This field cannot be blank.")
    return value

class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    location: str = Field(default="", max_length=100)
    farm_size_acres: float = Field(default=0, ge=0, le=1_000_000)
    @field_validator("full_name", "email")
    @classmethod
    def strip_required(cls, value): return clean_text(value)
    @field_validator("location")
    @classmethod
    def strip_location(cls, value): return value.strip()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    location: str
    farm_size_acres: float
    role: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ProfileUpdate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    location: str = Field(default="", max_length=100)
    farm_size_acres: float = Field(default=0, ge=0, le=1_000_000)
    @field_validator("full_name")
    @classmethod
    def strip_name(cls, value): return clean_text(value)
    @field_validator("location")
    @classmethod
    def strip_location(cls, value): return value.strip()

class PredictionRequest(BaseModel):
    crop_name: str = Field(min_length=1, max_length=100)
    market: str = Field(min_length=1, max_length=100)
    date: date
    @field_validator("crop_name", "market")
    @classmethod
    def strip_fields(cls, value): return clean_text(value)

class ProfitRequest(BaseModel):
    crop_name: str = Field(min_length=1, max_length=100)
    quantity_quintals: float = Field(gt=0, le=1_000_000)
    selling_price_per_quintal: float = Field(ge=0, le=100_000_000)
    total_expenses: float = Field(ge=0, le=1_000_000_000)
    @field_validator("crop_name")
    @classmethod
    def strip_crop(cls, value): return clean_text(value)
