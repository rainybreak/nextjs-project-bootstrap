import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QFormLayout,
                             QLineEdit, QComboBox, QTextEdit, QLabel, QMessageBox,
                             QHeaderView, QDialogButtonBox, QTabWidget, QListWidget,
                             QListWidgetItem, QSplitter, QGroupBox, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from datetime import datetime
from database import HotelDatabase

class ShiftManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = HotelDatabase()
        self.init_ui()
        self.load_shift_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Vardiya Yönetimi")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Today's date
        today_label = QLabel(f"Tarih: {datetime.now().strftime('%d/%m/%Y')}")
        today_label.setFont(QFont("Arial", 12))
        layout.addWidget(today_label)
        
        # Cover color section
        color_group = QGroupBox("Günlük Örtü Rengi")
        color_layout = QVBoxLayout()
        
        self.color_display = QLabel("Renk Seçilmedi")
        self.color_display.setMinimumHeight(50)
        self.color_display.setStyleSheet("""
            QLabel {
                border: 2px solid #ccc;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                background-color: white;
            }
        """)
        
        color_button_layout = QHBoxLayout()
        colors = [
            ("Kırmızı", "#FF0000"),
            ("Mavi", "#0000FF"),
            ("Yeşil", "#00FF00"),
            ("Sarı", "#FFFF00"),
            ("Mor", "#800080"),
            ("Turuncu", "#FFA500")
        ]
        
        for color_name, color_code in colors:
            btn = QPushButton(color_name)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color_code};
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 3px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    opacity: 0.8;
                }}
            """)
            btn.clicked.connect(lambda checked, name=color_name, code=color_code: self.set_cover_color(name, code))
            color_button_layout.addWidget(btn)
        
        color_layout.addWidget(self.color_display)
        color_layout.addLayout(color_button_layout)
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # Staff management section
        staff_group = QGroupBox("Personel Durumu")
        staff_layout = QVBoxLayout()
        
        # Working staff
        working_layout = QHBoxLayout()
        working_layout.addWidget(QLabel("Çalışan Personel:"))
        self.working_staff_edit = QLineEdit()
        self.working_staff_edit.setPlaceholderText("Çalışan personel isimlerini virgülle ayırarak yazın")
        working_layout.addWidget(self.working_staff_edit)
        
        # On leave staff
        leave_layout = QHBoxLayout()
        leave_layout.addWidget(QLabel("İzinli Personel:"))
        self.on_leave_edit = QLineEdit()
        self.on_leave_edit.setPlaceholderText("İzinli personel isimlerini virgülle ayırarak yazın")
        leave_layout.addWidget(self.on_leave_edit)
        
        staff_layout.addLayout(working_layout)
        staff_layout.addLayout(leave_layout)
        
        # Save button
        save_btn = QPushButton("Vardiya Bilgilerini Kaydet")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_shift_data)
        staff_layout.addWidget(save_btn)
        
        staff_group.setLayout(staff_layout)
        layout.addWidget(staff_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def set_cover_color(self, color_name, color_code):
        """Set the cover color"""
        self.color_display.setText(color_name)
        self.color_display.setStyleSheet(f"""
            QLabel {{
                border: 2px solid #ccc;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                background-color: {color_code};
                color: white;
            }}
        """)
        self.current_color = color_name
    
    def load_shift_data(self):
        """Load today's shift data"""
        shift_data = self.db.get_today_shift()
        if shift_data:
            self.working_staff_edit.setText(shift_data[2] or "")
            self.on_leave_edit.setText(shift_data[3] or "")
            if shift_data[4]:
                # Find color code for the saved color name
                color_map = {
                    "Kırmızı": "#FF0000",
                    "Mavi": "#0000FF", 
                    "Yeşil": "#00FF00",
                    "Sarı": "#FFFF00",
                    "Mor": "#800080",
                    "Turuncu": "#FFA500"
                }
                color_code = color_map.get(shift_data[4], "#FFFFFF")
                self.set_cover_color(shift_data[4], color_code)
        else:
            self.current_color = None
    
    def save_shift_data(self):
        """Save shift data to database"""
        today = datetime.now().strftime('%Y-%m-%d')
        working_staff = self.working_staff_edit.text().strip()
        on_leave = self.on_leave_edit.text().strip()
        cover_color = getattr(self, 'current_color', None)
        
        if self.db.update_shift(today, working_staff, on_leave, cover_color):
            QMessageBox.information(self, "Başarılı", "Vardiya bilgileri kaydedildi!")
        else:
            QMessageBox.warning(self, "Hata", "Vardiya bilgileri kaydedilemedi!")

class SpecialServiceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = HotelDatabase()
        self.init_ui()
        self.load_special_services()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Özel Servis Yönetimi")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Today's date
        today_label = QLabel(f"Tarih: {datetime.now().strftime('%d/%m/%Y')}")
        today_label.setFont(QFont("Arial", 12))
        layout.addWidget(today_label)
        
        # Add service button
        add_btn = QPushButton("Yeni Özel Servis Ekle")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        add_btn.clicked.connect(self.add_special_service)
        layout.addWidget(add_btn)
        
        # Services list
        self.services_list = QListWidget()
        self.services_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)
        layout.addWidget(self.services_list)
        
        self.setLayout(layout)
    
    def load_special_services(self):
        """Load today's special services"""
        services = self.db.get_today_special_services()
        self.services_list.clear()
        
        for service in services:
            item_text = f"ID: {service[0]} | {service[2]} | Durum: {service[3]}"
            item = QListWidgetItem(item_text)
            
            # Color code based on status
            if service[3] == "Beklemede":
                item.setBackground(QColor("#FFF3CD"))
            elif service[3] == "Tamamlandı":
                item.setBackground(QColor("#D4EDDA"))
            elif service[3] == "İptal":
                item.setBackground(QColor("#F8D7DA"))
            
            self.services_list.addItem(item)
    
    def add_special_service(self):
        """Add new special service"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Özel Servis")
        dialog.setFixedSize(400, 200)
        
        layout = QFormLayout()
        
        description_edit = QTextEdit()
        description_edit.setPlaceholderText("Özel servis talebini detaylı olarak yazın...")
        description_edit.setMaximumHeight(80)
        
        status_combo = QComboBox()
        status_combo.addItems(["Beklemede", "Tamamlandı", "İptal"])
        
        layout.addRow("Servis Açıklaması:", description_edit)
        layout.addRow("Durum:", status_combo)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(button_box)
        
        dialog.setLayout(layout)
        
        def save_service():
            description = description_edit.toPlainText().strip()
            if not description:
                QMessageBox.warning(dialog, "Hata", "Servis açıklaması boş olamaz!")
                return
            
            today = datetime.now().strftime('%Y-%m-%d')
            if self.db.add_special_service(today, description, status_combo.currentText()):
                QMessageBox.information(dialog, "Başarılı", "Özel servis eklendi!")
                self.load_special_services()
                dialog.accept()
            else:
                QMessageBox.warning(dialog, "Hata", "Özel servis eklenemedi!")
        
        button_box.accepted.connect(save_service)
        button_box.rejected.connect(dialog.reject)
        
        dialog.exec_()

class MenuManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = HotelDatabase()
        self.init_ui()
        self.load_menu_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Menü Yönetimi")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Today's date
        today_label = QLabel(f"Tarih: {datetime.now().strftime('%d/%m/%Y')}")
        today_label.setFont(QFont("Arial", 12))
        layout.addWidget(today_label)
        
        # Splitter for two sections
        splitter = QSplitter(Qt.Horizontal)
        
        # Daily menu section
        daily_group = QGroupBox("Günlük Yemek Menüsü")
        daily_layout = QVBoxLayout()
        
        self.menu_edit = QTextEdit()
        self.menu_edit.setPlaceholderText("""Günlük menüyü buraya yazın:

Örnek:
Çorbalar:
- Mercimek Çorbası
- Tavuk Çorbası

Ana Yemekler:
- Izgara Tavuk
- Köfte
- Balık

Salatalar:
- Çoban Salatası
- Yeşil Salata

Tatlılar:
- Sütlaç
- Baklava""")
        
        save_menu_btn = QPushButton("Menüyü Kaydet")
        save_menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_menu_btn.clicked.connect(self.save_menu)
        
        daily_layout.addWidget(self.menu_edit)
        daily_layout.addWidget(save_menu_btn)
        daily_group.setLayout(daily_layout)
        
        # Cocktail recipes section
        cocktail_group = QGroupBox("Kokteyl Tarifleri (Sabit)")
        cocktail_layout = QVBoxLayout()
        
        # Scroll area for cocktails
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        self.cocktail_list = QListWidget()
        self.cocktail_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #ddd;
                background-color: white;
                margin: 2px;
                border-radius: 3px;
            }
        """)
        
        scroll_layout.addWidget(self.cocktail_list)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        cocktail_layout.addWidget(scroll_area)
        cocktail_group.setLayout(cocktail_layout)
        
        # Add both sections to splitter
        splitter.addWidget(daily_group)
        splitter.addWidget(cocktail_group)
        splitter.setSizes([400, 400])
        
        layout.addWidget(splitter)
        self.setLayout(layout)
    
    def load_menu_data(self):
        """Load menu data"""
        # Load daily menu
        menu_data = self.db.get_today_menu()
        if menu_data:
            self.menu_edit.setPlainText(menu_data[2])
        
        # Load cocktail recipes
        recipes = self.db.get_cocktail_recipes()
        self.cocktail_list.clear()
        
        for recipe in recipes:
            item_text = f"""🍹 {recipe[1]}

📝 Tarif: {recipe[2]}

🥃 Malzemeler: {recipe[3]}"""
            
            item = QListWidgetItem(item_text)
            item.setFont(QFont("Arial", 10))
            self.cocktail_list.addItem(item)
    
    def save_menu(self):
        """Save daily menu"""
        today = datetime.now().strftime('%Y-%m-%d')
        menu_text = self.menu_edit.toPlainText().strip()
        
        if not menu_text:
            QMessageBox.warning(self, "Hata", "Menü boş olamaz!")
            return
        
        if self.db.update_menu(today, menu_text):
            QMessageBox.information(self, "Başarılı", "Günlük menü kaydedildi!")
        else:
            QMessageBox.warning(self, "Hata", "Menü kaydedilemedi!")

class FBManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Main title
        title = QLabel("F&B Yönetim Sistemi")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(title)
        
        # Tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
        """)
        
        # Add tabs
        tab_widget.addTab(ShiftManagementWidget(), "Vardiya Yönetimi")
        tab_widget.addTab(SpecialServiceWidget(), "Özel Servis")
        tab_widget.addTab(MenuManagementWidget(), "Menü Yönetimi")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)
