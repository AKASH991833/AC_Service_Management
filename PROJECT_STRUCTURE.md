# 📁 COMPLETE PROJECT STRUCTURE - ANSH AIR COOL

## 🎯 Overview (Hindi Mein)

Yeh ek **complete AC Service Management System** hai jisme 3 main parts hain:

1. **Frontend (Website)** - Customer-facing website
2. **Backend (API Server)** - Database aur admin panel
3. **Software (Desktop App)** - Billing aur management software

---

## 📂 Complete File Structure

```
D:\WEBISTE UI ADN BAC - Copy\
│
├── 📁 frontend/                          # 🌐 CUSTOMER WEBSITE (React-less Modern Web App)
│   ├── 📄 index.html                     # 🏠 Main entry point - Homepage
│   ├── 📄 test-fixes.html                # 🧪 Testing file for fixes
│   ├── 📄 test-form-submission.html      # 🧪 Form testing
│   ├── 📄 test-modules.html              # 🧪 Module testing
│   │
│   ├── 📁 admin/                         # 👨‍💼 ADMIN PANEL (Complete Website Editor)
│   │   ├── 📄 dashboard.html             # 🎛️ Main admin dashboard (NEW - Full website control)
│   │   ├── 📄 test-login.html            # 🧪 Login testing
│   │   ├── 📄 quick-test.html            # 🧪 Quick tests
│   │   └── 📄 css-test.html              # 🧪 CSS testing
│   │
│   ├── 📁 css/                           # 🎨 STYLESHEETS
│   │   ├── 📄 variables.css              # 🎨 CSS variables (colors, fonts, themes)
│   │   ├── 📄 components.css             # 🔧 Reusable components (buttons, cards, etc.)
│   │   ├── 📄 animations.css             # ✨ Animations (particles, blobs, transitions)
│   │   ├── 📄 responsive.css             # 📱 Mobile responsive styles
│   │   ├── 📄 style.css                  # 🎯 Main website styles
│   │   ├── 📄 admin.css                  # 👨‍💼 Admin panel styles (dark theme)
│   │   └── 📄 product-tabs.css           # 🛍️ Product tabs specific styles
│   │
│   ├── 📁 js/                            # ⚡ JAVASCRIPT MODULES
│   │   ├── 📄 main.js                    # 🚀 Main entry point - coordinates all modules
│   │   ├── 📄 config.js                  # ⚙️ App configuration & settings
│   │   ├── 📄 settings.js                # 🎛️ Frontend settings object
│   │   ├── 📄 ui-effects.js              # ✨ UI effects (cursor trail, particles, blobs)
│   │   ├── 📄 interactions.js            # 👆 User interactions (scroll, hover, clicks)
│   │   ├── 📄 validation.js              # ✅ Form validation logic
│   │   ├── 📄 api.js                     # 🔌 API calls to backend
│   │   ├── 📄 sections-loader.js         # 📄 Dynamic HTML section loader
│   │   ├── 📄 lazy-loader.js             # 🐌 Lazy loading for images/content
│   │   ├── 📄 admin.js                   # 👨‍💼 Old admin logic (deprecated)
│   │   └── 📄 admin-management.js        # 👨‍💼 Admin management functions
│   │
│   ├── 📁 sections/                      # 🧩 HTML SECTIONS (Loaded dynamically)
│   │   ├── 📄 hero.html                  # 🦸 Hero section (top banner)
│   │   ├── 📄 justdial.html              # ⭐ JustDial trust badge section
│   │   ├── 📄 services.html              # 🔧 Services showcase
│   │   ├── 📄 products.html              # 🛍️ Products (Buy & Rent AC)
│   │   ├── 📄 features.html              # ✨ Why choose us section
│   │   ├── 📄 stats.html                 # 📊 Statistics counter
│   │   ├── 📄 testimonials.html          # 💬 Customer reviews
│   │   ├── 📄 contact.html               # 📞 Contact form & info
│   │   └── 📄 footer.html                # 🔻 Footer section
│   │
│   ├── 📁 assets/                        # 🖼️ ASSETS
│   │   └── 📁 images/                    # 📸 Images folder
│   │
│   └── 📁 .vscode/                       # ⚙️ VSCODE SETTINGS
│       └── 📄 settings.json              # Editor configuration
│
├── 📁 backend/                           # 🔧 FLASK BACKEND API SERVER
│   ├── 📄 main.py                        # 🚀 Main Flask application entry point
│   ├── 📄 models.py                      # 💾 Database models (SQLAlchemy ORM)
│   │                                     #   - Admin, ServiceRequest, ContactMessage
│   │                                     #   - Service, Product, Testimonial
│   │                                     #   - GalleryImage, WebsiteContent, WebsiteSetting
│   │
│   ├── 📄 routes.py                      # 🛣️ Public API routes
│   │                                     #   - POST /api/service-request
│   │                                     #   - POST /api/contact
│   │                                     #   - GET /api/service-request
│   │                                     #   - GET /api/contact
│   │
│   ├── 📄 admin_routes.py                # 👨‍💼 ADMIN PANEL APIs (NEW - 50+ endpoints)
│   │                                     #   - Section management (Hero, Services, Products, etc.)
│   │                                     #   - CRUD operations for all content
│   │                                     #   - Image upload endpoints
│   │                                     #   - Site settings management
│   │
│   ├── 📄 security.py                    # 🔒 Security utilities
│   │                                     #   - Password hashing (bcrypt)
│   │                                     #   - Session validation
│   │                                     #   - Input sanitization
│   │                                     #   - Security event logging
│   │
│   ├── 📄 whatsapp.py                    # 📱 WhatsApp integration
│   │                                     #   - Send service confirmations
│   │                                     #   - Send contact message replies
│   │
│   ├── 📄 customer_routes.py             # 👥 Customer management routes
│   ├── 📄 new_routes.py                  # 🆕 New experimental routes
│   │
│   ├── 🗄️ DATABASE SETUP FILES:
│   ├── 📄 init_db.py                     # 🗄️ Initialize database tables
│   ├── 📄 init_admin_db.py               # 👨‍💼 Initialize admin user
│   ├── 📄 init_admin_full.py             # 👨‍💼 Full admin setup with data
│   ├── 📄 setup_admin_db.py              # ✅ Complete DB setup (RECOMMENDED)
│   ├── 📄 migrate_admin.py               # 🔄 Database migration
│   ├── 📄 migrate_db.py                  # 🔄 General migration
│   ├── 📄 migrate_customers.py           # 🔄 Customer migration
│   ├── 📄 migrate_service_requests.py    # 🔄 Service requests migration
│   │
│   ├── 🗄️ FIX & MAINTENANCE FILES:
│   ├── 📄 check_db.py                    # 🔍 Check database connection
│   ├── 📄 verify_admin.py                # 👨‍💼 Verify admin user
│   ├── 📄 fix_service_requests_table.py  # 🔧 Fix service requests table
│   ├── 📄 create_gallery_table.py        # 🗄️ Create gallery table
│   ├── 📄 create_new_tables.py           # 🗄️ Create new tables
│   ├── 📄 update_contact_messages_table.sql  # 🗄️ SQL migration
│   │
│   ├── 📄 test_data.py                   # 🧪 Test data generator
│   ├── 📄 quick_test.py                  # 🧪 Quick API tests
│   │
│   ├── 📄 .env                           # 🔐 Environment variables (DB credentials, API keys)
│   ├── 📄 .env.example                   # 📝 Example environment file
│   ├── 📄 .env.production                # 🚀 Production environment
│   ├── 📄 requirements.txt               # 📦 Python dependencies
│   ├── 📄 package-lock.json              # 📦 NPM lock file (unused)
│   └── 📄 backend.log                    # 📋 Application logs
│
├── 📁 software for ai creater - Copy/    # 🖥️ DESKTOP BILLING SOFTWARE (PySide6 Qt)
│   │                                     # Professional AC Service Management System
│   │
│   ├── 📄 main.py                        # 🚀 Main application entry point (Qt GUI)
│   ├── 📄 config.py                      # ⚙️ Application configuration
│   ├── 📄 requirements.txt               # 📦 Python dependencies (PySide6, etc.)
│   ├── 📄 .env                           # 🔐 Environment variables
│   ├── 📄 .env.example                   # 📝 Example environment
│   │
│   ├── 📁 database/                      # 🗄️ DATABASE LAYER
│   │   ├── 📄 __init__.py                # 📦 Package initializer
│   │   ├── 📄 db_connection.py           # 🔌 Database connection manager
│   │   ├── 📄 models.py                  # 💾 Data models
│   │   └── 📄 queries.py                 # 📝 SQL queries
│   │
│   ├── 📁 controllers/                   # 🎮 BUSINESS LOGIC
│   │   ├── 📄 __init__.py                # 📦 Package initializer
│   │   ├── 📄 auth_controller.py         # 🔐 Authentication logic
│   │   ├── 📄 customer_controller.py     # 👥 Customer management
│   │   ├── 📄 invoice_controller.py      # 📄 Invoice generation & management
│   │   ├── 📄 amc_controller.py          # 📋 AMC (Annual Maintenance Contract)
│   │   ├── 📄 technician_controller.py   # 👨‍🔧 Technician management
│   │   ├── 📄 dashboard_controller.py    # 📊 Dashboard data
│   │   ├── 📄 settings_controller.py     # ⚙️ Settings management
│   │   └── 📄 online_request_controller.py # 🌐 Online requests
│   │
│   ├── 📁 views/                         # 👁️ USER INTERFACE (Qt Widgets)
│   │   ├── 📄 __init__.py                # 📦 Package initializer
│   │   ├── 📄 main_window.py             # 🪟 Main application window
│   │   ├── 📄 login_view.py              # 🔐 Login screen
│   │   ├── 📄 base_window.py             # 🪟 Base window class
│   │   ├── 📄 customer_view.py           # 👥 Customer management UI
│   │   ├── 📄 invoice_view.py            # 📄 Invoice list UI
│   │   ├── 📄 invoice_management_view.py # 📄 Invoice creation UI
│   │   ├── 📄 edit_invoice_dialog.py     # ✏️ Edit invoice dialog
│   │   ├── 📄 amc_view.py                # 📋 AMC management UI
│   │   ├── 📄 technician_view.py         # 👨‍🔧 Technician UI
│   │   ├── 📄 online_request_view.py     # 🌐 Online requests UI
│   │   ├── 📄 settings_view.py           # ⚙️ Settings UI
│   │   ├── 📄 dashboard_view.py          # 📊 Dashboard UI
│   │   └── 📄 enhanced_dashboard_view.py # 📊 Enhanced dashboard
│   │
│   ├── 📁 utils/                         # 🛠️ UTILITY FUNCTIONS
│   │   ├── 📄 __init__.py                # 📦 Package initializer
│   │   ├── 📄 formatters.py              # 📝 Data formatting
│   │   ├── 📄 validators.py              # ✅ Input validation
│   │   ├── 📄 pdf_generator.py           # 📄 PDF generation
│   │   ├── 📄 pdf_invoice_generator.py   # 📄 Invoice PDF generator
│   │   ├── 📄 whatsapp_helper.py         # 📱 WhatsApp integration
│   │   ├── 📄 whatsapp_messages.py       # 💬 WhatsApp message templates
│   │   ├── 📄 session_manager.py         # 🔐 Session management
│   │   └── 📄 unified_theme.py           # 🎨 Qt theme styling
│   │
│   ├── 📁 sql/                           # 🗄️ SQL SCRIPTS
│   │   ├── 📄 setup_database.sql         # 🗄️ Database setup script
│   │   ├── 📄 add_contact_messages_table.sql  # 🗄️ Add contact table
│   │   ├── 📄 migration_add_booking_fields.sql  # 🗄️ Add booking fields
│   │   └── 📄 migration_add_indexes.sql  # 🗄️ Add database indexes
│   │
│   ├── 📁 exports/                       # 📤 EXPORTED FILES
│   │   └── (CSV exports, reports)
│   │
│   ├── 📁 invoices_pdf/                  # 📄 GENERATED INVOICES (PDF)
│   │   └── (Customer invoice PDFs)
│   │
│   ├── 📁 pdfs/                          # 📄 OTHER PDFs
│   │   └── (AMC contracts, reports)
│   │
│   ├── 📄 auto_backup.py                 # 💾 Automatic backup script
│   ├── 📄 backup_daily.bat               # 💾 Daily backup batch file
│   └── 📄 setup_auto_backup.bat          # ⚙️ Setup backup automation
│
├── 📁 uploads/                           # 📤 UPLOADED FILES
│   └── 📁 gallery/                       # 🖼️ Gallery images
│       └── (Uploaded images from admin)
│
├── 📁 archive/                           # 🗄️ OLD/ARCHIVED FILES
│   └── 📁 docs/                          # 📄 Documentation
│
├── 📄 .gitignore                         # 🚫 Git ignore rules
├── 📄 package-lock.json                  # 📦 Root package lock (unused)
│
├── 🗄️ DATABASE SCRIPTS:
├── 📄 create_tables.bat                  # 🗄️ Create database tables
├── 📄 run_migration.py                   # 🔄 Run migrations
│
├── 🚀 STARTUP SCRIPTS:
├── 📄 start.bat                          # ▶️ Start everything
├── 📄 start_backend.bat                  # ▶️ Start backend only
├── 📄 start_full_stack.bat               # ▶️ Start full stack
├── 📄 setup_and_start.bat                # ⚙️ Setup & start
├── 📄 restart_backend.bat                # 🔄 Restart backend
├── 📄 restart_with_security.bat          # 🔄 Restart with security
├── 📄 add_routes.bat                     # 🛣️ Add routes
│
├── 🧹 CLEANUP SCRIPTS:
├── 📄 cleanup.bat                        # 🧹 Cleanup files
├── 📄 cleanup_duplicates.bat             # 🧹 Remove duplicates
│
├── 📄 cookies.txt                        # 🍪 Test cookies
│
└── 📚 DOCUMENTATION:
    ├── 📄 ADMIN_PANEL_README.md          # 👨‍💼 Admin panel guide
    ├── 📄 QUICK_START.md                 # 🚀 Quick start guide
    ├── 📄 ADMIN_TESTING_REPORT.md        # ✅ Testing report
    └── 📄 ADMIN_COMPLETE_SUMMARY.md      # 🎉 Complete summary (Hindi)
```

