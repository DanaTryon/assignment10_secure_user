
## 📘 `README.md`

# 🔐 Secure FastAPI Calculator App

This project is a production-grade FastAPI application featuring secure user authentication, a robust calculator API, and full CI/CD integration. It demonstrates best practices in containerization, testing, and deployment.

---

## 🚀 Features

- ✅ JWT-based user authentication
- ✅ PostgreSQL-backed user model with password hashing
- ✅ Modular FastAPI routes for calculator operations
- ✅ Pydantic schema validation
- ✅ Full test suite: unit, integration, and E2E with Playwright
- ✅ 99% test coverage with `pytest-cov`
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Dockerized for local and cloud deployment

---

## 🧪 Test Coverage

- **Total tests:** 59
- **Coverage:** 99%
- **Test layers:** Unit, integration, E2E
- **Tools:** `pytest`, `pytest-cov`, `Playwright`

To run tests locally:

```bash
pytest --cov=app --cov-report=html
```

Coverage report will be saved to `htmlcov/index.html`.

---

## 🛠️ Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/DanaTryon/assignment10_secure_user.git
cd secure-fastapi-calculator
```

### 2. Start PostgreSQL with Docker

```bash
docker run --name fastapi-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fastapi_db \
  -p 5432:5432 -d postgres
```

### 3. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Set environment variable

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db
```

---

## 🧪 Run Tests

```bash
pytest
```

---

## 🧬 CI/CD Pipeline

This project uses GitHub Actions to automate:

- ✅ Testing on every push and PR
- ✅ Security scanning with Trivy
- ✅ Docker image build and deployment

### CI Environment

- PostgreSQL service runs in GitHub Actions
- `DATABASE_URL` is set to match the test DB
- Playwright is installed for E2E tests

---

## 📦 Deployment

To build and run locally:

```bash
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

Access the app at: `http://localhost:8000`

---
