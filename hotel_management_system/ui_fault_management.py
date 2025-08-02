import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QFormLayout,
                             QLineEdit, QComboBox, QTextEdit, QLabel, QMessageBox,
                             QHeaderView, QDialogButtonBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime
from database import HotelDatabase

class FaultDetailsDialog(QDialog):
    def __init__(self, fault_data, parent=None):
        super().__init__(parent)
        self.fault_data = fault_data
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Arıza Detayları")
        self.setFixedSize(400, 300)
        
        layout = QFormLayout()
        
        # Create read-only fields
        date_label = QLabel(self.fault_data[1])  # date
        room_label = QLabel(self.fault_data[2])  # room_number
        reporter_label = QLabel(self.fault_data[3])  # reporter
        description_label = QLabel(self.fault_data[4])  # fault_description
        description_label.setWordWrap(True)
        status_label = QLabel(self.fault_data[5])  # fault_status
        
        # Style the status label based on status
        if self.fault_data[5] == "Bekleniyor":
            status_label.setStyleSheet("color: orange; font-weight: bold;")
        elif self.fault_data[5] == "Çözüldü":
            status_label.setStyleSheet("color: green; font-weight: bold;")
        elif self.fault_data[5] == "Çözülemedi":
            status_label.setStyleSheet("color: red; font-weight: bold;")
        
        layout.addRow("Tarih:", date_label)
        layout.addRow("Oda Numarası:", room_label)
        layout.addRow("Bildiren:", reporter_label)
        layout.addRow("Arıza Açıklaması:", description_label)
        layout.addRow("Durum:", status_label)
        
        # Add status update section
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Bekleniyor", "Çözüldü", "Çözülemedi"])
        self.status_combo.setCurrentText(self.fault_data[5])
        layout.addRow("Durumu Güncelle:", self.status_combo)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.update_status)
        button_box.rejected.connect(self.reject)
        
        layout.addRow(button_box)
        self.setLayout(layout)
    
    def update_status(self):
        new_status = self.status_combo.currentText()
        if new_status != self.fault_data[5]:
            db = HotelDatabase()
            if db.update_fault_status(self.fault_data[0], new_status):
                QMessageBox.information(self, "Başarılı", "Arıza durumu güncellendi!")
                self.accept()
            else:
                QMessageBox.warning(self, "Hata", "Arıza durumu güncellenemedi!")
        else:
            self.accept()

class AddFaultDialog(QDialog):
    fault_added = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Yeni Arıza Bildir")
        self.setFixedSize(400, 350)
        
        layout = QFormLayout()
        
        # Date field (auto-filled with today)
        self.date_edit = QLineEdit()
        self.date_edit.setText(datetime.now().strftime('%Y-%m-%d'))
        self.date_edit.setReadOnly(True)
        
        # Room number
        self.room_edit = QLineEdit()
        self.room_edit.setPlaceholderText("Örn: 101, 205, vs.")
        
        # Reporter
        self.reporter_combo = QComboBox()
        self.reporter_combo.addItems(["F/O", "HK", "F&B", "Animasyon", "Diğer"])
        
        # Fault description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Arıza detaylarını buraya yazın...")
        self.description_edit.setMaximumHeight(100)
        
        # Status (default to waiting)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Bekleniyor", "Çözüldü", "Çözülemedi"])
        self.status_combo.setCurrentText("Bekleniyor")
        
        layout.addRow("Tarih:", self.date_edit)
        layout.addRow("Oda Numarası:", self.room_edit)
        layout.addRow("Bildiren:", self.reporter_combo)
        layout.addRow("Arıza Açıklaması:", self.description_edit)
        layout.addRow("Durum:", self.status_combo)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.add_fault)
        button_box.rejected.connect(self.reject)
        
        layout.addRow(button_box)
        self.setLayout(layout)
    
    def add_fault(self):
        # Validate inputs
        if not self.room_edit.text().strip():
            QMessageBox.warning(self, "Hata", "Oda numarası boş olamaz!")
            return
        
        if not self.description_edit.toPlainText().strip():
            QMessageBox.warning(self, "Hata", "Arıza açıklaması boş olamaz!")
            return
        
        # Add fault to database
        db = HotelDatabase()
        success = db.add_fault(
            self.date_edit.text(),
            self.room_edit.text().strip(),
            self.reporter_combo.currentText(),
            self.description_edit.toPlainText().strip(),
            self.status_combo.currentText()
        )
        
        if success:
            QMessageBox.information(self, "Başarılı", "Arıza başarıyla kaydedildi!")
            self.fault_added.emit()
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Arıza kaydedilemedi!")

class FaultManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = HotelDatabase()
        self.init_ui()
        self.load_pending_faults()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Arıza Yönetim Sistemi")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.report_fault_btn = QPushButton("Arıza Bildir")
        self.report_fault_btn.setStyleSheet("""
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
        self.report_fault_btn.clicked.connect(self.open_add_fault_dialog)
        
        self.all_faults_btn = QPushButton("Tüm Arızalar")
        self.all_faults_btn.setStyleSheet("""
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
        self.all_faults_btn.clicked.connect(self.load_all_faults)
        
        self.pending_faults_btn = QPushButton("Bekleyen Arızalar")
        self.pending_faults_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.pending_faults_btn.clicked.connect(self.load_pending_faults)
        
        button_layout.addWidget(self.report_fault_btn)
        button_layout.addWidget(self.all_faults_btn)
        button_layout.addWidget(self.pending_faults_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Table
        self.fault_table = QTableWidget()
        self.fault_table.setColumnCount(6)
        self.fault_table.setHorizontalHeaderLabels([
            "ID", "Tarih", "Oda No", "Bildiren", "Açıklama", "Durum"
        ])
        
        # Set column widths
        header = self.fault_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Room
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Reporter
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # Description
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Status
        
        # Style the table
        self.fault_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
                alternate-background-color: #f5f5f5;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 8px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
            }
        """)
        
        self.fault_table.setAlternatingRowColors(True)
        self.fault_table.doubleClicked.connect(self.show_fault_details)
        
        layout.addWidget(self.fault_table)
        
        # Status label
        self.status_label = QLabel("Bekleyen arızalar gösteriliyor")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def load_pending_faults(self):
        """Load pending faults into table"""
        faults = self.db.get_pending_faults()
        self.populate_table(faults)
        self.status_label.setText(f"Bekleyen arızalar gösteriliyor ({len(faults)} adet)")
    
    def load_all_faults(self):
        """Load all faults into table"""
        faults = self.db.get_all_faults()
        self.populate_table(faults)
        self.status_label.setText(f"Tüm arızalar gösteriliyor ({len(faults)} adet)")
    
    def populate_table(self, faults):
        """Populate table with fault data"""
        self.fault_table.setRowCount(len(faults))
        
        for row, fault in enumerate(faults):
            for col, data in enumerate(fault):
                item = QTableWidgetItem(str(data))
                
                # Color code status column
                if col == 5:  # Status column
                    if data == "Bekleniyor":
                        item.setBackground(Qt.yellow)
                    elif data == "Çözüldü":
                        item.setBackground(Qt.green)
                    elif data == "Çözülemedi":
                        item.setBackground(Qt.red)
                
                self.fault_table.setItem(row, col, item)
    
    def show_fault_details(self, index):
        """Show fault details dialog"""
        row = index.row()
        fault_id = int(self.fault_table.item(row, 0).text())
        fault_data = self.db.get_fault_by_id(fault_id)
        
        if fault_data:
            dialog = FaultDetailsDialog(fault_data, self)
            if dialog.exec_() == QDialog.Accepted:
                # Refresh the current view
                if "Bekleyen" in self.status_label.text():
                    self.load_pending_faults()
                else:
                    self.load_all_faults()
    
    def open_add_fault_dialog(self):
        """Open add fault dialog"""
        dialog = AddFaultDialog(self)
        dialog.fault_added.connect(self.load_pending_faults)
        dialog.exec_()
