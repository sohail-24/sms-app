# School Management System - Setup Instructions

## Prerequisites

Before running this School Management System on another computer, ensure you have the following installed:

### 1. Python
- **Python 3.8 or higher** (recommended: Python 3.9+)
- Download from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### 2. Git (Optional but recommended)
- Download from: https://git-scm.com/downloads

## Installation Steps

### Step 1: Clone or Copy the Project
```bash
# If using Git:
git clone <repository-url>

# Or simply copy the entire project folder to your computer
```

### Step 2: Navigate to Project Directory
```bash
cd "School Management System_Code/SMS"
```

### Step 3: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Required Libraries
```bash
# Install all dependencies
pip install -r requirements.txt
```

### Step 5: Database Setup
```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user (optional - you can also use the existing admin account)
python manage.py update_admin_credentials
```

### Step 6: Collect Static Files (For Production)
```bash
python manage.py collectstatic
```

### Step 7: Run the Server
```bash
# Development server
python manage.py runserver

# The application will be available at: http://127.0.0.1:8000/
```

## Required Libraries/Dependencies

The following Python packages are required (automatically installed with requirements.txt):

### Core Framework
- **Django 4.2.1** - Main web framework
- **Pillow 10.0.0** - Image processing for user photos

### Document Generation
- **reportlab 4.0.4** - PDF generation for reports
- **openpyxl 3.1.2** - Excel file generation
- **xlsxwriter 3.1.2** - Advanced Excel features

### Production Deployment (Optional)
- **gunicorn 20.1.0** - WSGI server for production
- **whitenoise 6.5.0** - Static file serving

### Development Tools (Optional)
- **django-extensions 3.2.3** - Additional Django utilities
- **python-dotenv 1.0.0** - Environment variable management

## Frontend Dependencies (CDN-based)

The following are loaded from CDNs and don't require installation:

- **Bootstrap 5.3.0** - UI framework
- **Font Awesome 6.0.0** - Icons
- **Chart.js** - Charts and graphs
- **FullCalendar 5.11.3** - Calendar functionality
- **Cropper.js 1.5.13** - Image cropping
- **Google Fonts (Poppins)** - Typography

## System Requirements

### Minimum Requirements:
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 500MB for application + data
- **OS**: Windows 7+, macOS 10.12+, or Linux

### Recommended Requirements:
- **RAM**: 8GB or more
- **Storage**: 1GB+ available space
- **OS**: Windows 10+, macOS 10.15+, or modern Linux distro

## Default Login Credentials

After setup, you can log in with:
- **Username**: `admin`
- **Password**: `admin123`

## Network Configuration

To access from other devices on the network:

1. Find your computer's IP address
2. Update `ALLOWED_HOSTS` in `SMS/settings.py`:
   ```python
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'YOUR_IP_ADDRESS']
   ```
3. Run the server with:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Troubleshooting

### Common Issues:

1. **"django-admin not found"**
   - Ensure Python is in your PATH
   - Activate virtual environment

2. **Database errors**
   - Delete `db.sqlite3` and run migrations again
   - Check file permissions

3. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATIC_URL` settings

4. **Permission errors**
   - Check file/folder permissions
   - Run as administrator if needed

### Getting Help:
- Check Django documentation: https://docs.djangoproject.com/
- Python documentation: https://docs.python.org/

## Development vs Production

### Development:
- Use the built-in Django server: `python manage.py runserver`
- SQLite database (included)
- Debug mode enabled

### Production:
- Use gunicorn or similar WSGI server
- Consider PostgreSQL/MySQL for database
- Set `DEBUG = False` in settings
- Configure proper static file serving

## Database Options

By default, the system uses SQLite (no additional setup required).

For other databases, install the appropriate driver:

### PostgreSQL:
```bash
pip install psycopg2-binary
```

### MySQL:
```bash
pip install mysqlclient
```

Then update the `DATABASES` setting in `SMS/settings.py`.

---

**Note**: This School Management System is designed to work out of the box with minimal configuration. The SQLite database and admin credentials are already set up for immediate use.


