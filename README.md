# 🌟 ANSH AIR COOL - AC Service Management System

> **Complete Business Solution for AC Service & Installation**  
> 📍 Mumbai, Maharashtra, India | 📞 +91 9819104977

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Screenshots](#screenshots)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

**Ansh Air Cool** ek professional AC service management system hai jo do main parts mein divide hai:

### 1. 🌐 Customer Website
- Service requests accept karta hai
- Contact form
- Products showcase (AC Sales & Rental)
- Testimonials
- Admin dashboard

### 2. 💻 Desktop Billing Software
- Customer management (CRM)
- Invoice generation with PDF
- AMC tracking
- Technician management
- Business analytics

**Dono parts ek centralized database use karte hain!**

---

## ✨ Features

### Website Features
- ✅ **Service Request System** - Installation, Repair, Gas Refill, Maintenance, AMC
- ✅ **Contact Form** - Direct customer communication
- ✅ **Product Catalog** - AC sales and rental showcase
- ✅ **Testimonials** - Customer reviews display
- ✅ **Image Gallery** - Work portfolio
- ✅ **Admin Dashboard** - Complete content management
- ✅ **Responsive Design** - Mobile-friendly
- ✅ **WhatsApp Integration** - Automated confirmations

### Desktop Software Features
- ✅ **User Authentication** - Secure login system
- ✅ **Customer Management** - Add, edit, search customers
- ✅ **Invoice Management** - Create, edit, delete invoices
- ✅ **PDF Generation** - Professional invoice PDFs
- ✅ **AMC Management** - Track annual maintenance contracts
- ✅ **Technician Management** - Assign jobs, track performance
- ✅ **Dashboard** - Real-time business statistics
- ✅ **Reports** - Excel export, analytics
- ✅ **Auto Backup** - Daily database backups

---

## 🛠️ Technology Stack

### Backend (Website API)
| Technology | Purpose |
|------------|---------|
| **Flask 3.0.0** | Web framework |
| **SQLAlchemy** | Database ORM |
| **PyMySQL** | MySQL connector |
| **bcrypt** | Password hashing |
| **Flask-CORS** | Cross-origin support |
| **Flask-Limiter** | Rate limiting |
| **Pillow** | Image processing |

### Frontend (Website)
| Technology | Purpose |
|------------|---------|
| **HTML5/CSS3** | Structure & styling |
| **Bootstrap 5.3.2** | Responsive framework |
| **JavaScript (ES6+)** | Client-side logic |
| **FontAwesome 6.5.1** | Icons |
| **AOS** | Scroll animations |

### Desktop Software
| Technology | Purpose |
|------------|---------|
| **PySide6 6.6.2** | Qt6 GUI framework |
| **mysql-connector** | Database connectivity |
| **reportlab** | PDF generation |
| **openpyxl** | Excel export |
| **psutil** | System monitoring |

### Database
- **MySQL 8.0+** (Production)
- **SQLite** (Development)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Desktop Software
cd Desktop_software
pip install -r requirements.txt
```

### Step 2: Configure Database

Edit `backend/.env`:
```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/ansh_aircool
```

Edit `Desktop_software/.env`:
```env
DB_PASSWORD=YOUR_PASSWORD
```

### Step 3: Initialize Database

```bash
cd backend
python init_database_complete.py
```

This creates:
- All database tables
- Admin user (username: `admin`, password: `Admin@123`)
- Default services
- Website content

### Step 4: Start Backend Server

```bash
cd backend
python main.py
```

Server will start at: **http://localhost:5000**

### Step 5: Open Website

**Option 1: Live Server (Recommended)**
- Install "Live Server" extension in VS Code
- Right-click `frontend/index.html`
- Select "Open with Live Server"

**Option 2: Direct File**
- Open `frontend/index.html` in browser

### Step 6: Start Desktop Software

```bash
cd Desktop_software
python main.py
```

Login with:
- Username: `admin`
- Password: `Admin@123`

---

## 📁 Project Structure

```
D:\Full_ac_website\
│
├── backend/                    # Flask API Server
│   ├── .env                    # Environment config ✅
│   ├── main.py                 # Application entry point
│   ├── routes.py               # Public API endpoints
│   ├── admin_routes.py         # Admin dashboard routes
│   ├── models.py               # Database models
│   ├── security.py             # Security utilities
│   ├── init_database_complete.py  # DB initialization ✅
│   └── requirements.txt        # Dependencies
│
├── frontend/                   # Static Website
│   ├── index.html              # Homepage
│   ├── admin/
│   │   ├── index.html          # Admin login
│   │   └── dashboard.html      # Admin panel
│   ├── js/
│   │   ├── settings.js         # API config
│   │   ├── api.js              # API client
│   │   ├── validation.js       # Form validation
│   │   └── admin-management.js # Admin logic ✅
│   ├── css/                    # Stylesheets
│   └── assets/                 # Images, icons
│
├── Desktop_software/           # PySide6 Desktop App
│   ├── .env                    # Environment config ✅
│   ├── main.py                 # Application entry
│   ├── config.py               # Configuration
│   ├── database/               # Database layer
│   ├── controllers/            # Business logic (MVC)
│   ├── views/                  # UI components
│   ├── utils/                  # Utilities
│   └── requirements.txt        # Dependencies
│
├── logs/                       # Application logs
├── backups/                    # Database backups
├── uploads/                    # User uploads
│
└── Documentation/
    ├── COMPLETE_DOCUMENTATION.txt    # Full docs ✅
    ├── CODE_STRUCTURE_EXPLAINED.txt  # Code comments ✅
    ├── FINAL_STATUS_HINDI.txt        # Hindi summary ✅
    ├── START_HERE.md                 # Quick start
    ├── SETUP_GUIDE.md                # Setup guide
    └── DEPLOYMENT_GUIDE.md           # Production deploy
```

---

## ⚙️ Configuration

### Backend (.env)

```env
# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=7f8a9b2c3d4e5f6a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a
API_KEY=ansh_aircool_secure_api_key_2026_production_ready

# Database
DATABASE_URL=mysql+pymysql://root:Akash%409918@localhost:3306/ansh_aircool
# Note: @ in password encoded as %40

# CORS
FRONTEND_URL=http://localhost:5500

# Session Security
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600

# Rate Limiting
RATELIMIT_ENABLED=true
RATELIMIT_DEFAULT=100 per day
```

### Desktop Software (.env)

```env
# Database
DB_PASSWORD=Akash@9918
DB_USER=root
DB_HOST=localhost
DB_NAME=ac_service_billing
DB_PORT=3306

# Application
APP_ENV=development
LOG_LEVEL=DEBUG

# Security
LOGIN_ENABLED=true        # Production: true
SESSION_TIMEOUT=3600

# Backup
AUTO_BACKUP_ENABLED=true
BACKUP_INTERVAL_HOURS=24
BACKUP_RETENTION_DAYS=7
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **COMPLETE_DOCUMENTATION.txt** | Full project documentation |
| **CODE_STRUCTURE_EXPLAINED.txt** | Code with detailed comments |
| **FINAL_STATUS_HINDI.txt** | Hindi summary |
| **START_HERE.md** | Quick start guide |
| **SETUP_GUIDE.md** | Detailed setup instructions |
| **DEPLOYMENT_GUIDE.md** | Production deployment guide |
| **FIX_SUMMARY.md** | What was fixed |

---

## 🖼️ Screenshots

### Website
- Homepage with hero section
- Services showcase
- Product catalog
- Contact form
- Admin dashboard

### Desktop Software
- Login screen
- Main dashboard
- Customer management
- Invoice creation
- AMC tracking
- Reports & analytics

---

## 🌐 Deployment

### Production Checklist

1. **Change Default Passwords**
   - Admin password (website)
   - Desktop software users
   - Database password

2. **Update Security Keys**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Update in `backend/.env`:
   - `SECRET_KEY`
   - `API_KEY`

3. **Enable HTTPS**
   - Get SSL certificate (Let's Encrypt)
   - Configure Nginx/Apache
   - Update `FRONTEND_URL` to HTTPS

4. **Set Production Mode**
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=False
   SESSION_COOKIE_SECURE=True
   ```

5. **Enable Backups**
   ```env
   BACKUP_ENABLED=true
   AUTO_BACKUP_ENABLED=true
   ```

See **DEPLOYMENT_GUIDE.md** for complete instructions.

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check MySQL is running
sc query MySQL80

# Verify .env exists
dir backend\.env

# Test database connection
python -c "from main import create_app; app = create_app()"
```

### Database connection failed
1. Check MySQL service is running
2. Verify password in `.env` files
3. Ensure `@` in password is encoded as `%40`
4. Test: `mysql -u root -p`

### Admin login fails
- Username: `admin`
- Password: `Admin@123`
- Clear browser cache
- Run `python init_database_complete.py` again

### Desktop software won't start
```bash
# Install dependencies
pip install -r requirements.txt

# Check database connection
# Verify LOGIN_ENABLED setting
```

### CORS errors
- Ensure backend allows frontend origin
- Use Live Server (port 5500)
- Check `FRONTEND_URL` in backend/.env

---

## 📞 Support

**Ansh Air Cool**  
📍 Mumbai, Maharashtra, India  
📞 +91 9819104977  
📧 anshaircool@gmail.com  

---

## 📄 License

© 2026 Ansh Air Cool. All rights reserved.

This is a proprietary business management system.  
Unauthorized copying or distribution is prohibited.

---

## 🎉 Credits

**Developed & Maintained By:** Ansh Air Cool Team  
**Version:** 1.0.0 (Production Ready)  
**Last Updated:** 2026-03-26  

---

<div align="center">

**Made with ❤️ for Ansh Air Cool**

[🔝 Back to Top](#ansh-air-cool---ac-service-management-system)

</div>
