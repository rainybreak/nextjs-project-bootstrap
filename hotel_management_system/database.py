import sqlite3
import os
from datetime import datetime

class HotelDatabase:
    def __init__(self, db_name="hotel.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        """Initialize database and create tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create Faults table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS faults (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    room_number TEXT NOT NULL,
                    reporter TEXT NOT NULL,
                    fault_description TEXT NOT NULL,
                    fault_status TEXT NOT NULL DEFAULT 'Bekleniyor'
                )
            ''')
            
            # Create Shifts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shifts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    working_staff TEXT,
                    on_leave TEXT,
                    cover_color TEXT
                )
            ''')
            
            # Create Special Services table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS special_services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    service_description TEXT NOT NULL,
                    status TEXT DEFAULT 'Beklemede'
                )
            ''')
            
            # Create Menus table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menus (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    food_menu TEXT NOT NULL
                )
            ''')
            
            # Create Cocktail Recipes table (static data)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cocktail_recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    recipe TEXT NOT NULL,
                    ingredients TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            
            # Insert sample cocktail recipes if table is empty
            cursor.execute('SELECT COUNT(*) FROM cocktail_recipes')
            if cursor.fetchone()[0] == 0:
                sample_cocktails = [
                    ("Mojito", "Nane yaprakları, lime, şeker, rom, soda", "10 nane yaprağı, 1/2 lime, 2 tsp şeker, 60ml beyaz rom, soda"),
                    ("Piña Colada", "Ananas suyu, hindistan cevizi kremi, rom", "90ml ananas suyu, 30ml hindistan cevizi kremi, 60ml beyaz rom, buz"),
                    ("Margarita", "Tequila, lime suyu, triple sec", "60ml tequila, 30ml lime suyu, 30ml triple sec, tuz kenarı"),
                    ("Cosmopolitan", "Vodka, cranberry suyu, lime suyu, triple sec", "45ml vodka, 15ml cranberry suyu, 15ml lime suyu, 15ml triple sec")
                ]
                cursor.executemany('INSERT INTO cocktail_recipes (name, recipe, ingredients) VALUES (?, ?, ?)', sample_cocktails)
                conn.commit()
            
            conn.close()
            print("Database initialized successfully")
            
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
    
    # Fault Management Functions
    def get_pending_faults(self):
        """Get all pending faults"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM faults WHERE fault_status = "Bekleniyor" ORDER BY date DESC')
            faults = cursor.fetchall()
            conn.close()
            return faults
        except sqlite3.Error as e:
            print(f"Error getting pending faults: {e}")
            return []
    
    def get_all_faults(self):
        """Get all faults"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM faults ORDER BY date DESC')
            faults = cursor.fetchall()
            conn.close()
            return faults
        except sqlite3.Error as e:
            print(f"Error getting all faults: {e}")
            return []
    
    def add_fault(self, date, room_number, reporter, fault_description, fault_status="Bekleniyor"):
        """Add new fault"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO faults (date, room_number, reporter, fault_description, fault_status)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, room_number, reporter, fault_description, fault_status))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error adding fault: {e}")
            return False
    
    def update_fault_status(self, fault_id, new_status):
        """Update fault status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE faults SET fault_status = ? WHERE id = ?', (new_status, fault_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating fault status: {e}")
            return False
    
    def get_fault_by_id(self, fault_id):
        """Get specific fault by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM faults WHERE id = ?', (fault_id,))
            fault = cursor.fetchone()
            conn.close()
            return fault
        except sqlite3.Error as e:
            print(f"Error getting fault by ID: {e}")
            return None
    
    # Shift Management Functions
    def get_today_shift(self):
        """Get today's shift information"""
        today = datetime.now().strftime('%Y-%m-%d')
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM shifts WHERE date = ?', (today,))
            shift = cursor.fetchone()
            conn.close()
            return shift
        except sqlite3.Error as e:
            print(f"Error getting today's shift: {e}")
            return None
    
    def update_shift(self, date, working_staff, on_leave, cover_color):
        """Update or insert shift information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if shift exists for this date
            cursor.execute('SELECT id FROM shifts WHERE date = ?', (date,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('''
                    UPDATE shifts SET working_staff = ?, on_leave = ?, cover_color = ?
                    WHERE date = ?
                ''', (working_staff, on_leave, cover_color, date))
            else:
                cursor.execute('''
                    INSERT INTO shifts (date, working_staff, on_leave, cover_color)
                    VALUES (?, ?, ?, ?)
                ''', (date, working_staff, on_leave, cover_color))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating shift: {e}")
            return False
    
    # Special Services Functions
    def get_today_special_services(self):
        """Get today's special services"""
        today = datetime.now().strftime('%Y-%m-%d')
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM special_services WHERE date = ? ORDER BY id DESC', (today,))
            services = cursor.fetchall()
            conn.close()
            return services
        except sqlite3.Error as e:
            print(f"Error getting today's special services: {e}")
            return []
    
    def add_special_service(self, date, service_description, status="Beklemede"):
        """Add special service request"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO special_services (date, service_description, status)
                VALUES (?, ?, ?)
            ''', (date, service_description, status))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error adding special service: {e}")
            return False
    
    # Menu Management Functions
    def get_today_menu(self):
        """Get today's food menu"""
        today = datetime.now().strftime('%Y-%m-%d')
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM menus WHERE date = ?', (today,))
            menu = cursor.fetchone()
            conn.close()
            return menu
        except sqlite3.Error as e:
            print(f"Error getting today's menu: {e}")
            return None
    
    def update_menu(self, date, food_menu):
        """Update or insert daily menu"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Check if menu exists for this date
            cursor.execute('SELECT id FROM menus WHERE date = ?', (date,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute('UPDATE menus SET food_menu = ? WHERE date = ?', (food_menu, date))
            else:
                cursor.execute('INSERT INTO menus (date, food_menu) VALUES (?, ?)', (date, food_menu))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating menu: {e}")
            return False
    
    def get_cocktail_recipes(self):
        """Get all cocktail recipes"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cocktail_recipes ORDER BY name')
            recipes = cursor.fetchall()
            conn.close()
            return recipes
        except sqlite3.Error as e:
            print(f"Error getting cocktail recipes: {e}")
            return []
