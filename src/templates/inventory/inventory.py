from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.models.inventory import db, Category, InventoryItem, Manager, InventoryCheck, CheckedItem
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('inventory/index.html', categories=categories)

@inventory_bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('inventory/categories.html', categories=categories)

@inventory_bp.route('/categories', methods=['POST'])
def add_category():
    name = request.form.get('name')
    if name:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
    return redirect(url_for('inventory.categories'))

@inventory_bp.route('/items')
def items():
    category_id = request.args.get('category_id', type=int)
    if category_id:
        category = Category.query.get_or_404(category_id)
        items = InventoryItem.query.filter_by(category_id=category_id).all()
        return render_template('inventory/items.html', items=items, category=category)
    else:
        categories = Category.query.all()
        return render_template('inventory/items.html', categories=categories)

@inventory_bp.route('/items/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity', type=int, default=0)
        unit = request.form.get('unit')
        threshold = request.form.get('threshold', type=int, default=5)
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
            return redirect(url_for('inventory.items', category_id=category_id))
    
    categories = Category.query.all()
    return render_template('inventory/add_item.html', categories=categories)

@inventory_bp.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.quantity = request.form.get('quantity', type=int, default=0)
        item.unit = request.form.get('unit')
        item.threshold = request.form.get('threshold', type=int, default=5)
        item.category_id = request.form.get('category_id', type=int)
        
        db.session.commit()
        return redirect(url_for('inventory.items', category_id=item.category_id))
    
    categories = Category.query.all()
    return render_template('inventory/edit_item.html', item=item, categories=categories)

@inventory_bp.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    category_id = item.category_id
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('inventory.items', category_id=category_id))

@inventory_bp.route('/check')
def check():
    categories = Category.query.all()
    return render_template('inventory/check.html', categories=categories)

@inventory_bp.route('/check/submit', methods=['POST'])
def submit_check():
    data = request.get_json()
    items = data.get('items', [])
    
    if not items:
        return jsonify({'status': 'error', 'message': 'No items provided'}), 400
    
    # Create a new inventory check
    inventory_check = InventoryCheck(
        timestamp=datetime.utcnow(),
        notes=data.get('notes', '')
    )
    db.session.add(inventory_check)
    db.session.flush()  # Get the ID without committing
    
    # Process each checked item
    for item_data in items:
        item_id = item_data.get('id')
        status = item_data.get('status')
        purchase_amount = item_data.get('purchase_amount')
        
        if item_id and status:
            # Update the item's status in the inventory
            item = InventoryItem.query.get(item_id)
            if item:
                item.is_low_stock = (status == 'low')
                item.is_out_of_stock = (status == 'out')
                item.last_checked = datetime.utcnow()
                
                # Create a checked item record
                checked_item = CheckedItem(
                    inventory_check_id=inventory_check.id,
                    item_id=item_id,
                    status=status,
                    purchase_amount=purchase_amount if (status == 'low' or status == 'out') else None
                )
                db.session.add(checked_item)
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'check_id': inventory_check.id,
        'redirect': url_for('inventory.view_submission', check_id=inventory_check.id)
    })

@inventory_bp.route('/managers')
def managers():
    managers = Manager.query.all()
    return render_template('inventory/managers.html', managers=managers)

@inventory_bp.route('/managers', methods=['POST'])
def add_manager():
    name = request.form.get('name')
    phone = request.form.get('phone')
    
    if name and phone:
        manager = Manager(name=name, phone=phone)
        db.session.add(manager)
        db.session.commit()
    
    return redirect(url_for('inventory.managers'))

@inventory_bp.route('/managers/<int:manager_id>/delete', methods=['POST'])
def delete_manager(manager_id):
    manager = Manager.query.get_or_404(manager_id)
    db.session.delete(manager)
    db.session.commit()
    return redirect(url_for('inventory.managers'))

@inventory_bp.route('/submissions')
def submissions():
    # Get all inventory checks, ordered by most recent first
    checks = InventoryCheck.query.order_by(InventoryCheck.timestamp.desc()).all()
    return render_template('inventory/submissions.html', checks=checks)

@inventory_bp.route('/submissions/<int:check_id>')
def view_submission(check_id):
    # Get the specific inventory check
    check = InventoryCheck.query.get_or_404(check_id)
    
    # Get all checked items for this check that are low or out of stock
    checked_items = CheckedItem.query.filter_by(inventory_check_id=check_id).filter(
        CheckedItem.status.in_(['low', 'out'])
    ).all()
    
    return render_template('inventory/view_submission.html', check=check, checked_items=checked_items)
