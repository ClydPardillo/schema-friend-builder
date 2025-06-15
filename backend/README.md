
# MyCause Backend (FastAPI + MySQL)

This backend provides a RESTful API for your web (HTML/Tailwind) frontend and React Native (mobile/middleware) app.  
It handles authentication, entity management (users, donors, charities, campaigns, donations), and secure integration with MySQL.

---

## 🚀 Quick Start

### 1. **Clone the repository**  
```sh
git clone <YOUR_REPO_URL>
cd <YOUR_PROJECT_FOLDER>/backend
```

### 2. **Create Virtual Environment (Recommended)**  
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**  
```sh
pip install -r requirements.txt
```

### 4. **Configure Environment Variables**  
Copy and modify `.env.example` as `.env`:

```sh
cp .env.example .env
```

Edit `.env` and set your **MySQL** credentials, secret key, etc.

### 5. **Database Setup**

- Ensure your MySQL database is running and accessible.
- If you haven't already, create the database specified in the `.env` file.

##### To auto-create tables:
The first request to the API will auto-create tables defined with SQLAlchemy models.  
Alternatively, you can add and execute `Base.metadata.create_all(bind=engine)` in a Python script for one-off migrations.

### 6. **Run the Application**  
```sh
uvicorn app.main:app --reload
```
- The server will run at: [http://localhost:8000](http://localhost:8000)
- Interactive API docs at: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

---

## 📦 Project Structure

```
backend/
  app/
    ├── auth/          # Password hashing, JWT helpers
    ├── models/        # SQLAlchemy ORM models
    ├── routes/        # FastAPI routers (API endpoints)
    ├── schemas/       # Pydantic request/response models
    ├── services/      # Database/session logic
    ├── config.py      # Settings, .env loader
    └── main.py        # FastAPI entrypoint
  requirements.txt
  .env.example
  README.md         # (this file)
  .gitignore
```

---

## 🛡️ Authentication

- Secure login & signup with bcrypt password hashing
- JWT-based access tokens returned on login
- Protected endpoints (see `/users/me`) require valid JWT

---

## 🖥️ API Endpoints

See `/docs` for live documentation and example requests/responses.

**Core modules/routes include:**  
- `/users`    – Signup, login, get profile  
- `/campaigns` – (Sample) List campaigns  
- `/donations` – (Sample) Create donation

Extend with more entities as needed!

---

## 🔄 CORS

CORS is enabled for:
- All local dev frontends (http://localhost + ports)
- Add domains as needed in the `CORS_ORIGINS` variable in your `.env`

---

## ✅ Troubleshooting

- Ensure your database is running and credentials in `.env` are correct
- Install all requirements using the provided requirements.txt
- If you get "table does not exist", double check your DB and run the app to auto-create tables

---

## 📖 Useful Commands

- Run in production:  
  ```sh
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```
- Reinstall all dependencies:  
  ```sh
  pip install -r requirements.txt
  ```

---

## 💬 Questions?

Open an issue in the repo, or refer to [FastAPI](https://fastapi.tiangolo.com/) docs.