---

## 🔍 Detailed File Descriptions

### 🌐 FRONTEND (Website)

#### Main Files
| File | Purpose | Description |
|------|---------|-------------|
| `index.html` | 🏠 Homepage | Main entry point, loads all sections dynamically |
| `admin/dashboard.html` | 👨‍💼 Admin Panel | Complete website editor (NEW) |

#### CSS Files (Styles)
| File | Purpose | Description |
|------|---------|-------------|
| `variables.css` | 🎨 Theme Variables | Colors, fonts, spacing constants |
| `components.css` | 🔧 Components | Buttons, cards, forms, navbars |
| `animations.css` | ✨ Animations | Particles, blobs, loading screens |
| `responsive.css` | 📱 Responsive | Mobile & tablet layouts |
| `style.css` | 🎯 Main Styles | Primary website styling |
| `admin.css` | 👨‍💼 Admin Styles | Dark theme admin panel |
| `product-tabs.css` | 🛍️ Product Tabs | AC product tabs styling |

#### JavaScript Files (Logic)
| File | Purpose | Description |
|------|---------|-------------|
| `main.js` | 🚀 Main Entry | Initializes all modules |
| `config.js` | ⚙️ Config | App-wide configuration |
| `settings.js` | 🎛️ Settings | Frontend settings object |
| `ui-effects.js` | ✨ Effects | Cursor trail, particles, blobs |
| `interactions.js` | 👆 Interactions | Scroll, hover, click handlers |
| `validation.js` | ✅ Validation | Form validation logic |
| `api.js` | 🔌 API Calls | Backend communication |
| `sections-loader.js` | 📄 Loader | Dynamic HTML loading |
| `lazy-loader.js` | 🐌 Lazy Load | Performance optimization |

