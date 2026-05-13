# Study Buddy — Complete Setup Guide
**Stack:** Django + React + PostgreSQL + OpenAI + JWT + Deploy on Render/Vercel 
**OS:** Windows 
**Author:** Mohammad Salhab 
**Date:** 2026
---
## Table of Contents
1. [Prerequisites — Install everything](#phase-1--prerequisites)
2. [Git setup + Remote repo](#phase-2--git-setup)
3. [Backend — Django + DRF + JWT](#phase-3--backend)
4. [Database — PostgreSQL](#phase-4--postgresql)
5. [Frontend — React + Axios + Auth](#phase-5--frontend)
6. [Run locally](#phase-6--run-locally)
7. [Connect OpenAI API](#phase-7--openai-api)
8. [Deploy on Render + Vercel](#phase-8--deployment)
9. [Quick reference commands](#quick-reference)
---
## PHASE 1 — Prerequisites
### 1.1 Install Git
- Download: https://git-scm.com/download/win
- During install: choose **"Git from command line and also from 3rd-party software"**
- Verify:
```bash
git --version
```
### 1.2 Install Python 3.11
- Download: https://www.python.org/downloads/
- CHECK "Add Python to PATH" during install
- Verify:
```bash
python --version
pip --version
```
### 1.3 Install Node.js LTS (20.x)
- Download: https://nodejs.org
- Run installer (all defaults)
- Verify:
```bash
node -v
npm -v
```
### 1.4 Install PostgreSQL 16
- Download: https://www.postgresql.org/download/windows/
- During install:
 - Set postgres superuser password (REMEMBER IT)
 - Port: 5432 (default)
 - Keep pgAdmin 4 checked
- Verify:
```bash
psql --version
```
### 1.5 Install VS Code
- Download: https://code.visualstudio.com
- Install these extensions:
 - Python (Microsoft)
 - ES7+ React/Redux snippets
 - Prettier
 - GitLens (optional)
### 1.6 Verify all tools
```bash
git --version
python --version
pip --version
node -v
npm -v
psql --version
```
---
## PHASE 2 — Git Setup
### 2.1 Create project folder
```bash
cd C:\Users\<YourName>\Desktop
mkdir study-buddy
cd study-buddy
code .
```
### 2.2 Initialize Git
```bash
git init
git branch -M main
```
### 2.3 Create .gitignore
Create file: `study-buddy/.gitignore`
```
# Python
__pycache__/
*.pyc
*.pyo
.env
.venv/
venv/
*.egg-info/
# Django
db.sqlite3
staticfiles/
media/
# Node / React
node_modules/
dist/
build/
.env.local
# VS Code
.vscode/
# OS
.DS_Store
Thumbs.db
```
### 2.4 Create README
```bash
echo # Study Buddy > README.md
```
### 2.5 First commit
```bash
git add .
git commit -m "chore: init project"
```
### 2.6 Create GitHub remote repo
1. Go to github.com → New repository
2. Name: `study-buddy`
3. Do NOT add README/gitignore (already have them)
4. Copy the HTTPS URL
```bash
git remote add origin https://github.com/<YOUR_USERNAME>/study-buddy.git
git push -u origin main
```
---
## PHASE 3 — Backend (Django + DRF + JWT)
### 3.1 Create backend folder + virtual environment
```bash
mkdir backend
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
```
### 3.2 Install packages
```bash
pip install django djangorestframework django-cors-headers djangorestframework￾simplejwt psycopg2-binary python-dotenv openai gunicorn whitenoise
pip freeze > requirements.txt
```
### 3.3 Start Django project
```bash
django-admin startproject config .
python manage.py startapp api
```
### 3.4 Folder structure (backend/)
```
backend/
 config/
 __init__.py
 settings.py
 urls.py
 wsgi.py
 api/
 migrations/
 __init__.py
 models.py
 views.py
 serializers.py
 urls.py
 .venv/
 manage.py
 requirements.txt
 .env
```
### 3.5 Create backend/.env
```
DJANGO_SECRET_KEY=replace-this-with-a-long-random-string-min-50-chars
DJANGO_DEBUG=True
DB_NAME=studybuddy_db
DB_USER=studybuddy_user
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=5432
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```
### 3.6 settings.py
```python
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-dev-key")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
INSTALLED_APPS = [
 "django.contrib.admin",
 "django.contrib.auth",
 "django.contrib.contenttypes",
 "django.contrib.sessions",
 "django.contrib.messages",
 "django.contrib.staticfiles",
 "rest_framework",
 "corsheaders",
 "api",
]
MIDDLEWARE = [
 "corsheaders.middleware.CorsMiddleware",
 "django.middleware.security.SecurityMiddleware",
 "whitenoise.middleware.WhiteNoiseMiddleware",
 "django.contrib.sessions.middleware.SessionMiddleware",
 "django.middleware.common.CommonMiddleware",
 "django.middleware.csrf.CsrfViewMiddleware",
 "django.contrib.auth.middleware.AuthenticationMiddleware",
 "django.contrib.messages.middleware.MessageMiddleware",
 "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
 {
 "BACKEND": "django.template.backends.django.DjangoTemplates",
 "DIRS": [],
 "APP_DIRS": True,
 "OPTIONS": {
 "context_processors": [
 "django.template.context_processors.debug",
 "django.template.context_processors.request",
 "django.contrib.auth.context_processors.auth",
 "django.contrib.messages.context_processors.messages",
 ],
 },
 },
]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {
 "default": {
 "ENGINE": "django.db.backends.postgresql",
 "NAME": os.getenv("DB_NAME"),
 "USER": os.getenv("DB_USER"),
 "PASSWORD": os.getenv("DB_PASSWORD"),
 "HOST": os.getenv("DB_HOST", "localhost"),
 "PORT": os.getenv("DB_PORT", "5432"),
 }
}
AUTH_PASSWORD_VALIDATORS = [
 {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]
REST_FRAMEWORK = {
 "DEFAULT_AUTHENTICATION_CLASSES": (
 "rest_framework_simplejwt.authentication.JWTAuthentication",
 ),
 "DEFAULT_PERMISSION_CLASSES": (
 "rest_framework.permissions.IsAuthenticated",
 ),
}
SIMPLE_JWT = {
 "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
 "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
 "AUTH_HEADER_TYPES": ("Bearer",),
}
CORS_ALLOWED_ORIGINS = os.getenv(
 "CORS_ALLOWED_ORIGINS", "http://localhost:5173"
).split(",")
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Amman"
USE_I18N = True
USE_TZ = True
```
### 3.7 models.py
```python
from django.db import models
from django.contrib.auth.models import User
class Note(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
 title = models.CharField(max_length=255)
 content = models.TextField()
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)
 def __str__(self):
 return f"{self.user.username} — {self.title}"
class BugReport(models.Model):
 PRIORITY = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
 user = models.ForeignKey(
 User, on_delete=models.SET_NULL,
 null=True, blank=True, related_name="reports"
 )
 title = models.CharField(max_length=255)
 description = models.TextField()
 steps = models.TextField()
 expected = models.TextField()
 actual = models.TextField()
 browser = models.CharField(max_length=100, blank=True)
 priority = models.CharField(max_length=10, choices=PRIORITY, default="medium")
 created_at = models.DateTimeField(auto_now_add=True)
 def __str__(self):
 return self.title
```
### 3.8 serializers.py
```python
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, BugReport
class RegisterSerializer(serializers.ModelSerializer):
 password = serializers.CharField(write_only=True, min_length=8)
 class Meta:
 model = User
 fields = ("id", "username", "email", "password")
 def create(self, validated_data):
 return User.objects.create_user(
 username=validated_data["username"],
 email=validated_data.get("email", ""),
 password=validated_data["password"],
 )
class UserSerializer(serializers.ModelSerializer):
 class Meta:
 model = User
 fields = ("id", "username", "email")
class NoteSerializer(serializers.ModelSerializer):
 class Meta:
 model = Note
 fields = ("id", "title", "content", "created_at", "updated_at")
 read_only_fields = ("id", "created_at", "updated_at")
class BugReportSerializer(serializers.ModelSerializer):
 class Meta:
 model = BugReport
 fields = "__all__"
 read_only_fields = ("id", "created_at", "user")
```
### 3.9 views.py
```python
import os
import json
from openai import OpenAI
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Note, BugReport
from .serializers import (
 RegisterSerializer, UserSerializer,
 NoteSerializer, BugReportSerializer,
)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Auth
class RegisterView(generics.CreateAPIView):
 queryset = User.objects.all()
 serializer_class = RegisterSerializer
 permission_classes = [AllowAny]
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
 return Response(UserSerializer(request.user).data)
# Notes
class NoteListCreateView(generics.ListCreateAPIView):
 serializer_class = NoteSerializer
 permission_classes = [IsAuthenticated]
 def get_queryset(self):
 return Note.objects.filter(user=self.request.user).order_by("-created_at")
 def perform_create(self, serializer):
 serializer.save(user=self.request.user)
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
 serializer_class = NoteSerializer
 permission_classes = [IsAuthenticated]
 def get_queryset(self):
 return Note.objects.filter(user=self.request.user)
# Bug Reports
class BugReportListCreateView(generics.ListCreateAPIView):
 serializer_class = BugReportSerializer
 permission_classes = [AllowAny]
 def get_queryset(self):
 return BugReport.objects.all().order_by("-created_at")
 def perform_create(self, serializer):
 user = self.request.user if self.request.user.is_authenticated else None
 serializer.save(user=user)
# AI Features
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def summarize(request):
 text = request.data.get("text", "").strip()
 if not text:
 return Response({"error": "text is required"}, status=400)
 if len(text) > 5000:
 return Response({"error": "text too long (max 5000 chars)"}, status=400)
 try:
 response = client.chat.completions.create(
 model="gpt-3.5-turbo",
 messages=[
 {
 "role": "system",
 "content": (
 "You are a helpful study assistant. "
 "Summarize the provided text in clear bullet points. "
 "Be concise. Do not add information not in the text."
 ),
 },
 {"role": "user", "content": f"Summarize this:\n\n{text}"},
 ],
 max_tokens=500,
 temperature=0.3,
 )
 return Response({"summary": response.choices[0].message.content})
 except Exception as e:
 return Response({"error": "AI service error", "detail": str(e)}, status=500)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_quiz(request):
 text = request.data.get("text", "").strip()
 count = int(request.data.get("count", 5))
 if not text:
 return Response({"error": "text is required"}, status=400)
 if len(text) > 5000:
 return Response({"error": "text too long (max 5000 chars)"}, status=400)
 if not (1 <= count <= 10):
 return Response({"error": "count must be 1-10"}, status=400)
 try:
 response = client.chat.completions.create(
 model="gpt-3.5-turbo",
 messages=[
 {
 "role": "system",
 "content": (
 f"Generate {count} multiple-choice questions from the text. "
 "Return a JSON array: "
 '[{"question":"...","options":["A)...","B)...","C)...","D)..."],"answer":"A"}]'
 " Return ONLY the JSON array."
 ),
 },
 {"role": "user", "content": f"Generate quiz from:\n\n{text}"},
 ],
 max_tokens=1000,
 temperature=0.4,
 )
 raw = response.choices[0].message.content
 questions = json.loads(raw)
 return Response({"questions": questions})
 except Exception as e:
 return Response({"error": "AI service error", "detail": str(e)}, status=500)
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
 return Response({"status": "ok", "project": "Study Buddy"})
```
### 3.10 api/urls.py
```python
from django.urls import path
from . import views
urlpatterns = [
 path("health/", views.health),
 path("auth/register/", views.RegisterView.as_view()),
 path("auth/me/", views.me),
 path("notes/", views.NoteListCreateView.as_view()),
 path("notes/<int:pk>/", views.NoteDetailView.as_view()),
 path("bug-reports/", views.BugReportListCreateView.as_view()),
 path("ai/summarize/", views.summarize),
 path("ai/quiz/", views.generate_quiz),
]
```
### 3.11 config/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
 path("admin/", admin.site.urls),
 path("api/", include("api.urls")),
 path("api/token/", TokenObtainPairView.as_view()),
 path("api/token/refresh/", TokenRefreshView.as_view()),
]
```
---
## PHASE 4 — PostgreSQL
### 4.1 Open SQL Shell (psql)
Start menu → search "SQL Shell (psql)" → open 
Press Enter for all defaults → enter your postgres password
### 4.2 Create user + database
```sql
CREATE USER studybuddy_user WITH PASSWORD 'strong_password';
CREATE DATABASE studybuddy_db OWNER studybuddy_user;
GRANT ALL PRIVILEGES ON DATABASE studybuddy_db TO studybuddy_user;
\q
```
### 4.3 Run migrations
```bash
cd backend
.venv\Scripts\activate
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
### 4.4 Test
- http://127.0.0.1:8000/api/health/ → should return {"status":"ok"}
- http://127.0.0.1:8000/admin → admin panel
---
## PHASE 5 — Frontend (React + Vite)
### 5.1 Create React app
```bash
cd ..
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install axios react-router-dom
```
### 5.2 Create frontend/.env
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```
### 5.3 Folder structure (frontend/src/)
```
src/
 api/
 axios.js
 context/
 AuthContext.jsx
 components/
 ProtectedRoute.jsx
 Navbar.jsx
 pages/
 Login.jsx
 Register.jsx
 Notes.jsx
 AITools.jsx
 Support.jsx
 App.jsx
 main.jsx
```
### 5.4 src/api/axios.js
```javascript
import axios from "axios";
const api = axios.create({
 baseURL: import.meta.env.VITE_API_BASE_URL,
});
api.interceptors.request.use((config) => {
 const token = localStorage.getItem("access");
 if (token) config.headers.Authorization = `Bearer ${token}`;
 return config;
});
api.interceptors.response.use(
 (res) => res,
 async (error) => {
 const original = error.config;
 if (error.response?.status === 401 && !original._retry) {
 original._retry = true;
 try {
 const refresh = localStorage.getItem("refresh");
 const { data } = await axios.post(
 `${import.meta.env.VITE_API_BASE_URL}/api/token/refresh/`,
 { refresh }
 );
 localStorage.setItem("access", data.access);
 original.headers.Authorization = `Bearer ${data.access}`;
 return api(original);
 } catch {
 localStorage.clear();
 window.location.href = "/login";
 }
 }
 return Promise.reject(error);
 }
);
export default api;
```
### 5.5 src/context/AuthContext.jsx
```javascript
import { createContext, useContext, useState } from "react";
import api from "../api/axios";
const AuthContext = createContext(null);
export function AuthProvider({ children }) {
 const [user, setUser] = useState(
 JSON.parse(localStorage.getItem("user") || "null")
 );
 const login = async (username, password) => {
 const { data } = await api.post("/api/token/", { username, password });
 localStorage.setItem("access", data.access);
 localStorage.setItem("refresh", data.refresh);
 const me = await api.get("/api/auth/me/");
 localStorage.setItem("user", JSON.stringify(me.data));
 setUser(me.data);
 };
 const register = async (username, email, password) => {
 await api.post("/api/auth/register/", { username, email, password });
 await login(username, password);
 };
 const logout = () => {
 localStorage.clear();
 setUser(null);
 };
 return (
 <AuthContext.Provider value={{ user, login, register, logout }}>
 {children}
 </AuthContext.Provider>
 );
}
export const useAuth = () => useContext(AuthContext);
```
### 5.6 src/components/ProtectedRoute.jsx
```javascript
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
export default function ProtectedRoute({ children }) {
 const { user } = useAuth();
 return user ? children : <Navigate to="/login" replace />;
}
```
### 5.7 src/App.jsx
```javascript
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Notes from "./pages/Notes";
import Support from "./pages/Support";
import AITools from "./pages/AITools";
export default function App() {
 return (
 <AuthProvider>
 <BrowserRouter>
 <Routes>
 <Route path="/" element={<Navigate to="/notes" replace />} />
 <Route path="/login" element={<Login />} />
 <Route path="/register" element={<Register />} />
 <Route path="/notes" element={<ProtectedRoute><Notes /></ProtectedRoute>} />
 <Route path="/ai" element={<ProtectedRoute><AITools /></ProtectedRoute>} />
 <Route path="/support" element={<Support />} />
 </Routes>
 </BrowserRouter>
 </AuthProvider>
 );
}
```
---
## PHASE 6 — Run Locally
### Terminal 1 — Backend
```bash
cd backend
.venv\Scripts\activate
python manage.py runserver
```
### Terminal 2 — Frontend
```bash
cd frontend
npm run dev
```
### Open browser
- Frontend: http://localhost:5173
- Backend API: http://127.0.0.1:8000/api/health/
- Admin: http://127.0.0.1:8000/admin
### Test checklist
- [ ] Register new user
- [ ] Login → redirected to /notes
- [ ] Create a note
- [ ] Go to AI Tools → summarize text
- [ ] Generate quiz from text
- [ ] Logout → try /notes (redirects to login)
- [ ] Submit a bug report (no login needed)
---
## PHASE 7 — OpenAI API
### 7.1 Get API key
1. Go to https://platform.openai.com
2. Sign up / login
3. Go to API Keys → Create new secret key
4. Copy the key (starts with sk-)
### 7.2 Add to .env
```
OPENAI_API_KEY=sk-your-key-here
```
### 7.3 API endpoints available
| Endpoint | Method | Auth | Description |
|---|---|---|---|
| /api/ai/summarize/ | POST | Required | Summarize text |
| /api/ai/quiz/ | POST | Required | Generate MCQ quiz |
### 7.4 Request format
```json
{
 "text": "Your study notes here...",
 "count": 5
}
```
### 7.5 Safety rules (important)
- Max text: 5000 characters
- API key ONLY in backend .env
- Never expose key in frontend code
- Always validate input before calling OpenAI
---
## PHASE 8 — Deployment
### 8.1 Prepare for production
Create `backend/build.sh`:
```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```
Push to GitHub:
```bash
git add .
git commit -m "feat: ready for deployment"
git push
```
### 8.2 Deploy PostgreSQL on Render
1. Go to https://render.com → Sign up
2. New → PostgreSQL
3. Name: `studybuddy-db`
4. Region: Frankfurt (EU)
5. Plan: Free
6. Create → copy **Internal Database URL**
### 8.3 Deploy Django Backend on Render
1. New → Web Service
2. Connect GitHub → select `study-buddy`
3. Settings:
 - Root directory: `backend`
 - Runtime: Python 3
 - Build command:
 ```
 pip install -r requirements.txt && python manage.py collectstatic --no-input && python 
manage.py migrate
 ```
 - Start command:
 ```
 gunicorn config.wsgi:application
 ```
4. Add environment variables:
| Key | Value |
|---|---|
| DJANGO_SECRET_KEY | (long random string 50+ chars) |
| DJANGO_DEBUG | False |
| DATABASE_URL | (paste from Render Postgres) |
| ALLOWED_HOSTS | your-service-name.onrender.com |
| OPENAI_API_KEY | sk-your-key |
| CORS_ALLOWED_ORIGINS | https://your-app.vercel.app |
5. Deploy
### 8.4 Update settings.py for DATABASE_URL (Render)
Add to settings.py:
```python
import dj_database_url
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
 DATABASES["default"] = dj_database_url.config(default=DATABASE_URL)
```
Install package:
```bash
pip install dj-database-url
pip freeze > requirements.txt
```
### 8.5 Deploy React Frontend on Vercel
1. Go to https://vercel.com → Sign up
2. New Project → Import GitHub repo
3. Settings:
 - Root directory: `frontend`
 - Build command: `npm run build`
 - Output directory: `dist`
4. Add environment variable:
 - `VITE_API_BASE_URL` = `https://your-backend.onrender.com`
5. Deploy
6. Copy your Vercel URL
### 8.6 Final connection
1. Copy Vercel URL (e.g., https://study-buddy.vercel.app)
2. Go to Render backend → Environment
3. Update `CORS_ALLOWED_ORIGINS` = `https://study-buddy.vercel.app`
4. Save → Render will redeploy automatically
### 8.7 Production test checklist
- [ ] Frontend loads on Vercel URL
- [ ] Register works
- [ ] Login returns JWT token
- [ ] Notes save to Postgres
- [ ] AI summarize works
- [ ] AI quiz works
- [ ] Bug report submits
- [ ] Logout clears session
---
## Architecture Diagram
```
Student Browser
 │
 ▼
React App (Vercel) ──────────────────────────────────
 │ │
 │ HTTPS + JWT Bearer Token │
 ▼ │
Django API (Render) │
 │ │ │
 ▼ ▼ │
PostgreSQL OpenAI API │
(Render DB) (GPT-3.5) │
 │
Static files ◄───────────────────────────────────────
(WhiteNoise)
```
---
## Quick Reference — All Commands
```bash
# ── SETUP ──────────────────────────────────────────────────────────────────
# Clone project
git clone https://github.com/<YOU>/study-buddy.git
cd study-buddy
# ── BACKEND ────────────────────────────────────────────────────────────────
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# ── FRONTEND ───────────────────────────────────────────────────────────────
cd frontend
npm install
npm run dev
# ── GIT ────────────────────────────────────────────────────────────────────
git add .
git commit -m "message"
git push
# ── DATABASE ───────────────────────────────────────────────────────────────
# Create migration after model change
python manage.py makemigrations
python manage.py migrate
# ── PRODUCTION ─────────────────────────────────────────────────────────────
# Build frontend
cd frontend && npm run build
# Collect static (Django)
cd backend && python manage.py collectstatic
```
---
## API Reference
| Endpoint | Method | Auth | Body | Description |
|---|---|---|---|---|
| /api/health/ | GET | No | — | Health check |
| /api/auth/register/ | POST | No | username, email, password | Register |
| /api/token/ | POST | No | username, password | Login → JWT |
| /api/token/refresh/ | POST | No | refresh | Refresh token |
| /api/auth/me/ | GET | Yes | — | Current user |
| /api/notes/ | GET | Yes | — | List notes |
| /api/notes/ | POST | Yes | title, content | Create note |
| /api/notes/:id/ | GET | Yes | — | Get note |
| /api/notes/:id/ | PATCH | Yes | title?, content? | Update note |
| /api/notes/:id/ | DELETE | Yes | — | Delete note |
| /api/bug-reports/ | GET | No | — | List reports |
| /api/bug-reports/ | POST | No | all fields | Create report |
| /api/ai/summarize/ | POST | Yes | text | Summarize |
| /api/ai/quiz/ | POST | Yes | text, count | Generate quiz |
---
## Common Errors + Fixes
| Error | Cause | Fix |
|---|---|---|
| ModuleNotFoundError | venv not activated | Run `.venv\Scripts\activate` |
| psycopg2 error | Postgres not running | Start Postgres service |
| CORS error | Origin not in allowed list | Add frontend URL to CORS_ALLOWED_ORIGINS |
| 401 Unauthorized | Token missing/expired | Check Authorization header / refresh token |
| OpenAI error | Wrong API key | Check .env OPENAI_API_KEY |
| Vite env not loading | Wrong prefix | Use VITE_ prefix for all env vars |
| migrate error | DB not created | Create DB in psql first |
---
*Study Buddy — Built with Django + React + PostgreSQL + OpenAI* 
*Trainer: Mohammad Salhab | BTEC Grade 12 | Jordan | 2026*
