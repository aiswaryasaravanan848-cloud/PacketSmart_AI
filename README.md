# PocketSmart AI

A complete FastAPI + Jinja2 + Gemini application based on the supplied PocketSmart AI project document. It provides:

- User registration, login, JWT authentication, logout, session metadata and session data
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional outfit image analysis
- Gemini-powered recommendations with a deterministic mock-data fallback when no API key is configured or Gemini fails
- Recommendation history and detail pages
- Responsive HTML/CSS/JavaScript UI
- Automated API tests

## Important model note
The supplied document names **Gemini 1.5 Flash Pro**. The current Google Gemini API model catalog has newer models, and this implementation therefore makes the model configurable through `GEMINI_MODEL`. The default is `gemini-2.5-flash`; set `GEMINI_MODEL` to another model available to your API account if needed. Gemini 2.5 Flash supports text and image input. See the current Google documentation before changing the model.

## Project structure

```text
PocketSmart_AI/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── pages.py
│   │   └── planners.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py
│   │   ├── marketplace_service.py
│   │   └── recommendation_service.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   ├── planner.html
│   │   └── detail.html
│   └── static/
│       ├── app.css
│       └── app.js
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## VS Code setup

### 1. Open the project
Open the `PocketSmart_AI` folder in VS Code.

### 2. Create a virtual environment
Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
py -3 -m venv .venv
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment

```bash
copy .env.example .env
```

PowerShell alternative:

```powershell
Copy-Item .env.example .env
```

Put your Gemini API key into `.env`:

```env
GEMINI_API_KEY=your_key_here
```

If you leave it blank, the app still runs using deterministic fallback recommendations. This is useful for testing the complete UI without an AI key.

### 5. Start the app

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Test

With the virtual environment active:

```bash
pytest -q
```

The tests use fallback mode and do not require a Gemini API key.

## API routes

Authentication:

- `POST /register`
- `POST /login`
- `POST /logout`
- `POST /token`
- `GET /session-info`
- `GET /session-data`

Planners:

- `POST /generate-home`
- `POST /generate-party`
- `POST /generate-jewelry`
- `GET /recommendations-details/{recommendation_id}`
- `GET /history`

Page routes include `/`, `/login`, `/register`, `/dashboard`, `/history`, `/planner/home`, `/planner/party`, and `/planner/jewelry`.

## Notes about external marketplaces
The project document calls for Amazon, Flipkart, IKEA, Swiggy, Zomato, OYO and similar sources, but it does not provide production API credentials/contracts. This implementation therefore uses clearly labeled search links and a local mock catalog instead of pretending to have live marketplace inventory. Replace `marketplace_service.py` with approved partner APIs when credentials/contracts are available.