#### HTML Sections
| File | Purpose | Description |
|------|---------|-------------|
| `hero.html` | 🦸 Hero | Top banner with CTA |
| `justdial.html` | ⭐ Trust Badge | JustDial verification |
| `services.html` | 🔧 Services | AC service showcase |
| `products.html` | 🛍️ Products | Buy & Rent AC |
| `features.html` | ✨ Features | Why choose us |
| `stats.html` | 📊 Stats | Counter statistics |
| `testimonials.html` | 💬 Reviews | Customer testimonials |
| `contact.html` | 📞 Contact | Contact form & info |
| `footer.html` | 🔻 Footer | Footer links & info |

---

### 🔧 BACKEND (Flask API Server)

#### Core Files
| File | Purpose | Description |
|------|---------|-------------|
| `main.py` | 🚀 Entry Point | Flask application factory |
| `models.py` | 💾 Models | SQLAlchemy ORM models |
| `routes.py` | 🛣️ Routes | Public API endpoints |
| `admin_routes.py` | 👨‍💼 Admin APIs | Admin panel endpoints (NEW) |
| `security.py` | 🔒 Security | Auth, hashing, validation |
| `whatsapp.py` | 📱 WhatsApp | Message sending logic |

#### Database Setup
| File | Purpose | Description |
|------|---------|-------------|
| `setup_admin_db.py` | ✅ Full Setup | Complete DB setup (USE THIS) |
| `init_admin_full.py` | 👨‍💼 Init Admin | Admin + default data |
| `init_db.py` | 🗄️ Init DB | Basic table creation |
| `migrate_admin.py` | 🔄 Migration | Schema updates |

