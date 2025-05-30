from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from src.models.inventory import db, Category, InventoryItem, Manager, InventoryCheck, CheckedItem

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('inventory/index.html', categories=categories)

@inventory_bp.route('/items')
def items():
    category_id = request.args.get('category_id', type=int)
    if category_id:
        items = InventoryItem.query.filter_by(category_id=category_id).all()
        category = Category.query.get_or_404(category_id)
        return render_template('inventory/items.html', items=items, category=category)
    else:
        items = InventoryItem.query.all()
        return render_template('inventory/items.html', items=items, category=None)

@inventory_bp.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        # Create a new inventory check
        new_check = InventoryCheck(
            check_date=datetime.now(),
            checked_by=request.form.get('checked_by', 'Staff'),
            notes=request.form.get('notes', '')
        )
        db.session.add(new_check)
        db.session.flush()  # Get the ID without committing
        
        # Process checked items
        for key, value in request.form.items():
            if key.startswith('item_'):
                item_id = int(key.split('_')[1])
                status = value
                
                checked_item = CheckedItem(
                    inventory_check_id=new_check.id,
                    item_id=item_id,
                    is_low_stock=(status == 'low'),
                    is_out_of_stock=(status == 'out')
                )
                db.session.add(checked_item)
                
                # Update the item status in inventory
                item = InventoryItem.query.get(item_id)
                if item:
                    item.is_low_stock = (status == 'low')
                    item.is_out_of_stock = (status == 'out')
                    item.last_checked = datetime.now()
        
        db.session.commit()
        
        # Redirect to send notification
        return redirect(url_for('inventory.send_notification', check_id=new_check.id))
    
    # GET request - show the check form
    categories = Category.query.all()
    return render_template('inventory/check.html', categories=categories)

@inventory_bp.route('/send_notification/<int:check_id>')
def send_notification(check_id):
    check = InventoryCheck.query.get_or_404(check_id)
    
    # If notification already sent, just show the result
    if check.notification_sent:
        return render_template('inventory/notification_sent.html', check=check)
    
    # Get all low stock and out of stock items from this check
    low_stock_items = []
    out_of_stock_items = []
    
    for checked_item in check.items:
        item = checked_item.item
        if checked_item.is_low_stock:
            low_stock_items.append(item)
        if checked_item.is_out_of_stock:
            out_of_stock_items.append(item)
    
    # Get active managers
    managers = Manager.query.filter_by(is_active=True).all()
    
    # Prepare for sending notification
    return render_template(
        'inventory/confirm_notification.html',
        check=check,
        low_stock_items=low_stock_items,
        out_of_stock_items=out_of_stock_items,
        managers=managers
    )

@inventory_bp.route('/send_sms/<int:check_id>', methods=['POST'])
def send_sms(check_id):
    from src.utils.sms import send_inventory_notification
    
    check = InventoryCheck.query.get_or_404(check_id)
    
    # Get manager IDs from form
    manager_ids = request.form.getlist('managers')
    managers = Manager.query.filter(Manager.id.in_(manager_ids)).all()
    
    if not managers:
        flash('Please select at least one manager to notify', 'error')
        return redirect(url_for('inventory.send_notification', check_id=check_id))
    
    # Get items that need attention
    low_stock_items = []
    out_of_stock_items = []
    
    for checked_item in check.items:
        item = checked_item.item
        if checked_item.is_low_stock:
            low_stock_items.append(item)
        if checked_item.is_out_of_stock:
            out_of_stock_items.append(item)
    
    # Send SMS to each manager
    results = []
    for manager in managers:
        result = send_inventory_notification(
            manager.phone,
            low_stock_items,
            out_of_stock_items,
            check.check_date
        )
        results.append({
            'manager': manager.name,
            'success': result['success'],
            'message': result['message']
        })
    
    # Mark notification as sent
    check.notification_sent = True
    db.session.commit()
    
    return render_template('inventory/notification_results.html', results=results, check=check)

@inventory_bp.route('/managers', methods=['GET', 'POST'])
def managers():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        
        if name and phone:
            manager = Manager(name=name, phone=phone)
            db.session.add(manager)
            db.session.commit()
            flash('Manager added successfully', 'success')
        else:
            flash('Name and phone are required', 'error')
            
    managers = Manager.query.all()
    return render_template('inventory/managers.html', managers=managers)

@inventory_bp.route('/managers/toggle/<int:manager_id>')
def toggle_manager(manager_id):
    manager = Manager.query.get_or_404(manager_id)
    manager.is_active = not manager.is_active
    db.session.commit()
    return redirect(url_for('inventory.managers'))

@inventory_bp.route('/managers/delete/<int:manager_id>')
def delete_manager(manager_id):
    manager = Manager.query.get_or_404(manager_id)
    db.session.delete(manager)
    db.session.commit()
    flash('Manager deleted successfully', 'success')
    return redirect(url_for('inventory.managers'))

@inventory_bp.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        name = request.form.get('name')
        
        if name:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully', 'success')
        else:
            flash('Category name is required', 'error')
            
    categories = Category.query.all()
    return render_template('inventory/categories.html', categories=categories)

@inventory_bp.route('/items/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity', type=int)
        unit = request.form.get('unit')
        threshold = request.form.get('threshold', type=int)
        category_id = request.form.get('category_id', type=int)
        
        if name and unit and category_id:
            item = InventoryItem(
                name=name,
                quantity=quantity,
                unit=unit,
                threshold=threshold,
                category_id=category_id
            )
            db.session.add(item)
            db.session.commit()
            flash('Item added successfully', 'success')
            return redirect(url_for('inventory.items'))
        else:
            flash('Name, unit and category are required', 'error')
    
    categories = Category.query.all()
    return render_template('inventory/add_item.html', categories=categories)

@inventory_bp.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.quantity = request.form.get('quantity', type=int)
        item.unit = request.form.get('unit')
        item.threshold = request.form.get('threshold', type=int)
        item.category_id = request.form.get('category_id', type=int)
        
        db.session.commit()
        flash('Item updated successfully', 'success')
        return redirect(url_for('inventory.items'))
    
    categories = Category.query.all()
    return render_template('inventory/edit_item.html', item=item, categories=categories)

@inventory_bp.route('/items/delete/<int:item_id>')
def delete_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully', 'success')
    return redirect(url_for('inventory.items'))
