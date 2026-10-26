# Harvest2Market AI 🌾

A beginner-friendly, end-to-end full-stack web application for farmers — built as a college project demonstration.

> **⚠️ Data notice:** Crop listings in `backend/data/sample_prices.csv` are **illustrative sample data**, not live mandi prices. The linear regression price estimate is an educational demonstration trained on this small dataset. Always check your local market before making a sale.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Market Prices** | Browse sample crop prices across multiple markets |
| **Price Prediction** | Get an educational price estimate using a Linear Regression ML model |
| **Profit Calculator** | Enter quantity, selling price, and expenses to calculate profit or loss in ₹ |
| **Market Comparison** | Compare the same crop across markets; highest price highlighted |
| **User Accounts** | Register, log in, and manage your farm profile |
| **Admin Dashboard** | View all registered users (admin role required) |

---

## 🏗️ Project Structure

```
Harvest2Market AI/
├── backend/
│   ├── data/
│   │   └── sample_prices.csv     # Sample crop price dataset (4 crops × 3 markets)
│   ├── models/
│   │   └── price_model.joblib    # Trained Linear Regression model
│   ├── main.py                   # FastAPI routes, startup, authentication
│   ├── database.py               # SQLite engine and session setup (SQLAlchemy)
│   ├── models.py                 # SQLAlchemy ORM models (User, MarketPrice)
│   ├── Schemas.py                # Pydantic request/response schemas
│   ├── train_model.py            # Script to train and save the ML model
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment variable template
│   └── .env                     # Your local config (do not commit)
├── frontend/
│   ├── src/
│   │   ├── pages/               # Individual page components
│   │   │   ├── Home.jsx         # Landing page
│   │   │   ├── Login.jsx        # Login page
│   │   │   ├── Register.jsx     # Registration page
│   │   │   ├── Auth.jsx         # Shared login/register form logic
│   │   │   ├── Dashboard.jsx    # Overview dashboard
│   │   │   ├── MarketPrices.jsx # Price listing table
│   │   │   ├── PricePrediction.jsx  # ML estimate form
│   │   │   ├── ProfitCalculator.jsx # Profit/loss calculator
│   │   │   ├── MarketComparison.jsx # Side-by-side market chart
│   │   │   ├── Profile.jsx      # User profile editor
│   │   │   └── AdminDashboard.jsx   # Admin user list
│   │   ├── components/
│   │   │   ├── Navbar.jsx       # Top navigation bar
│   │   │   ├── Sidebar.jsx      # Left sidebar navigation
│   │   │   ├── PriceChart.jsx   # Area chart for price trend
│   │   │   └── StatCard.jsx     # Metric summary card
│   │   ├── screens.jsx          # All page screen implementations
│   │   ├── app.jsx              # Router, authentication context, shell layout
│   │   ├── api.js               # Axios API client (single base URL)
│   │   ├── main.jsx             # React entry point
│   │   └── style.css            # All styles (Forest Green & Cream theme)
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── .gitignore
└── README.md
```

---

## 🛠️ Technology Stack

**Frontend**
- React 18 + Vite 6
- React Router DOM 7
- Recharts (area chart, bar chart)
- Lucide React (icons)
- Axios (HTTP client)
- Vanilla CSS (Forest Green + Cream theme, responsive design)

**Backend**
- Python 3.10+
- FastAPI 0.115
- Uvicorn (ASGI server)
- SQLAlchemy 2 ORM + SQLite
- Pydantic v2 (validation)
- pwdlib + argon2 (password hashing)
- PyJWT (JSON Web Tokens)

**Machine Learning**
- pandas + NumPy
- scikit-learn (Pipeline, OneHotEncoder, LinearRegression)
- joblib (model serialisation)

---

## 🚀 Running on Windows (PowerShell)

> You need **Python 3.10+** and **Node.js 20+** installed.  
> Open **two separate PowerShell windows** from the project root.

---

### Window 1 — Backend (FastAPI)

```powershell
# Navigate into the backend folder
cd "Harvest2Market AI\backend"

# (First time only) Allow scripts in this session if PowerShell blocks activation
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# (First time only) Create a Python virtual environment
py -3 -m venv .venv

# Activate the environment
.\.venv\Scripts\Activate.ps1

# (First time only) Install Python packages
pip install -r requirements.txt

# (First time only) Train the ML model — saves models/price_model.joblib
python train_model.py

# Start the API server
uvicorn main:app --reload
```

The API will be available at **http://localhost:8000**.  
SQLite database is created and seeded automatically on first startup.  
Interactive API docs: **http://localhost:8000/docs**

---

### Window 2 — Frontend (React + Vite)

