# Workshop Inventory Management - Windows Executable Guide

## 🎯 Quick Start (2 Minutes)

### Method 1: Using Batch File (Recommended)
1. **Download all files** to your Windows computer
2. **Double-click** `create_windows_exe.bat`
3. **Wait** for the build to complete
4. **Find your executable** in the `dist` folder as `Workshop_Inventory_Management.exe`

### Method 2: Using PowerShell
1. **Right-click** on `create_windows_exe.ps1`
2. **Select** "Run with PowerShell"
3. **Follow the prompts**

---

## 📋 Prerequisites

- **Python 3.7+** installed on Windows
- **Internet connection** for downloading packages
- **Administrator privileges** may be required for some installations

### Installing Python (if not installed)
1. Download Python from [python.org](https://www.python.org/downloads/)
2. **Important:** Check "Add Python to PATH" during installation
3. Restart your computer after installation

---

## 🔧 Manual Build Process

If the automatic scripts don't work, follow these steps manually:

### Step 1: Install Dependencies
```cmd
python -m pip install --upgrade pip
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Werkzeug==2.3.7 openpyxl==3.1.2 Pillow==10.0.1 python-dotenv==1.0.0 pyinstaller
```

### Step 2: Build Executable
```cmd
pyinstaller --onefile --windowed --name "Workshop_Inventory_Management" --icon=static/favicon.ico --add-data "templates;templates" --add-data "static;static" --hidden-import=openpyxl --hidden-import=PIL --hidden-import=sqlite3 launcher.py
```

### Step 3: Find Your Executable
- Look in the `dist` folder
- File name: `Workshop_Inventory_Management.exe`
- Size: Approximately 20-25 MB

---

## 🚀 Running the Application

### First Run
1. **Double-click** `Workshop_Inventory_Management.exe`
2. **Wait** for the application to start (may take 10-15 seconds)
3. **Browser** will open automatically
4. **Login** with default credentials:
   - Username: `admin`
   - Password: `admin123`

### Features Available
- ✅ **Auto-fill functionality** when entering model numbers
- ✅ **Multi-category inventory management**
- ✅ **User authentication** with roles
- ✅ **Excel export** capabilities
- ✅ **Real-time stock tracking**
- ✅ **Activity logging**
- ✅ **Low stock alerts**

---

## 📁 File Structure Required

Make sure these files are in the same folder before building:
```
Workshop_Inventory_Management/
├── launcher.py
├── app.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── stock_release.html
│   ├── stock_entry.html
│   ├── stock_check.html
│   ├── notifications.html
│   ├── activities.html
│   └── settings.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── favicon.ico
├── create_windows_exe.bat
├── create_windows_exe.ps1
└── requirements.txt
```

---

## 🔧 Troubleshooting

### Common Issues

#### "Python is not recognized"
- **Solution:** Reinstall Python and check "Add Python to PATH"
- **Alternative:** Use full Python path: `C:\Python39\python.exe`

#### "pip is not recognized"
- **Solution:** Use `python -m pip` instead of just `pip`

#### Build fails with "module not found"
- **Solution:** Install missing modules manually:
  ```cmd
  pip install [module-name]
  ```

#### Executable doesn't start
- **Check:** Windows Defender or antivirus isn't blocking it
- **Solution:** Add exception in antivirus software

#### Browser doesn't open automatically
- **Solution:** Manually open browser and go to `http://localhost:5000`

### Performance Tips
- **First run** may be slow (10-15 seconds)
- **Subsequent runs** will be faster
- **Close other applications** during build process
- **Use SSD** for better performance

---

## 🛡️ Security Notes

- **Change default password** immediately after first login
- **Backup database** regularly (SQLite file created automatically)
- **Keep executable** in secure location
- **Don't share executable** with default credentials

---

## 📞 Support

If you encounter issues:
1. **Check** this guide thoroughly
2. **Verify** all files are present
3. **Ensure** Python is properly installed
4. **Try** running commands manually
5. **Check** Windows compatibility (Windows 10+ recommended)

---

## 🎉 Success Indicators

✅ **Build successful** when you see:
- "Building EXE completed successfully"
- File appears in `dist` folder
- File size is 20-25 MB

✅ **Application working** when you see:
- Console window appears briefly
- Browser opens automatically
- Login page loads correctly
- Dashboard shows after login

---

*Workshop Inventory Management System - Windows Executable v1.0*