import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                             QWidget, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

# Import custom modules
from database import HotelDatabase
from ui_fault_management import FaultManagementWidget
from ui_fb_menu import FBManagementWidget

class HotelManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_database()
    
    def init_database(self):
        """Initialize database connection"""
        try:
            self.db = HotelDatabase()
            print("Database initialized successfully")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", 
                               f"Failed to initialize database: {str(e)}")
            sys.exit(1)
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Otel Yönetim Sistemi")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set application icon (optional)
        # self.setWindowIcon(QIcon('hotel_icon.png'))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Application title
        title_label = QLabel("🏨 OTEL YÖNETİM SİSTEMİ")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background-color: #ecf0f1;
                padding: 15px;
                border-radius: 10px;
                margin: 10px;
                border: 2px solid #bdc3c7;
            }
        """)
        layout.addWidget(title_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                background-color: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 12px 25px;
                margin-right: 3px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                min-width: 150px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid white;
                color: #3498db;
            }
            QTabBar::tab:hover {
                background-color: #d5dbdb;
            }
        """)
        
        try:
            # Add Fault Management tab
            fault_widget = FaultManagementWidget()
            self.tab_widget.addTab(fault_widget, "🔧 Teknik Servis")
            
            # Add F&B Management tab
            fb_widget = FBManagementWidget()
            self.tab_widget.addTab(fb_widget, "🍽️ F&B Menüsü")
            
        except Exception as e:
            QMessageBox.critical(self, "UI Error", 
                               f"Failed to initialize UI components: {str(e)}")
            sys.exit(1)
        
        layout.addWidget(self.tab_widget)
        central_widget.setLayout(layout)
        
        # Set window properties
        self.setMinimumSize(1000, 700)
        self.center_window()
        
        # Apply global stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
    
    def center_window(self):
        """Center the window on screen"""
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(self, 'Çıkış', 
                                   'Uygulamadan çıkmak istediğinizden emin misiniz?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    """Main application entry point"""
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Otel Yönetim Sistemi")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Hotel Management Solutions")
    
    # Set application style
    app.setStyle('Fusion')  # Modern look
    
    try:
        # Create and show main window
        window = HotelManagementSystem()
        window.show()
        
        # Start event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        # Show error message if application fails to start
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setWindowTitle("Uygulama Hatası")
        error_msg.setText("Uygulama başlatılamadı!")
        error_msg.setDetailedText(str(e))
        error_msg.exec_()
        sys.exit(1)

if __name__ == '__main__':
    main()