```powershell
# Navigate into the frontend folder
cd "Harvest2Market AI\frontend"

# (First time only) Install Node packages
npm install

# Start the development server
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 🔗 API Endpoints

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/api/health` | Public | Check server is running |
| `POST` | `/api/register` | Public | Create a farmer account |
| `POST` | `/api/login` | Public | Verify credentials, get JWT token |
| `GET` | `/api/market-prices` | Public | List all sample price rows |
| `POST` | `/api/predict` | Public | Get educational price estimate |
| `POST` | `/api/profit-calculator` | 🔐 Signed in | Calculate revenue and profit/loss |
| `GET` | `/api/profile/{user_id}` | 🔐 Self / Admin | Read profile |
| `PUT` | `/api/profile/{user_id}` | 🔐 Self | Update profile |
| `GET` | `/api/admin/users` | 🔐 Admin only | List all user accounts |

**Testing in Swagger UI (http://localhost:8000/docs):**
1. Call `POST /api/register` or `POST /api/login`
2. Copy the `access_token` from the response
3. Click **Authorize** (top right), paste the token, click **Authorize**
4. Protected endpoints will now work

---

## 🔒 Security Notes

- Passwords are **hashed with Argon2** via pwdlib — never stored as plain text
- Authentication uses **signed JWT tokens** (short-lived, default 60 min)
- Admin access is **enforced on the backend** — changing the browser state has no effect
- The `SECRET_KEY` in `.env.example` is for **local development only**; change it before any deployment

---

## 👨‍💼 Making an Admin Account

Registration always creates a `farmer` account. To make an account an admin for your local demo:

1. Stop the FastAPI server
2. Open the database with any SQLite browser (e.g. [DB Browser for SQLite](https://sqlitebrowser.org/)):
   ```
   backend/harvest2market.db
   ```
3. In the `users` table, change the `role` field of your account from `farmer` to `admin`
4. Restart the server

Or use Python from the backend folder:
```powershell
.\.venv\Scripts\python.exe -c "
from database import SessionLocal
from models import User
db = SessionLocal()
u = db.query(User).filter(User.email == 'your@email.com').first()
u.role = 'admin'
db.commit()
print('Done')
db.close()
"
```

---

## 🤖 How the ML Model Works

1. `backend/data/sample_prices.csv` contains 49 rows: 4 crops × 3 markets × 4 months
2. `train_model.py` creates a **scikit-learn Pipeline**:
   - `OneHotEncoder` converts crop name and market to numbers
   - `LinearRegression` learns the price trend from the day number
3. The trained model is saved to `backend/models/price_model.joblib`
4. The FastAPI `/api/predict` endpoint loads it and returns a prediction

> ⚠️ This is an **educational demonstration**. The model is trained on 49 rows of sample data. It has not been validated for real-world price forecasting accuracy.

**To retrain the model** (e.g. after editing the CSV):
```powershell
python train_model.py
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| **Frontend can't connect** | Make sure `uvicorn main:app --reload` is running in the backend folder |
| **CORS error in browser** | Verify `FRONTEND_ORIGINS` in `backend/.env` includes `http://localhost:5173` |
| **Prediction returns 503** | Run `python train_model.py` in the backend folder |
| **`Activate.ps1` is blocked** | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first |
| **`py -3` not found** | Try `python -m venv .venv` if `python` points to Python 3.10+ |
| **Port 5173 in use** | Change port in `vite.config.js` and update `FRONTEND_ORIGINS` accordingly |
| **SQLite schema error** | Stop FastAPI, delete `backend/harvest2market.db`, restart (data will be re-seeded) |

---

## 📊 Sample Dataset

The file `backend/data/sample_prices.csv` has these columns:

| Column | Example |
|---|---|
| `crop_name` | Wheat, Onion, Tomato, Potato |
| `market` | Nashik, Pune, Nagpur |
| `date` | 2025-01-05 |
| `price_per_quintal` | 2450 |

All prices are in **Indian Rupees (₹) per quintal**. Replace this file with licensed real-world data for a production application.

---

## 📝 Project Notes for College Presentation

- **Frontend ↔ Backend**: React sends HTTP requests to FastAPI using Axios. A single `api.js` file holds the base URL so it's easy to change.
- **Authentication flow**: Register → get JWT → store in `localStorage` → attach as `Authorization: Bearer ...` header on every protected request.
- **Database**: SQLAlchemy creates the SQLite file automatically at startup. No separate database server needed.
- **ML integration**: The model is loaded once per API request in `main.py`. In production you would cache it at startup.
- **Separation of concerns**: Backend validates all input with Pydantic. Frontend never trusts itself for security decisions.
