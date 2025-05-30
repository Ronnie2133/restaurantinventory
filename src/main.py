import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for
from datetime import datetime
from src.models.inventory import db
from src.routes import inventory_bp

def create_app():
    app = Flask(__name__)
    
    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'restaurant-inventory-secret-key'
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(inventory_bp)
    
    # Create a route to redirect root to inventory
    @app.route('/')
    def index():
        return redirect(url_for('inventory.index'))
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Add initial data if database is empty
        from src.models.inventory import Category, InventoryItem, Manager, CheckedItem, InventoryCheck
        
        # Drop existing tables and recreate to ensure clean data
        if Category.query.count() > 0:
            # Delete all existing data
            db.session.query(CheckedItem).delete()
            db.session.query(InventoryCheck).delete()
            db.session.query(InventoryItem).delete()
            db.session.query(Category).delete()
            db.session.query(Manager).delete()
            db.session.commit()
        
        # Add categories
        storage_room = Category(name='Storage Room')
        prep_area = Category(name='Prep Area')
        freezer = Category(name='Freezer')
        walk_in_cooler = Category(name='Walk In Cooler')
        guest_area = Category(name='Guest Area')
        
        db.session.add_all([storage_room, prep_area, freezer, walk_in_cooler, guest_area])
        db.session.commit()
        
        # Add Storage Room items
        storage_room_items = [
            InventoryItem(name='Roasted Eggplant', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Chickpeas', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Jalapeños', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Banana Peppers', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Chipotle Peppers', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Black Olives', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Mayonnaise', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Mustard', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Vegeta', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Rice', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Egyptian Rice', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Lemon Juice', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Vinegar', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Red Wine Vinegar', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Tahini', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Frying Oil', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Canola Oil', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Bleach', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Fabulouso', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Trash Bags', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Ziplock Large', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
            InventoryItem(name='Ziplock Small', quantity=0, unit='unit', threshold=1, category_id=storage_room.id),
        ]
        
        # Add Prep Area items
        prep_area_items = [
            InventoryItem(name='Paprika', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Salt', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Granulated Garlic', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Granulated Onions', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Black Pepper', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Cumin Powder', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Chopped Onions', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Coriander Powder', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Baking Powder', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Baking Soda', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Flour', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Aluminum Foil Roll', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Food Service Film Wrap', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Disposable Gloves', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
            InventoryItem(name='Oregano', quantity=0, unit='unit', threshold=1, category_id=prep_area.id),
        ]
        
        # Add Freezer items
        freezer_items = [
            InventoryItem(name='Gyro', quantity=0, unit='unit', threshold=1, category_id=freezer.id),
            InventoryItem(name='Fries', quantity=0, unit='unit', threshold=1, category_id=freezer.id),
            InventoryItem(name='Kibbeh', quantity=0, unit='unit', threshold=1, category_id=freezer.id),
            InventoryItem(name='Filet Mignon', quantity=0, unit='unit', threshold=1, category_id=freezer.id),
            InventoryItem(name='Lamb Shank', quantity=0, unit='unit', threshold=1, category_id=freezer.id),
            InventoryItem(name='Lamb Kabob', quantity=0, unit='unit', threshold=1, category_id=freezer.id),
            InventoryItem(name='Lamb Chops', quantity=0, unit='unit', threshold=1, category_id=freezer.id),
        ]
        
        # Add Walk In Cooler items
        walk_in_cooler_items = [
            InventoryItem(name='Chicken Kabob', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Chicken Shawarma', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Beef Kabob', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Lamb Kabob', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Lamb Chops', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Kofta', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Milk', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Heavy Cream', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Garlic', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Falafel', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Grape Leaves', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Mozzarella Cheese', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Feta Cheese', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Salad', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Butter', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Hummus Sauce', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Garlic Sauce', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Tzatziki', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Tomatoes', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Onions', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Cucumber', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Lemons', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Limes', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Lettuce', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
            InventoryItem(name='Red Cabbage', quantity=0, unit='unit', threshold=1, category_id=walk_in_cooler.id),
        ]
        
        # Add Guest Area items
        guest_area_items = [
            InventoryItem(name='Coca Cola', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Coca Cola Diet', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Fanta Orange', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Dr Pepper', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Minute Maid Lemonade', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Sprite', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Schweppes Gold Pineapple', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Schweppes Pomegranate', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Fayrouz Pineapple', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Fayrouz Apple', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Modelo', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Laguintas IPA', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='805', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Pacifico', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Corona Extra', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Baklava', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Utensils', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Coca Cola Cups', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Coca Cola Lids', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Water Cups', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Ketchup', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
            InventoryItem(name='Tobasco', quantity=0, unit='unit', threshold=1, category_id=guest_area.id),
        ]
        
        # Add all items to the database
        all_items = storage_room_items + prep_area_items + freezer_items + walk_in_cooler_items + guest_area_items
        db.session.add_all(all_items)
        
        # Add a sample manager
        manager = Manager(name='Restaurant Manager', phone='+15555555555')
        db.session.add(manager)
        
        db.session.commit()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
