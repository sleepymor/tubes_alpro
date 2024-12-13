from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QWidget, QPushButton, QLineEdit, QFormLayout, QDialog, QComboBox,
    QCheckBox, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
import mysql.connector as mc
import os
import shutil
import sys


# Database Connection
def get_db_connection():
    return mc.connect(
        host="localhost",
        user="root",
        password="",
        database="apv"
    )


# Fetch Regions
def get_regions(cursor):
    cursor.execute("SELECT ID, Region FROM region")
    return cursor.fetchall()


# Fetch Scales
def get_scales(cursor):
    cursor.execute("SELECT ID, Scale FROM scale")
    return cursor.fetchall()


# Add Vendor Dialog
class AddRecordDialog(QDialog):
    def __init__(self, regions, scales, data=None):
        super().__init__()
        self.setWindowTitle("Add Vendor" if not data else "Update Vendor")
        self.setMinimumWidth(400)

        self.values = {}
        self.logo_path = ""

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Input Fields
        self.name_input = QLineEdit(data.get("Name") if data else "")
        self.number_input = QLineEdit(data.get("Number") if data else "")
        self.website_input = QLineEdit(data.get("Website") if data else "")
        self.address_input = QLineEdit(data.get("Address") if data else "")

        # Region Dropdown
        self.region_combo = QComboBox()
        for region_id, region_name in regions:
            self.region_combo.addItem(region_name, region_id)
        if data:
            self.region_combo.setCurrentText(data.get("Region"))

        # Scales Checkboxes
        self.scale_checkboxes = []
        scale_layout = QVBoxLayout()  # Create a layout to hold the checkboxes
        for scale_id, scale_name in scales:
            checkbox = QCheckBox(scale_name)
            checkbox.setProperty("scale_id", scale_id)
            self.scale_checkboxes.append(checkbox)
            scale_layout.addWidget(checkbox)  # Add each checkbox to the layout

        scales_widget = QWidget()
        scales_widget.setLayout(scale_layout)  # Set the layout to a widget

        # Add to form
        form_layout.addRow("Scales:", scales_widget)

        # Logo Upload
        self.logo_input = QLineEdit(data.get("Logo") if data else "")
        self.logo_input.setPlaceholderText("Select logo...")
        self.logo_input.setReadOnly(True)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_logo)

        # Price Range
        self.min_price_input = QLineEdit(str(data.get("MinPrice") if data else ""))
        self.max_price_input = QLineEdit(str(data.get("MaxPrice") if data else ""))

        # Add Fields to Form
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Contact Number:", self.number_input)
        form_layout.addRow("Website:", self.website_input)
        form_layout.addRow("Address:", self.address_input)
        form_layout.addRow("Region:", self.region_combo)
        form_layout.addRow("Scales:", QWidget(layout=QVBoxLayout(*self.scale_checkboxes)))
        form_layout.addRow("Logo:", self.logo_input)
        form_layout.addRow("", browse_button)
        form_layout.addRow("Min Price:", self.min_price_input)
        form_layout.addRow("Max Price:", self.max_price_input)

        layout.addLayout(form_layout)

        # Save Button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def browse_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.logo_input.setText(file_path)
            self.logo_path = file_path

    def save_data(self):
        try:
            # Validation
            if not self.name_input.text():
                raise ValueError("Name is required.")
            if not self.number_input.text():
                raise ValueError("Contact Number is required.")
            min_price = int(self.min_price_input.text())
            max_price = int(self.max_price_input.text())
            if min_price < 500_000 or max_price > 1_000_000_000:
                raise ValueError("Prices must be between 500k and 1B!")

            # Save Logo
            if self.logo_path:
                os.makedirs("./vendor_logo/", exist_ok=True)
                target_path = os.path.join("./vendor_logo/", os.path.basename(self.logo_path))
                if self.logo_path != target_path:
                    shutil.copy(self.logo_path, target_path)

                self.values["Logo"] = target_path

            # Collect Scale IDs
            selected_scales = [
                checkbox.property("scale_id")
                for checkbox in self.scale_checkboxes
                if checkbox.isChecked()
            ]
            if not selected_scales:
                raise ValueError("At least one scale must be selected.")

            # Collect Other Data
            self.values.update({
                "Name": self.name_input.text(),
                "Number": self.number_input.text(),
                "Website": self.website_input.text(),
                "Address": self.address_input.text(),
                "Region": self.region_combo.currentData(),
                "Scales": selected_scales,
                "MinPrice": min_price,
                "MaxPrice": max_price,
            })
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


# Admin Dashboard
class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 1000, 600)

        self.connection = get_db_connection()
        self.cursor = self.connection.cursor()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        load_button = QPushButton("Load Vendors")
        load_button.clicked.connect(self.display_vendors)
        add_button = QPushButton("Add Vendor")
        add_button.clicked.connect(self.add_vendor)
        button_layout.addWidget(load_button)
        button_layout.addWidget(add_button)

        layout.addLayout(button_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def display_vendors(self):
        query = """
        SELECT v.ID, v.Name, v.Number, v.Website, v.Logo, v.Address,
               r.Region, v.MinPrice, v.MaxPrice,
               GROUP_CONCAT(s.Scale SEPARATOR ', ') AS Scales
        FROM vendor v
        JOIN region r ON v.RegionID = r.ID
        LEFT JOIN vendorscale vs ON v.ID = vs.VendorID
        LEFT JOIN scale s ON vs.ScaleID = s.ID
        GROUP BY v.ID;
        """
        self.cursor.execute(query)
        vendors = self.cursor.fetchall()

        self.table.setRowCount(0)
        self.table.setColumnCount(len(vendors[0]))
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Number", "Website", "Logo", "Address",
            "Region", "MinPrice", "MaxPrice", "Scales"
        ])

        for row_idx, vendor in enumerate(vendors):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(vendor):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def add_vendor(self):
        regions = get_regions(self.cursor)
        scales = get_scales(self.cursor)
        dialog = AddRecordDialog(regions, scales)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.values
            try:
                self.cursor.execute(
                    "INSERT INTO vendor (Name, Number, Website, Logo, Address, MinPrice, MaxPrice, RegionID) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (data["Name"], data["Number"], data["Website"], data["Logo"],
                     data["Address"], data["MinPrice"], data["MaxPrice"], data["Region"])
                )
                vendor_id = self.cursor.lastrowid
                for scale_id in data["Scales"]:
                    self.cursor.execute(
                        "INSERT INTO vendorscale (VendorID, ScaleID) VALUES (%s, %s)",
                        (vendor_id, scale_id)
                    )
                self.connection.commit()
                QMessageBox.information(self, "Success", "Vendor added successfully!")
                self.display_vendors()
            except mc.Error as err:
                QMessageBox.critical(self, "Error", f"Database error: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec_())
