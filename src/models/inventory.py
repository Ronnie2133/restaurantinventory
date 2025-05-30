from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    items = db.relationship('InventoryItem', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(20), nullable=False)
    threshold = db.Column(db.Integer, default=5)  # Threshold for low stock alert
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    is_low_stock = db.Column(db.Boolean, default=False)
    is_out_of_stock = db.Column(db.Boolean, default=False)
    last_checked = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<InventoryItem {self.name}>'

class Manager(db.Model):
    __tablename__ = 'managers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Manager {self.name}>'

class InventoryCheck(db.Model):
    __tablename__ = 'inventory_checks'
    
    id = db.Column(db.Integer, primary_key=True)
    check_date = db.Column(db.DateTime, nullable=False)
    checked_by = db.Column(db.String(100))
    notes = db.Column(db.Text)
    notification_sent = db.Column(db.Boolean, default=False)
    
    items = db.relationship('CheckedItem', backref='inventory_check', lazy=True)
    
    def __repr__(self):
        return f'<InventoryCheck {self.check_date}>'

class CheckedItem(db.Model):
    __tablename__ = 'checked_items'
    
    id = db.Column(db.Integer, primary_key=True)
    inventory_check_id = db.Column(db.Integer, db.ForeignKey('inventory_checks.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    is_low_stock = db.Column(db.Boolean, default=False)
    is_out_of_stock = db.Column(db.Boolean, default=False)
    
    item = db.relationship('InventoryItem')
    
    def __repr__(self):
        return f'<CheckedItem {self.item.name}>'
