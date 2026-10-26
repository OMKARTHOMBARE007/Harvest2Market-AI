"""Harvest2Market API: illustrative sample market data and model estimates."""
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
from typing import Annotated
import joblib
import jwt
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine, get_db
from models import MarketPrice, User
from Schemas import AuthResponse, LoginRequest, PredictionRequest, ProfileUpdate, ProfitRequest, RegisterRequest, UserResponse

MODEL_PATH = BASE_DIR / "models" / "price_model.joblib"
SECRET_KEY = os.getenv("SECRET_KEY", "local-development-only-change-this-secret")
TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))
ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()
bearer = HTTPBearer(auto_error=False)
app = FastAPI(title="Harvest2Market AI API", version="1.0.0", description="Student demonstration API. Market rows and estimates are illustrative.")
origins = [
    x.strip()
    for x in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,https://harvest2-market-ai.vercel.app"
    ).split(",")
    if x.strip()
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST", "PUT"], allow_headers=["Authorization", "Content-Type"])

def seed_prices(db: Session):
    if db.scalar(select(func.count()).select_from(MarketPrice)): return
    frame = pd.read_csv(BASE_DIR / "data" / "sample_prices.csv")
    for row in frame.to_dict(orient="records"):
        db.add(MarketPrice(crop_name=row["crop_name"], market=row["market"], date=date.fromisoformat(row["date"]), price_per_quintal=float(row["price_per_quintal"])))
    db.commit()

@app.on_event("startup")
def initialize_database():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db: seed_prices(db)

def create_token(user: User):
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user.id), "role": user.role, "iat": now, "exp": now + timedelta(minutes=TOKEN_MINUTES)}, SECRET_KEY, algorithm=ALGORITHM)

def current_user(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)], db: Annotated[Session, Depends(get_db)]) -> User:
    unauthorized = HTTPException(status_code=401, detail="Please sign in to continue.", headers={"WWW-Authenticate": "Bearer"})
    if not credentials: raise unauthorized
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub", ""))
    except (jwt.InvalidTokenError, ValueError, TypeError): raise unauthorized
    user = db.get(User, user_id)
    if not user: raise unauthorized
    return user

def admin_user(user: Annotated[User, Depends(current_user)]) -> User:
    if user.role != "admin": raise HTTPException(status_code=403, detail="Administrator access is required.")
    return user

def auth_response(user: User): return AuthResponse(access_token=create_token(user), user=UserResponse.model_validate(user))

@app.get("/api/health")
def health(): return {"status": "ok", "data_mode": "sample demonstration data"}

@app.post("/api/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterRequest, db: Annotated[Session, Depends(get_db)]):
    email = str(payload.email).lower()
    if db.scalar(select(User).where(User.email == email)): raise HTTPException(status_code=409, detail="An account with this email already exists.")
    user = User(full_name=payload.full_name, email=email, hashed_password=password_hash.hash(payload.password), location=payload.location, farm_size_acres=payload.farm_size_acres, role="farmer")
    db.add(user)
    try: db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    db.refresh(user)
    return auth_response(user)

@app.post("/api/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if not user or not password_hash.verify(payload.password, user.hashed_password): raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    return auth_response(user)

@app.get("/api/market-prices")
def market_prices(db: Annotated[Session, Depends(get_db)]):
    rows = db.scalars(select(MarketPrice).order_by(MarketPrice.date, MarketPrice.crop_name, MarketPrice.market)).all()
    return [{"id": p.id, "crop_name": p.crop_name, "market": p.market, "date": p.date.isoformat(), "price_per_quintal": p.price_per_quintal, "is_sample": True} for p in rows]

@app.post("/api/predict")
def predict(payload: PredictionRequest):
    if not MODEL_PATH.exists(): raise HTTPException(status_code=503, detail="The prediction model is not trained yet. Run python train_model.py from the backend folder.")
    try:
        bundle = joblib.load(MODEL_PATH)
        day_number = (payload.date - date.fromisoformat(bundle["start_date"])).days
        estimate = float(bundle["model"].predict(pd.DataFrame([{"crop_name": payload.crop_name, "market": payload.market, "day_number": day_number}]))[0])
    except (OSError, ValueError, KeyError, EOFError) as exc: raise HTTPException(status_code=500, detail="Could not load the prediction model. Retrain it using python train_model.py.") from exc
    return {"crop_name": payload.crop_name, "market": payload.market, "date": payload.date.isoformat(), "predicted_price": round(max(0, estimate), 2), "unit": "INR per quintal", "is_estimate": True, "disclaimer": "Educational estimate based on a small sample dataset. Not a live or guaranteed market price."}

@app.post("/api/profit-calculator")
def profit_calculator(payload: ProfitRequest, _: Annotated[User, Depends(current_user)]):
    revenue = payload.quantity_quintals * payload.selling_price_per_quintal
    profit = revenue - payload.total_expenses
    return {"crop_name": payload.crop_name, "quantity_quintals": payload.quantity_quintals, "selling_price_per_quintal": payload.selling_price_per_quintal, "revenue": round(revenue, 2), "total_expenses": payload.total_expenses, "profit": round(profit, 2), "currency": "INR"}

@app.get("/api/profile/{user_id}", response_model=UserResponse)
def get_profile(user_id: int, requester: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]):
    if requester.id != user_id and requester.role != "admin": raise HTTPException(status_code=403, detail="You can only view your own profile.")
    user = db.get(User, user_id)
    if not user: raise HTTPException(status_code=404, detail="User not found.")
    return user

@app.put("/api/profile/{user_id}", response_model=UserResponse)
def update_profile(user_id: int, payload: ProfileUpdate, requester: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]):
    if requester.id != user_id: raise HTTPException(status_code=403, detail="You can only update your own profile.")
    requester.full_name, requester.location, requester.farm_size_acres = payload.full_name, payload.location, payload.farm_size_acres
    db.commit()
    db.refresh(requester)
    return requester

@app.get("/api/admin/users", response_model=list[UserResponse])
def list_users(_: Annotated[User, Depends(admin_user)], db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(User).order_by(User.id)).all()
