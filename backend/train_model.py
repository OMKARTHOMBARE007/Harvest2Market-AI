"""Train and save the educational sample-price model."""
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sample_prices.csv"
MODEL_PATH = BASE_DIR / "models" / "price_model.joblib"
FEATURES = ["crop_name", "market", "day_number"]

def main():
    data = pd.read_csv(DATA_PATH, parse_dates=["date"])
    if data.empty or data["price_per_quintal"].isna().any(): raise ValueError("Sample dataset must contain complete crop-price rows.")
    data["day_number"] = (data["date"] - data["date"].min()).dt.days
    transform = ColumnTransformer([("categories", OneHotEncoder(handle_unknown="ignore"), ["crop_name", "market"]), ("date", "passthrough", ["day_number"])])
    model = Pipeline([("features", transform), ("regression", LinearRegression())])
    model.fit(data[FEATURES], data["price_per_quintal"])
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "start_date": data["date"].min().date().isoformat()}, MODEL_PATH)
    print(f"Trained on {len(data)} demonstration rows. Saved model to {MODEL_PATH}")
if __name__ == "__main__": main()
