from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import tempfile

# Optional import for Pillow (image processing)
try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))

class StorageLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    main_category = db.Column(db.String(50), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    model_number = db.Column(db.String(100), nullable=False, unique=True)
    main_category = db.Column(db.String(50), nullable=False)
    sub_category = db.Column(db.String(100), nullable=False)
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=False)
    current_stock = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=10)
    preview_image = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    storage_location = db.relationship('StorageLocation', backref='items')

class StockTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'in' or 'out'
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    invoice_order_no = db.Column(db.String(100), nullable=True)
    project_name = db.Column(db.String(200), nullable=True)
    authorized_person = db.Column(db.String(100), nullable=True)
    receiver = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    item = db.relationship('Item', backref='transactions')
    user = db.relationship('User', backref='transactions')

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='activities')

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
        
        # Create default categories and storage locations
        categories = {
            'Electrical': ['PLC and accessories', 'HMI', 'Sensors', 'VFD', 'Servo drivers', 'Induction motors', 'Servo motors', 'Stepper motors'],
            'Mechanical': ['Bearings', 'Shafts', 'Key bars', 'Thread bars', 'Chains & sprockets', 'Pipes and Fittings'],
            'Pneumatic': ['Cylinders', 'Solenoid valves', 'Fittings', 'Tubes'],
            'Other': []
        }
        
        storage_locations = {
            'Electrical': ['PLC & Accessories', 'Sensors', 'Motors'],
            'Mechanical': ['Rack 1', 'Rack 2', 'Rack 3', 'Rack 4', 'Rack 5', 'Rack 6', 'Rack 7', 'Rack 8'],
            'Pneumatic': ['Pneumatic Rack 1', 'Pneumatic Rack 2', 'Pneumatic Rack 3', 'Pneumatic Rack 4', 'Pneumatic Rack 5'],
            'Other': ['General Storage']
        }
        
        for main_cat, locations in storage_locations.items():
            for location in locations:
                if not StorageLocation.query.filter_by(name=location, main_category=main_cat).first():
                    storage_loc = StorageLocation(name=location, main_category=main_cat)
                    db.session.add(storage_loc)
        
        db.session.commit()

def log_activity(user_id, action):
    activity = ActivityLog(user_id=user_id, action=action)
    db.session.add(activity)
    db.session.commit()

def login_required(f):
    def login_decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    login_decorated_function.__name__ = f.__name__
    return login_decorated_function

def admin_required(f):
    def admin_decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    admin_decorated_function.__name__ = f.__name__
    return admin_decorated_function

# Routes
@app.route('/')
def home():
    # Get recent critical notifications (low stock items)
    low_stock_items = Item.query.filter(Item.current_stock <= Item.low_stock_threshold).limit(5).all()
    recent_activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(5).all()
    
    return render_template('home.html', 
                         low_stock_items=low_stock_items, 
                         recent_activities=recent_activities)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            log_activity(user.id, f'User {username} logged in')
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')
    
    users = User.query.all()
    return render_template('login.html', users=users)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_activity(session['user_id'], f'User {session["username"]} logged out')
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/stock-release', methods=['GET', 'POST'])
@login_required
def stock_release():
    if request.method == 'POST':
        model_number = request.form['model_number']
        quantity = int(request.form['quantity'])
        project_name = request.form['project_name']
        authorized_person = request.form['authorized_person']
        receiver = request.form['receiver']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        item = Item.query.filter_by(model_number=model_number).first()
        
        if not item:
            flash('Item not found!', 'danger')
            return redirect(url_for('stock_release'))
        
        if item.current_stock < quantity:
            flash('Insufficient stock available!', 'danger')
            return redirect(url_for('stock_release'))
        
        # Create transaction
        transaction = StockTransaction(
            item_id=item.id,
            transaction_type='out',
            quantity=quantity,
            date=date,
            project_name=project_name,
            authorized_person=authorized_person,
            receiver=receiver,
            user_id=session['user_id']
        )
        
        # Update stock
        item.current_stock -= quantity
        item.updated_at = datetime.utcnow()
        
        db.session.add(transaction)
        db.session.commit()
        
        log_activity(session['user_id'], f'Released {quantity} units of {item.name} for {project_name}')
        flash('Stock released successfully!', 'success')
        return redirect(url_for('stock_release'))
    
    items = Item.query.all()
    return render_template('stock_release.html', items=items, now=datetime.now())