#### Models (Database Tables)
| Model | Table | Purpose |
|-------|-------|---------|
| `Admin` | `admins` | Admin users |
| `ServiceRequest` | `service_requests` | Customer service requests |
| `ContactMessage` | `contact_messages` | Contact form submissions |
| `Service` | `services` | AC services offered |
| `Product` | `products` | AC products (Buy/Rent) |
| `Testimonial` | `testimonials` | Customer reviews |
| `GalleryImage` | `gallery_images` | Photo gallery |
| `WebsiteContent` | `website_content` | Editable website content |
| `WebsiteSetting` | `website_settings` | Site-wide settings |

---

### 🖥️ SOFTWARE (Desktop Billing App)

#### Architecture: MVC Pattern
```
📁 controllers/  →  Business Logic
📁 views/        →  User Interface (Qt Widgets)
📁 database/     →  Data Layer
📁 utils/        →  Helper Functions
```

#### Controllers (Business Logic)
| File | Purpose | Description |
|------|---------|-------------|
| `auth_controller.py` | 🔐 Auth | Login/logout logic |
| `customer_controller.py` | 👥 Customers | Customer CRUD |
| `invoice_controller.py` | 📄 Invoices | Invoice management |
| `amc_controller.py` | 📋 AMC | AMC contracts |
| `technician_controller.py` | 👨‍🔧 Technicians | Tech management |
| `dashboard_controller.py` | 📊 Dashboard | Dashboard data |
| `settings_controller.py` | ⚙️ Settings | App settings |
| `online_request_controller.py` | 🌐 Requests | Web requests |

