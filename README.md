# Ansh Air Cool - AC Service Management System

Complete business solution for an AC service and installation business in Mumbai, with two main parts:

1. **Customer website** - accepts service requests, shows services and pricing, and captures contact enquiries.
2. **Desktop billing software** - PySide6 desktop app for invoices, customers and reports.

This was built as a BCA final-year project (see `Akash_Nikhil_Blackbook.md` for the full project report).

## Features

### Website
- Service request and contact forms
- Service catalog with images and pricing
- Admin dashboard for managing enquiries, services and content
- Rate-limited Flask API with bcrypt password hashing and CSRF protection

### Desktop software
- GST invoice generation with PDF export (reportlab)
- Customer and service management
- Excel export (openpyxl)

## Technology stack

| Layer | Technologies |
|-------|--------------|
| Backend API | Flask 3, SQLAlchemy, PyMySQL, bcrypt, Flask-CORS, Flask-Limiter |
| Frontend | HTML5/CSS3, Bootstrap 5.3, JavaScript (ES6+), AOS |
| Desktop app | PySide6 (Qt6), mysql-connector, reportlab, openpyxl |
| Database | MySQL 8 (production), SQLite (development) |

## Quick start

Prerequisites: Python 3.8+, MySQL 8.0+.

```bash
# Backend
cd backend
pip install -r requirements.txt

# Desktop software
cd Desktop_software
pip install -r requirements.txt
```

Configure the database in `backend/.env` and `Desktop_software/.env` (see the `.env.example` files), then:

```bash
cd backend
python init_database_complete.py   # creates tables, admin user, default content
python main.py                     # API on http://localhost:5000
```

Serve `frontend/index.html` with any static server (e.g. the VS Code Live Server extension). Change any default admin credentials before deploying.
