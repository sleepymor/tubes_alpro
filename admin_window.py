import sys
from database import cursor, mc, db
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QDialog,
    QComboBox,
    QCheckBox,
    QGridLayout,
    QSlider,
)
from PyQt5.QtCore import Qt


class AddRecordDialog(QDialog):
    def __init__(self, regions, scales, data=None, parent=None,):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Record")
        self.values = {}
        self.data = data  # Data for editing

        # Layout for form
        form_layout = QFormLayout()

        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Name")
        form_layout.addRow("Name:", self.name_input)

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Enter Number")
        form_layout.addRow("Number:", self.number_input)

        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("Enter Website")
        form_layout.addRow("Website:", self.website_input)

        self.logo_input = QLineEdit()
        self.logo_input.setPlaceholderText("Enter Logo URL")
        form_layout.addRow("Logo:", self.logo_input)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter Address")
        form_layout.addRow("Address:", self.address_input)

        # Dropdown for Region
        self.region_dropdown = QComboBox()
        self.region_dropdown.addItems(regions)
        form_layout.addRow("Region:", self.region_dropdown)

        # Checkboxes for Scale
        self.scale_checkboxes = []
        scale_layout = QGridLayout()
        for i, scale in enumerate(scales):
            checkbox = QCheckBox(scale)
            self.scale_checkboxes.append(checkbox)
            scale_layout.addWidget(checkbox, i // 3, i % 3)  # 3 checkboxes per row

        scale_widget = QWidget()
        scale_widget.setLayout(scale_layout)
        form_layout.addRow("Scale:", scale_widget)

        # Price Range Sliders (Min and Max)
        self.min_price_slider = QSlider(Qt.Horizontal)
        self.min_price_slider.setMinimum(1)
        self.min_price_slider.setMaximum(10000)
        self.min_price_slider.setValue(100)
        self.min_price_slider.valueChanged.connect(self.update_price_label)

        self.max_price_slider = QSlider(Qt.Horizontal)
        self.max_price_slider.setMinimum(1)
        self.max_price_slider.setMaximum(10000)
        self.max_price_slider.setValue(1000)
        self.max_price_slider.valueChanged.connect(self.update_price_label)

        self.price_label = QLabel("Price Range: Rp 10 juta - Rp 100 juta")
        form_layout.addRow("Price Range:", self.price_label)
        form_layout.addRow("Minimum:", self.min_price_slider)
        form_layout.addRow("Maximum:", self.max_price_slider)

        # Add buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_record)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Set main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Populate fields if editing
        if self.data:
            self.populate_fields()

    def update_price_label(self):
        min_value = self.min_price_slider.value()
        max_value = self.max_price_slider.value()
        min_price = min_value * 100000
        max_price = max_value * 100000
        self.price_label.setText(
            f"Price Range: {self.format_price(min_price)} - {self.format_price(max_price)}"
        )

    @staticmethod
    def format_price(value):
        if value >= 1_000_000_000:
            return f"Rp {value // 1_000_000_000} miliar"
        elif value >= 1_000_000:
            return f"Rp {value // 1_000_000} juta"
        else:
            return f"Rp {value // 1000} ribu"

    def populate_fields(self):
        self.name_input.setText(self.data["Name"])
        self.number_input.setText(self.data["Number"])
        self.website_input.setText(self.data["Website"])
        self.logo_input.setText(self.data["Logo"])
        self.address_input.setText(self.data["Address"])
        self.region_dropdown.setCurrentText(self.data["Region"])

        selected_scales = self.data["Scale"].split(", ")
        for checkbox in self.scale_checkboxes:
            if checkbox.text() in selected_scales:
                checkbox.setChecked(True)

        min_price, max_price = self.data["Price Range"].split(" - ")
        self.min_price_slider.setValue(
            int(min_price.replace("Rp ", "").replace(" juta", "").replace(" ", "")) * 10
        )
        self.max_price_slider.setValue(
            int(max_price.replace("Rp ", "").replace(" juta", "").replace(" ", "")) * 10
        )

    def save_record(self):
        self.values["Name"] = self.name_input.text()
        self.values["Number"] = self.number_input.text()
        self.values["Website"] = self.website_input.text()
        self.values["Logo"] = self.logo_input.text()
        self.values["Address"] = self.address_input.text()
        self.values["Region"] = self.region_dropdown.currentText()
        self.values["Scale"] = ", ".join(
            checkbox.text() for checkbox in self.scale_checkboxes if checkbox.isChecked()
        )
        self.values["Price Range"] = self.price_label.text().split(":")[1].strip()

        if not all(self.values.values()):
            QMessageBox.warning(self, "Warning", "All fields must be filled!")
            return

        self.accept()


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 1000, 600)

        self.headers = [
            "Select",
            "Name",
            "Number",
            "Website",
            "Logo",
            "Address",
            "Region",
            "Scale",
            "Price Range",
        ]

        self.regions = ["North", "South", "East", "West"]
        self.scales = ["Small", "Medium", "Large"]

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        label = QLabel("Admin Dashboard")
        label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        layout.addWidget(label)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.headers))
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_record)
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit_record)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        self.setCentralWidget(central_widget)

        # Display data
        self.display_vendors()

    def add_record(self):
            dialog = AddRecordDialog(self.regions, self.scales, parent=self)
            if dialog.exec_() == QDialog.Accepted:
                values = dialog.values

                try:
                    region_id = self.regions.index(values["Region"]) + 1
                    scale_ids = [self.scales.index(scale) + 1 for scale in values["Scale"].split(", ")]

                    min_price, max_price = map(
                        lambda p: int(p.replace("Rp ", "").replace(" juta", "").replace(" ", "")) * 1_000_000,
                        values["Price Range"].split(" - "),
                    )

                    cursor.execute(
                        "INSERT INTO vendor (Name, Number, Website, Logo, Address, MaxPrice, MinPrice, RegionID) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            values["Name"],
                            values["Number"],
                            values["Website"],
                            values["Logo"],
                            values["Address"],
                            max_price,
                            min_price,
                            region_id,
                        ),
                    )
                    vendor_id = cursor.lastrowid

                    for scale_id in scale_ids:
                        cursor.execute(
                            "INSERT INTO vendorscale (VendorID, ScaleID) VALUES (%s, %s)",
                            (vendor_id, scale_id),
                        )

                    db.commit()
                    QMessageBox.information(self, "Success", "Vendor successfully added.")
                    row_position = self.table_widget.rowCount()
                    self.table_widget.insertRow(row_position)
                    for col, header in enumerate(self.headers):
                        self.table_widget.setItem(row_position, col, QTableWidgetItem(values[header]))

                except Exception as err:
                    QMessageBox.critical(self, "Error", f"Error: {err}")
                    db.rollback()


    def edit_record(self):
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            return

        data = {
            self.headers[col]: self.table_widget.item(selected_row, col).text()
            for col in range(1, self.table_widget.columnCount())
        }

        dialog = AddRecordDialog(self.regions, self.scales, data=data, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            for col, header in enumerate(self.headers[1:], start=1):
                value = dialog.values[header]
                self.table_widget.setItem(selected_row, col, QTableWidgetItem(value))

    def delete_record(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            self.table_widget.removeRow(selected_row)


    def display_vendors(self):
        query = """
            SELECT 
                v.Name, v.Number, v.Website, v.Logo, v.Address, 
                r.Region AS RegionName,
                GROUP_CONCAT(s.Scale SEPARATOR ', ') AS ScaleNames,
                CONCAT('Rp ', FORMAT(v.MinPrice, 0), ' - Rp ', FORMAT(v.MaxPrice, 0)) AS PriceRange
            FROM 
                vendor v
            JOIN 
                region r ON v.RegionID = r.ID
            LEFT JOIN 
                vendorscale vs ON v.ID = vs.VendorID
            LEFT JOIN 
                scale s ON vs.ScaleID = s.ID
            GROUP BY 
                v.ID;
        """
        try:
            cursor.execute(query)
            vendors = cursor.fetchall()

            # Reset table
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(len(self.headers))
            self.table_widget.setHorizontalHeaderLabels(self.headers)

            # Populate table with data
            for row_number, vendor in enumerate(vendors):
                self.table_widget.insertRow(row_number)
                for column_number, data in enumerate(vendor):
                    item = QTableWidgetItem(str(data))
                    self.table_widget.setItem(row_number, column_number + 1, item)
        except mc.Error as err:
            QMessageBox.critical(self, "Error", f"Database error: {err}")

    
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = AdminWindow()
  window.show()
  sys.exit(app.exec_())