#### Views (User Interface)
| File | Purpose | Description |
|------|---------|-------------|
| `main_window.py` | 🪟 Main Window | Primary UI |
| `login_view.py` | 🔐 Login | Login screen |
| `customer_view.py` | 👥 Customers | Customer management UI |
| `invoice_view.py` | 📄 Invoices | Invoice list UI |
| `amc_view.py` | 📋 AMC | AMC management UI |
| `technician_view.py` | 👨‍🔧 Technicians | Technician UI |
| `dashboard_view.py` | 📊 Dashboard | Main dashboard |

#### Utils (Helpers)
| File | Purpose | Description |
|------|---------|-------------|
| `pdf_generator.py` | 📄 PDF | PDF generation |
| `pdf_invoice_generator.py` | 📄 Invoices | Invoice PDFs |
| `whatsapp_helper.py` | 📱 WhatsApp | Send messages |
| `formatters.py` | 📝 Format | Data formatting |
| `validators.py` | ✅ Validate | Input validation |
| `session_manager.py` | 🔐 Session | User sessions |

---

## 🎯 How Everything Connects

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────┐
        │                                          │
        ▼                                          ▼
┌───────────────────┐                    ┌──────────────────┐
│   WEBSITE         │                    │  DESKTOP SOFTWARE │
│   (Frontend)      │                    │  (PySide6 Qt)     │
│   - Customers     │                    │  - Admin Staff    │
│   - Service Req   │                    │  - Billing        │
│   - Contact Form  │                    │  - Management     │
└─────────┬─────────┘                    └─────────┬────────┘
          │                                        │
          │ HTTP/REST API                          │ Direct DB
          │ (JSON)                                 │ (MySQL)
          ▼                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND API SERVER                           │