@app.route('/stock-entry', methods=['GET', 'POST'])
@login_required
def stock_entry():
    if request.method == 'POST':
        model_number = request.form['model_number']
        item_name = request.form['item_name']
        main_category = request.form['main_category']
        sub_category = request.form['sub_category']
        storage_location_id = int(request.form['storage_location_id'])
        quantity = int(request.form['quantity'])
        low_stock_threshold = int(request.form['low_stock_threshold'])
        invoice_order_no = request.form['invoice_order_no']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        # Check if item exists
        item = Item.query.filter_by(model_number=model_number).first()
        
        if item:
            # Update existing item
            item.current_stock += quantity
            item.updated_at = datetime.utcnow()
            action = f'Added {quantity} units to existing item {item.name}'
        else:
            # Create new item
            item = Item(
                name=item_name,
                model_number=model_number,
                main_category=main_category,
                sub_category=sub_category,
                storage_location_id=storage_location_id,
                current_stock=quantity,
                low_stock_threshold=low_stock_threshold
            )
            db.session.add(item)
            db.session.flush()  # To get the item ID
            action = f'Created new item {item_name} with {quantity} units'
        
        # Create transaction
        transaction = StockTransaction(
            item_id=item.id,
            transaction_type='in',
            quantity=quantity,
            date=date,
            invoice_order_no=invoice_order_no,
            user_id=session['user_id']
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        log_activity(session['user_id'], action)
        flash('Stock entry completed successfully!', 'success')
        return redirect(url_for('stock_entry'))
    
    storage_locations = StorageLocation.query.all()
    return render_template('stock_entry.html', storage_locations=storage_locations, now=datetime.now())

@app.route('/stock-check')
def stock_check():
    search_term = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Item.query
    
    if search_term:
        query = query.filter(
            db.or_(
                Item.name.contains(search_term),
                Item.model_number.contains(search_term)
            )
        )
    
    if category:
        query = query.filter(Item.main_category == category)
    
    items = query.all()
    categories = ['Electrical', 'Mechanical', 'Pneumatic', 'Other']
    
    return render_template('stock_check.html', items=items, categories=categories, 
                         search_term=search_term, selected_category=category)

@app.route('/notifications')
def notifications():
    low_stock_items = Item.query.filter(Item.current_stock <= Item.low_stock_threshold).all()
    return render_template('notifications.html', low_stock_items=low_stock_items)

@app.route('/activities')
def activities():
    activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(100).all()
    return render_template('activities.html', activities=activities)

@app.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    if request.method == 'POST':
        action = request.form['action']
        
        if action == 'change_password':
            user_id = int(request.form['user_id'])
            new_password = request.form['new_password']
            
            user = User.query.get(user_id)
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            
            log_activity(session['user_id'], f'Changed password for user {user.username}')
            flash('Password changed successfully!', 'success')
        
        elif action == 'add_user':
            username = request.form['username']
            password = request.form['password']
            is_admin = 'is_admin' in request.form
            
            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'danger')
            else:
                user = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    is_admin=is_admin
                )
                db.session.add(user)
                db.session.commit()
                
                log_activity(session['user_id'], f'Created new user {username}')
                flash('User created successfully!', 'success')
        
        elif action == 'delete_user':
            user_id = int(request.form['user_id'])
            user = User.query.get(user_id)
            
            if user.username == 'admin':
                flash('Cannot delete admin user!', 'danger')
            else:
                db.session.delete(user)
                db.session.commit()
                
                log_activity(session['user_id'], f'Deleted user {user.username}')
                flash('User deleted successfully!', 'success')
    
    users = User.query.all()
    return render_template('settings.html', users=users)

# API Routes
@app.route('/api/item/<model_number>')
def api_get_item(model_number):
    item = Item.query.filter_by(model_number=model_number).first()
    if item:
        return jsonify({
            'name': item.name,
            'main_category': item.main_category,
            'sub_category': item.sub_category,
            'storage_location': item.storage_location.name,
            'storage_location_id': item.storage_location_id,
            'current_stock': item.current_stock,
            'low_stock_threshold': item.low_stock_threshold,
            'preview_image': item.preview_image
        })
    return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items/search')
def api_search_items():
    term = request.args.get('term', '')
    items = Item.query.filter(
        db.or_(
            Item.name.contains(term),
            Item.model_number.contains(term)
        )
    ).limit(10).all()
    
    return jsonify([{
        'model_number': item.model_number,
        'name': item.name,
        'category': item.main_category
    } for item in items])

@app.route('/api/storage-locations/<category>')
def api_get_storage_locations(category):
    locations = StorageLocation.query.filter_by(main_category=category).all()
    return jsonify([{
        'id': loc.id,
        'name': loc.name
    } for loc in locations])

@app.route('/export/<table>')
@login_required
def export_data(table):
    wb = Workbook()
    ws = wb.active
    
    if table == 'items':
        ws.title = 'Items'
        headers = ['Model Number', 'Name', 'Main Category', 'Sub Category', 'Storage Location', 'Current Stock', 'Low Stock Threshold']
        ws.append(headers)
        
        items = Item.query.all()
        for item in items:
            ws.append([
                item.model_number,
                item.name,
                item.main_category,
                item.sub_category,
                item.storage_location.name,
                item.current_stock,
                item.low_stock_threshold
            ])
    
    elif table == 'transactions':
        ws.title = 'Transactions'
        headers = ['Date', 'Item Name', 'Model Number', 'Type', 'Quantity', 'Project/Invoice', 'User']
        ws.append(headers)
        
        transactions = StockTransaction.query.all()
        for trans in transactions:
            ws.append([
                trans.date.strftime('%Y-%m-%d'),
                trans.item.name,
                trans.item.model_number,
                trans.transaction_type.upper(),
                trans.quantity,
                trans.project_name or trans.invoice_order_no,
                trans.user.username
            ])
    
    elif table == 'activities':
        ws.title = 'Activities'
        headers = ['Timestamp', 'User', 'Action']
        ws.append(headers)
        
        activities = ActivityLog.query.all()
        for activity in activities:
            ws.append([
                activity.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                activity.user.username,
                activity.action
            ])
    
    # Style headers
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
    wb.save(temp_file.name)
    temp_file.close()
    
    log_activity(session['user_id'], f'Exported {table} data to Excel')
    
    return send_file(temp_file.name, as_attachment=True, download_name=f'{table}_export.xlsx')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)