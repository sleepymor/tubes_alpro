import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QPushButton, QComboBox, QCheckBox, QDialog,
    QLabel, QLineEdit, QFormLayout, QHBoxLayout, QWidget,
    QFileDialog, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import mysql.connector


def connect_to_database():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="",  
        database="apv"  
    )


class AddVendorDialog(QDialog):
    def __init__(self, db, refresh_table_callback):
        super().__init__()
        self.setWindowTitle("Add Vendor")
        self.db = db
        self.refresh_table_callback = refresh_table_callback
        self.logo_path = None  # To store the path of the selected or dropped logo

        # Form Layout
        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)

        # Name Input
        self.name_input = QLineEdit()
        self.form_layout.addRow("Name:", self.name_input)

        # Region Dropdown
        self.region_dropdown = QComboBox()
        self.populate_regions()
        self.form_layout.addRow("Region:", self.region_dropdown)

        # Scale Checkboxes
        self.scale_layout = QVBoxLayout()
        self.scale_checkboxes = []
        self.populate_scales()
        self.form_layout.addRow("Scales:", self.scale_layout)

        # Min and Max Price
        self.min_price_input = QLineEdit()
        self.max_price_input = QLineEdit()
        self.form_layout.addRow("Min Price:", self.min_price_input)
        self.form_layout.addRow("Max Price:", self.max_price_input)

        # Website and Number
        self.website_input = QLineEdit()
        self.form_layout.addRow("Website:", self.website_input)

        self.number_input = QLineEdit()
        self.form_layout.addRow("Number:", self.number_input)

        # Address Input
        self.address_input = QLineEdit()
        self.form_layout.addRow("Address:", self.address_input)

        # Logo Drag-and-Drop Area
        self.logo_frame = QLabel("Drag & Drop Logo Here\nor Browse", self)
        self.logo_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.logo_frame.setAlignment(Qt.AlignCenter)
        self.logo_frame.setAcceptDrops(True)
        self.form_layout.addRow("Logo:", self.logo_frame)

        # Browse Button for Logo
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_logo)
        self.form_layout.addWidget(self.browse_button)

        # Add Vendor Button
        self.add_button = QPushButton("Add Vendor")
        self.add_button.clicked.connect(self.add_vendor)
        self.form_layout.addRow(self.add_button)

    def populate_regions(self):
        """Populate the region dropdown with data from the database."""
        cursor = self.db.cursor()
        cursor.execute("SELECT ID, Region FROM region")
        for row in cursor.fetchall():
            self.region_dropdown.addItem(row[1], row[0])

    def populate_scales(self):
        """Populate checkboxes with scale data."""
        cursor = self.db.cursor()
        cursor.execute("SELECT ID, Scale FROM scale")
        for row in cursor.fetchall():
            checkbox = QCheckBox(row[1])
            checkbox.setProperty("ScaleID", row[0])
            self.scale_layout.addWidget(checkbox)
            self.scale_checkboxes.append(checkbox)

    def browse_logo(self):
        """Open a file dialog to select a logo."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.logo_path = file_path
            pixmap = QPixmap(file_path)
            self.logo_frame.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

    def add_vendor(self):
        """Insert a new vendor into the database."""
        name = self.name_input.text()
        region_id = self.region_dropdown.currentData()
        min_price = self.min_price_input.text()
        max_price = self.max_price_input.text()
        website = self.website_input.text()
        number = self.number_input.text()
        address = self.address_input.text()
        scales = [cb.property("ScaleID") for cb in self.scale_checkboxes if cb.isChecked()]

        # Save logo to /vendor_logo/
        logo_filename = None
        if self.logo_path:
            os.makedirs("vendor_logo", exist_ok=True)
            logo_filename = os.path.basename(self.logo_path)
            shutil.copy(self.logo_path, f"vendor_logo/{logo_filename}")

        # Insert vendor data into the database
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO vendor (RegionID, Name, MinPrice, MaxPrice, Website, Number, Address, Logo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (region_id, name, min_price, max_price, website, number, address, logo_filename))
        vendor_id = cursor.lastrowid

        # Insert vendor scales into the database
        for scale_id in scales:
            cursor.execute("INSERT INTO vendorscale (VendorID, ScaleID) VALUES (%s, %s)", (vendor_id, scale_id))

        self.db.commit()
        self.refresh_table_callback()
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Vendor Management")
        self.db = db

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Add Vendor Button
        self.add_vendor_button = QPushButton("Add Vendor")
        self.add_vendor_button.clicked.connect(self.open_add_vendor_dialog)
        self.layout.addWidget(self.add_vendor_button)

        # Vendor Table
        self.vendor_table = QTableWidget()
        self.vendor_table.setColumnCount(6)
        self.vendor_table.setHorizontalHeaderLabels(["Name", "Region", "Min Price", "Max Price", "Website", "Logo"])
        self.layout.addWidget(self.vendor_table)

        self.load_vendors()

    def open_add_vendor_dialog(self):
        dialog = AddVendorDialog(self.db, self.load_vendors)
        dialog.exec_()

    def load_vendors(self):
        """Load vendor data into the table."""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT vendor.Name, region.Region, vendor.MinPrice, vendor.MaxPrice, vendor.Website, vendor.Logo
            FROM vendor
            JOIN region ON vendor.RegionID = region.ID
        """)
        rows = cursor.fetchall()

        self.vendor_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                if col_idx == 5:  # Display logo path as a placeholder
                    item = "vendor_logo/" + item if item else "No Logo"
                self.vendor_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))


def main():
    app = QApplication([])
    db = connect_to_database()

    window = MainWindow(db)
    window.show()

    app.exec_()
    db.close()


if __name__ == "__main__":
    main()
