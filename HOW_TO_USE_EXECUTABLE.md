# 🚀 Workshop Inventory Management System - Executable Version

## ✅ **Your .exe file is ready!**

**File Location:** `dist/WorkshopInventory`

## 📖 **How to Use Your Executable**

### **Option 1: Double-Click to Run** (Easiest)
1. Navigate to the `dist` folder
2. **Double-click** on `WorkshopInventory`
3. A terminal window will open showing:
   ```
   🏭 WORKSHOP INVENTORY MANAGEMENT SYSTEM
   ====================================================
   Starting the application...
   📊 Initializing database...
   ✅ Database ready!
   📡 Using default port 5000
   🚀 Starting web server on http://localhost:5000
   🌐 Browser will open automatically...
   
   ====================================================
   📝 DEFAULT LOGIN CREDENTIALS:
      Username: admin
      Password: admin123
   ====================================================
   ```
4. Your web browser will **automatically open** to the application
5. **Login** with the default credentials shown above

### **Option 2: Run from Terminal**
1. Open a terminal
2. Navigate to the project folder:
   ```bash
   cd /path/to/your/workshop-inventory
   ```
3. Run the executable:
   ```bash
   ./dist/WorkshopInventory
   ```

## 🌐 **Accessing the Application**

- **URL:** http://localhost:5000
- **Username:** admin
- **Password:** admin123

## 🎯 **What Happens When You Run It:**

1. ✅ **Database Creation** - Automatically creates the SQLite database
2. ✅ **Server Start** - Starts the web server
3. ✅ **Browser Launch** - Opens your default web browser
4. ✅ **Ready to Use** - Login and start managing your inventory!

## 📁 **Important Files Created:**

- `inventory.db` - Your database file (keep this safe!)
- Log files and temporary files as needed

## 🛑 **How to Stop the Application:**

- **In the terminal window:** Press `Ctrl+C`
- **Close the terminal window** where it's running

## 🔒 **Security Note:**

**IMPORTANT:** Change the default password (admin123) immediately after first login!
- Go to **Settings** → **User Management** → **Change Password**

## 📋 **Features Available:**

- ✅ **Home Dashboard** - Overview and quick access
- ✅ **Stock Entry** - Add new items with auto-fill
- ✅ **Stock Release** - Release items for projects
- ✅ **Stock Check** - Search and view inventory
- ✅ **Notifications** - Low stock alerts
- ✅ **Activities** - System activity log
- ✅ **Settings** - User management (Admin only)
- ✅ **Excel Export** - Export data for backup

## 🚨 **Troubleshooting:**

### **If the browser doesn't open automatically:**
- Manually open your browser
- Go to: `http://localhost:5000`

### **If you see "Port already in use":**
- The system will automatically find another port
- Check the terminal for the actual URL

### **If you can't login:**
- Make sure you're using: Username: `admin`, Password: `admin123`
- Check that caps lock is off

### **If the application won't start:**
- Make sure no other instances are running
- Check that port 5000 isn't being used by another application

## 💾 **Backup Your Data:**

- **Database File:** Copy `inventory.db` to a safe location
- **Excel Export:** Use the export features within the application

## 🎉 **You're All Set!**

Your Workshop Inventory Management System is now ready to use as a standalone executable. No need to install Python or any dependencies - everything is included!

**Happy Inventory Managing!** 🏭📦