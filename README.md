# Workshop Inventory Management System

A comprehensive web-based inventory management system designed specifically for workshops. This system helps you manage electrical, mechanical, pneumatic, and other workshop items efficiently with features like auto-fill, low stock notifications, and Excel export capabilities.

## Features

### Core Functionality
- **Multi-category Inventory Management**: Electrical, Mechanical, Pneumatic, and Other categories
- **Auto-fill Technology**: When entering a model number, the system automatically fills related fields
- **Smart Search**: Search by model number, item name, or category
- **Stock Level Monitoring**: Real-time stock tracking with low stock alerts
- **User Authentication**: Multi-user system with admin and regular user roles
- **Excel Export**: Export data to Excel format for backup and analysis
- **Activity Logging**: Complete audit trail of all system activities

### Page Structure
1. **Home Page**: Dashboard with quick access to all functions and critical notifications
2. **Stock Entry**: Add new items or refill existing stock with auto-fill capabilities
3. **Stock Release**: Release items for projects or sales with stock validation
4. **Stock Check**: Search and view inventory with filtering options
5. **Notifications**: View low stock alerts and critical notifications
6. **Activities**: Monitor all system activities and user actions
7. **Settings**: Admin panel for user management and system configuration

### Categories and Storage Locations

**Electrical**
- Subcategories: PLC and accessories, HMI, Sensors, VFD, Servo drivers, Induction motors, Servo motors, Stepper motors
- Storage: PLC & Accessories, Sensors, Motors cupboards

**Mechanical**
- Subcategories: Bearings, Shafts, Key bars, Thread bars, Chains & sprockets, Pipes and Fittings
- Storage: 8 organized racks

**Pneumatic**
- Subcategories: Cylinders, Solenoid valves, Fittings, Tubes
- Storage: 5 dedicated racks

**Other**
- Custom categories and general storage

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   cd /path/to/your/desired/location
   # If you have the files, ensure they're in a directory called 'workshop-inventory'
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - The application will automatically create the database and default admin user

## Default Login Credentials

- **Admin User**: 
  - Username: `admin`
  - Password: `admin123`

**Important**: Change the default password after first login through the Settings page.

## Usage Guide

### First Time Setup

1. **Login** with the default admin credentials
2. **Change the admin password** in Settings
3. **Create additional users** if needed
4. **Add your first items** using the Stock Entry page

### Adding New Items

1. Go to **Stock Entry** page
2. Enter the **Model Number** (this will be unique identifier)
3. Fill in **Item Name**, **Category**, and **Sub-category**
4. Select appropriate **Storage Location**
5. Enter **Quantity** and **Low Stock Threshold**
6. Add **Invoice/Order Number** for tracking
7. Click **Add/Update Stock**

### Auto-fill Feature

When entering a model number that already exists in the system:
- All related fields will automatically populate
- This ensures consistency and saves time
- You can then just update the quantity to add more stock

### Releasing Stock

1. Go to **Stock Release** page
2. Select the **Model Number** from the dropdown
3. Enter the **Quantity** (system prevents over-release)
4. Fill in **Project/Sale Name**, **Authorized Person**, and **Receiver**
5. Click **Release Stock**

### Monitoring Stock

- Use **Stock Check** to search and view all items
- Check **Notifications** for low stock alerts
- Monitor **Activities** to track all system usage
- Set up appropriate **Low Stock Thresholds** for each item

### Data Export

- Export **Items**, **Transactions**, or **Activities** to Excel
- Available from multiple pages for logged-in users
- Useful for backup, analysis, and reporting

## Technical Details

### Database Schema

The system uses SQLite database with the following main tables:
- **Users**: User authentication and roles
- **Items**: Inventory items with categories and stock levels
- **StorageLocations**: Physical storage locations
- **StockTransactions**: All stock movements (in/out)
- **ActivityLog**: System activity tracking

### File Structure

```
workshop-inventory/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Home page
│   ├── login.html        # Login page
│   ├── stock_entry.html  # Stock entry page
│   ├── stock_release.html # Stock release page
│   ├── stock_check.html  # Stock checking page
│   ├── notifications.html # Notifications page
│   ├── activities.html   # Activities page
│   └── settings.html     # Settings page
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   └── images/           # Item images (auto-created)
└── inventory.db          # SQLite database (auto-created)
```

### Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (local storage)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Libraries**: 
  - Flask-SQLAlchemy for database ORM
  - Werkzeug for password hashing
  - openpyxl for Excel export
  - jQuery for frontend interactions

## Security Features

- **Password Hashing**: All passwords are securely hashed
- **Session Management**: Secure session handling
- **Role-based Access**: Admin and user roles with different permissions
- **Input Validation**: Form validation and sanitization
- **Activity Logging**: Complete audit trail

## Customization

### Adding New Categories

1. Login as admin
2. Modify the categories in the `init_db()` function in `app.py`
3. Add corresponding storage locations
4. Restart the application

### Modifying Storage Locations

Storage locations can be modified in the `init_db()` function. The system supports:
- Multiple storage locations per category
- Custom naming for racks, cupboards, etc.
- Easy addition of new storage areas

### Styling Customization

- Modify `static/css/style.css` for visual changes
- The system uses Bootstrap 5 for responsive design
- Custom CSS variables for easy color scheme changes

## Backup and Maintenance

### Database Backup

1. **Automated Export**: Use the Excel export feature regularly
2. **Database File**: Copy the `inventory.db` file for complete backup
3. **Scheduled Backups**: Set up automated copying of the database file

### Maintenance Tasks

- **Regular Password Updates**: Change passwords periodically
- **Clean Old Activities**: Archive old activity logs if needed
- **Update Stock Thresholds**: Adjust low stock levels based on usage patterns
- **Review Categories**: Add new categories as your workshop grows

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure the application has write permissions in the directory
   - Check if `inventory.db` file exists and is accessible

2. **Login Problems**
   - Use default credentials: admin/admin123
   - Check if cookies are enabled in your browser

3. **Auto-fill Not Working**
   - Ensure JavaScript is enabled
   - Check browser console for errors
   - Verify model number exists in database

4. **Export Issues**
   - Ensure you're logged in
   - Check if openpyxl is installed correctly
   - Verify browser allows file downloads

### Performance Optimization

- **Regular Maintenance**: Clean up old activity logs periodically
- **Image Optimization**: Optimize item images for web display
- **Database Indexing**: The system automatically indexes key fields

## Support and Development

### Feature Requests

This system is designed to be extensible. Common enhancement requests:
- Barcode scanning integration
- Email notifications for low stock
- Advanced reporting and analytics
- Mobile app companion
- Multi-location support

### Development Notes

- The system follows Flask best practices
- Database migrations are handled automatically
- All forms include CSRF protection
- Responsive design works on tablets and mobile devices

## License

This project is provided as-is for workshop inventory management purposes. Modify and use according to your needs.

## Version History

- **v1.0**: Initial release with core functionality
- Auto-fill technology for model numbers
- Multi-category inventory management
- User authentication and role management
- Excel export capabilities
- Activity logging and notifications

---

For additional support or questions, refer to the inline help text within the application or check the activity logs for troubleshooting information.