│                     (Flask - Port 5000)                         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   routes.py  │  │admin_routes.py│  │  whatsapp.py │         │
│  │  (Public)    │  │  (Admin Panel)│  │  (Messages)  │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                            │                                     │
│                            ▼                                     │
│                  ┌─────────────────┐                            │
│                  │   models.py     │                            │
│                  │   (ORM Layer)   │                            │
│                  └────────┬────────┘                            │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
                  ┌─────────────────┐
                  │   MySQL DB      │
                  │   (Database)    │
                  │                 │
                  │ - admins        │
                  │ - services      │
                  │ - products      │
                  │ - testimonials  │
                  │ - requests      │
                  │ - invoices      │
                  │ - customers     │
                  └─────────────────┘
```

---

## 🚀 Data Flow Examples

### 1️⃣ Customer Submits Service Request

```
Website (index.html)
    ↓ (User fills form)
validation.js (Validates input)
    ↓
api.js (POST /api/service-request)
    ↓
backend/routes.py (submit_service_request)
    ↓
models.py (ServiceRequest created)
    ↓
whatsapp.py (Send confirmation)
    ↓
Database (Saved to service_requests table)
    ↓
Response to user ("Request submitted!")
```

### 2️⃣ Admin Edits Website Section

```
Admin Dashboard (dashboard.html)
    ↓ (User edits Hero section)
saveHeroSection() function
    ↓
api.js (PUT /api/admin-full/section/hero)
    ↓
backend/admin_routes.py (update_hero_section)
    ↓
models.py (WebsiteContent updated)
    ↓
Database (Saved to website_content table)
    ↓
Response ("Section saved!")
    ↓
Preview shows updated website
```

### 3️⃣ Staff Creates Invoice (Desktop Software)

```
Desktop App (invoice_view.py)
    ↓ (User enters invoice details)
invoice_controller.py (validate & process)
    ↓
pdf_invoice_generator.py (Generate PDF)
    ↓
database/models.py (Save invoice)
    ↓
MySQL Database (invoices table)
    ↓
whatsapp_helper.py (Send to customer)
    ↓
PDF saved to invoices_pdf/ folder
```

---

## 📊 Database Schema

### Website Database (ac_service_billing)
```sql
admins                  # Admin users
service_requests        # Customer service requests
contact_messages        # Contact form submissions
services                # AC services offered
products                # AC products (Buy/Rent)
testimonials            # Customer reviews
gallery_images          # Photo gallery
website_content         # Editable content (NEW)
website_settings        # Site settings (NEW)
```

### Software Database (ac_service_billing)
```sql
customers               # Customer database
invoices                # Invoice records
invoice_items           # Invoice line items
amc_contracts           # AMC contracts
technicians             # Technician details
service_requests        # Service requests
users                   # Software users
settings                # App settings
```

---

## 🎯 Key Features by Component

### Frontend (Website)
- ✅ Modern, responsive design
- ✅ Animated particles & blobs
- ✅ Dynamic section loading
- ✅ Form validation
- ✅ WhatsApp integration
- ✅ Admin panel for editing

### Backend (API)
- ✅ RESTful API
- ✅ JWT/Session auth
- ✅ Rate limiting
- ✅ CORS protection
- ✅ Input validation
- ✅ Security headers
- ✅ WhatsApp notifications

### Software (Desktop)
- ✅ Professional Qt GUI
- ✅ Invoice generation
- ✅ PDF creation
- ✅ Customer management
- ✅ AMC tracking
- ✅ Technician management
- ✅ Dashboard analytics
- ✅ Auto backup

---

## 📝 Quick Reference

### Start Backend
```bash
cd backend
python main.py
```

### Open Admin Panel
```
frontend/admin/dashboard.html
```

### Start Desktop Software
```bash
cd "software for ai creater - Copy"
python main.py
```

### Database Setup
```bash
cd backend
python setup_admin_db.py
```

---

## 🔐 Default Credentials

### Admin Panel
- Username: `admin`
- Password: `admin123`

### Database
- Host: `localhost`
- User: `root`
- Password: `Akash@9918`
- Database: `ac_service_billing`

---

**Yeh tumhara complete project structure hai!** 🎉

Har file ka purpose aur connection clear hai ab!
