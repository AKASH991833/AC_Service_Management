# 🎛️ Ansh Air Cool - Complete Admin Panel

## Overview

This admin panel gives you **complete control** over every section of your website. You can edit all content, manage services, products, testimonials, and more - all from a beautiful, easy-to-use dashboard.

## 🚀 Setup Instructions

### 1. Initialize Database

Run the initialization script to create tables and default data:

```bash
cd backend
python init_admin_full.py
```

This will:
- Create all required database tables
- Create a default admin user
- Initialize all website sections with default content
- Create sample services and testimonials

### 2. Start Backend Server

```bash
python main.py
```

The backend will start on `http://localhost:5000`

### 3. Open Admin Dashboard

Open the admin dashboard in your browser:
- **Admin Dashboard**: `http://localhost:5500/frontend/admin/dashboard.html`
- **Default Login**: 
  - Username: `admin`
  - Password: `admin123`

⚠️ **IMPORTANT**: Change the default password after first login!

## 📋 Features

### 1. **Dashboard Overview**
- View statistics (messages, requests, etc.)
- Quick access to all sections
- Real-time data

### 2. **Hero Section Editor**
- Edit main title and subtitle
- Configure CTA button text and phone number
- Upload background image
- Enable/disable video background

### 3. **Services Management**
- Add, edit, delete services
- Set prices, duration, descriptions
- Upload service images
- Activate/deactivate services
- Reorder services

### 4. **Products Management (Buy & Rent)**
- Manage AC products for sale
- Manage AC products for rent
- Set specifications (capacity, type, star rating)
- Upload product images
- Manage pricing and availability
- Add features and descriptions

### 5. **Testimonials Management**
- Add customer reviews
- Set ratings (1-5 stars)
- Add customer photos
- Feature/unfeature testimonials
- Reorder testimonials

### 6. **Features Section**
- Edit section title and subtitle
- Add/remove features
- Configure icons and descriptions

### 7. **Stats Section**
- Edit customer count
- Edit services completed
- Edit years of experience
- Edit technician count

### 8. **Contact Section**
- Update phone numbers
- Update email and WhatsApp
- Edit business hours
- Add Google Maps embed
- Show/hide contact form

### 9. **Footer Section**
- Edit company name and tagline
- Update copyright text
- Add social media links
- Manage quick links

### 10. **JustDial Badge**
- Enable/disable badge
- Set rating and review count
- Upload badge image

### 11. **Site Settings**
- Site title and description (SEO)
- Upload logo and favicon
- Add Google Analytics code
- Configure WhatsApp button

### 12. **Messages & Service Requests**
- View all contact messages
- View all service requests
- Update status
- Track customer communications

## 🎨 How to Use

### Editing a Section

1. **Login** to the admin dashboard
2. **Navigate** to the section you want to edit (sidebar menu)
3. **Edit** the content in the form fields
4. **Click "Save Changes"** to update the website
5. **Click "Preview Website"** to see your changes

### Adding a New Service

1. Go to **Services** section
2. Click **"Add Service"**
3. Enter service name
4. Fill in details (price, description, etc.)
5. Click **Save**

### Adding a New Product

1. Go to **Products (Buy & Rent)** section
2. Select product type (Buy or Rent)
3. Click **"Add Product"**
4. Enter product details
5. Upload product image
6. Click **Save**

### Uploading Images

1. Click the **"Upload Image"** button next to any image field
2. Select an image from your computer
3. The image URL will be automatically filled
4. Save your changes

## 🔐 Security

- Session-based authentication
- Password hashing with bcrypt
- CORS protection
- Rate limiting on API endpoints
- Input validation and sanitization

## 📁 File Structure

```
backend/
├── admin_routes.py          # New comprehensive admin API routes
├── init_admin_full.py       # Database initialization script
├── main.py                  # Flask backend server
├── models.py                # Database models
├── routes.py                # Existing API routes
└── security.py              # Security utilities

frontend/
├── admin/
│   └── dashboard.html       # New complete admin dashboard
├── css/
│   └── admin.css            # Admin panel styles
└── index.html               # Main website
```

## 🛠️ API Endpoints

### Section Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/admin-full/section/hero` | GET, PUT | Hero section |
| `/api/admin-full/section/services` | GET, POST | Services list |
| `/api/admin-full/section/services/<id>` | PUT, DELETE | Single service |
| `/api/admin-full/section/products` | GET, POST | Products list |
| `/api/admin-full/section/products/<id>` | PUT, DELETE | Single product |
| `/api/admin-full/section/testimonials` | GET, POST | Testimonials |
| `/api/admin-full/section/features` | GET, PUT | Features section |
| `/api/admin-full/section/stats` | GET, PUT | Stats section |
| `/api/admin-full/section/contact` | GET, PUT | Contact section |
| `/api/admin-full/section/footer` | GET, PUT | Footer section |
| `/api/admin-full/section/justdial` | GET, PUT | JustDial badge |
| `/api/admin-full/settings/site` | GET, PUT | Site settings |
| `/api/admin-full/upload/image` | POST | Image upload |

## 🎯 Next Steps

### To Connect Admin Panel with Live Website:

1. **Update Frontend to Load Dynamic Data:**
   - Modify `frontend/js/api.js` to fetch data from admin API
   - Update section loaders to use database content

2. **Example: Update Hero Section**
   ```javascript
   // In frontend/js/sections-loader.js
   async function loadHeroSection() {
       const response = await fetch('http://localhost:5000/api/admin-full/section/hero');
       const data = await response.json();
       
       if (data.success) {
           document.querySelector('.hero-title').textContent = data.data.title;
           document.querySelector('.hero-subtitle').textContent = data.data.subtitle;
       }
   }
   ```

3. **Make Website Dynamic:**
   - Replace hardcoded text with API-fetched data
   - Add refresh mechanism to update content
   - Cache data for performance

## 💡 Tips

- **Preview Changes**: Always preview your changes before publishing
- **Backup Database**: Regularly backup your database
- **Test on Mobile**: Check how changes look on mobile devices
- **SEO**: Update site description and keywords for better SEO
- **Images**: Optimize images before uploading for faster load times

## 🐛 Troubleshooting

### Can't Login?
- Make sure backend server is running
- Check if you ran `init_admin_full.py`
- Verify database connection

### Changes Not Showing?
- Click "Preview Website" to refresh
- Clear browser cache
- Check browser console for errors

### Images Not Uploading?
- Check if `uploads` folder exists
- Verify file size (max 5MB)
- Check file format (PNG, JPG, GIF, WEBP)

## 📞 Support

For issues or questions, check the backend logs:
```bash
# View backend logs
tail -f backend.log
```

---

**Made with ❤️ for Ansh Air Cool**
