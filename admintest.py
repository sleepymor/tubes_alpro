from database import cursor, mc, db
import sys, os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
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
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtCore import Qt


class AddRecordDialog(QDialog):
    def __init__(self, regions, scales, data=None):
        super().__init__()
        self.setWindowTitle("Add Vendor")
        self.setMinimumWidth(400)

        self.values = {}
        self.logo_path = ""

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Input fields
        self.name_input = QLineEdit(data.get("Name") if data else "")
        self.number_input = QLineEdit(data.get("Number") if data else "")
        self.website_input = QLineEdit(data.get("Website") if data else "")
        self.address_input = QLineEdit(data.get("Address") if data else "")

        # Region dropdown
        self.region_combo = QComboBox()
        for region_id, region_name in regions:
            self.region_combo.addItem(region_name, region_id)

        # Scales checkboxes
        self.scale_checkboxes = []
        scale_layout = QVBoxLayout()
        for scale_id, scale_name in scales:
            checkbox = QCheckBox(scale_name)
            checkbox.setProperty("scale_id", scale_id)  # Store the scale ID in the checkbox
            scale_layout.addWidget(checkbox)
            self.scale_checkboxes.append(checkbox)

        scale_groupbox = QWidget()
        scale_groupbox.setLayout(scale_layout)

        # Logo upload
        self.logo_input = QLineEdit()
        self.logo_input.setPlaceholderText("Drag and drop a file or click 'Browse'")
        self.logo_input.setReadOnly(True)
        self.logo_input.setAcceptDrops(True)
        self.logo_input.dragEnterEvent = self.drag_enter_event
        self.logo_input.dropEvent = self.drop_event

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_logo)

        # Price Range
        self.min_price_input = QLineEdit()
        self.max_price_input = QLineEdit()

        # Add fields to the form
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Contact Number:", self.number_input)
        form_layout.addRow("Website:", self.website_input)
        form_layout.addRow("Address:", self.address_input)
        form_layout.addRow("Region:", self.region_combo)
        form_layout.addRow("Scales:", scale_groupbox)
        form_layout.addRow("Logo:", self.logo_input)
        form_layout.addRow("", self.browse_button)
        form_layout.addRow("Min Price (500k):", self.min_price_input)
        form_layout.addRow("Max Price (1B):", self.max_price_input)

        layout.addLayout(form_layout)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if os.path.splitext(file_path)[1].lower() in [".jpg", ".png", ".jpeg"]:
                self.logo_input.setText(file_path)
                self.logo_path = file_path
            else:
                QMessageBox.warning(
                    self, "Invalid File", "Please drop a valid image file!"
                )

    def browse_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Logo", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.logo_input.setText(file_path)
            self.logo_path = file_path

    def save_data(self):
        try:
            # Validate price range
            min_price = int(self.min_price_input.text())
            max_price = int(self.max_price_input.text())

            if min_price < 500_000 or max_price > 1_000_000_000:
                raise ValueError("Prices must be between 500k and 1B!")

            # Copy logo to ./vendor_logo/ directory
            if self.logo_path:
                target_dir = "./vendor_logo/"
                os.makedirs(target_dir, exist_ok=True)
                target_path = os.path.join(target_dir, os.path.basename(self.logo_path))
                if self.logo_path != target_path:
                    import shutil

                    shutil.copy(self.logo_path, target_path)

                self.values["Logo"] = target_path

            # Collect selected scales
            selected_scales = [
                checkbox.property("scale_id")
                for checkbox in self.scale_checkboxes
                if checkbox.isChecked()
            ]
            if not selected_scales:
                raise ValueError("At least one scale must be selected.")

            # Collect remaining input values
            self.values.update(
                {
                    "Name": self.name_input.text(),
                    "Number": self.number_input.text(),
                    "Website": self.website_input.text(),
                    "Address": self.address_input.text(),
                    "Region": self.region_combo.currentData(),
                    "Scales": selected_scales,
                    "MinPrice": min_price,
                    "MaxPrice": max_price,
                }
            )

            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        # Buttons for CRUD operations
        button_layout = QHBoxLayout()
        load_button = QPushButton("Load Vendors")
        load_button.clicked.connect(self.display_vendors)

        add_button = QPushButton("Add Vendor")
        add_button.clicked.connect(self.add_vendor)

        update_button = QPushButton("Update Vendor")
        update_button.clicked.connect(self.update_vendor)

        delete_button = QPushButton("Delete Vendor")
        delete_button.clicked.connect(self.delete_vendor)

        button_layout.addWidget(load_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def display_vendors(self):
        query = """
            SELECT 
            v.ID AS VendorID,
            v.Name AS VendorName,
            v.Number AS ContactNumber,
            v.Website AS VendorWebsite,
            v.Logo AS VendorLogo,
            v.Address AS VendorAddress,
            v.MaxPrice,
            v.MinPrice,
            r.Region AS RegionName,
            GROUP_CONCAT(s.Scale SEPARATOR ', ') AS ScaleNames
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

            self.table.setRowCount(0)
            self.table.setColumnCount(len(vendors[0]))
            self.table.setHorizontalHeaderLabels(
                [
                    "ID",
                    "Name",
                    "Number",
                    "Website",
                    "Logo",
                    "Address",
                    "Max Price",
                    "Min Price",
                    "Region",
                    "Scales",
                ]
            )

            for row_number, vendor in enumerate(vendors):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(vendor):
                    self.table.setItem(
                        row_number, column_number, QTableWidgetItem(str(data))
                    )
        except mc.Error as err:
            QMessageBox.critical(self, "Error", f"Database error: {err}")

# Fungsi untuk menampilkan region
def get_regions(cursor):
    cursor.execute("SELECT ID, Region FROM region")
    regions = cursor.fetchall()
    return regions

# Fungsi untuk menampilkan scale
def get_scales(cursor):
    cursor.execute("SELECT ID, Scale FROM scale")
    scales = cursor.fetchall()

def add_vendor(cursor):

    name = input("Masukkan nama vendor: ")
    number = input("Masukkan nomor vendor: ")
    website = input("Masukkan website vendor: ")
    logo = input("Masukkan logo vendor (URL/file path): ")
    address = input("Masukkan alamat vendor: ")
    max_price = int(input("Masukkan harga maksimum: "))
    min_price = int(input("Masukkan harga minimum: "))

    get_regions(cursor)
    region_ids = input("Masukkan ID region (maksimal 3, pisahkan dengan koma): ")

    get_scales(cursor)
    scale_ids = input("Masukkan ID scale (maksimal 3, pisahkan dengan koma): ")
    scale_ids = [int(id.strip()) for id in scale_ids.split(",")[:3]]

    try:
        cursor.execute(
            "INSERT INTO vendor (Name, Number, Website, Logo, Address, MaxPrice, MinPrice, RegionID) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (name, number, website, logo, address, max_price, min_price, region_ids[0]),
        )
        vendor_id = cursor.lastrowid

        for scale_id in scale_ids:
            cursor.execute(
                "INSERT INTO vendorscale (VendorID, ScaleID) VALUES (%s, %s)",
                (vendor_id, scale_id),
            )

        for region_id in region_ids[1:]:
            cursor.execute(
                "INSERT INTO vendor (Name, Number, Website, Logo, Address, MaxPrice, MinPrice, RegionID) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, number, website, logo, address, max_price, min_price, region_id),
            )

        db.commit()
        print("Vendor berhasil ditambahkan.")
    except mc.Error as err:
        print(f"Terjadi kesalahan: {err}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

    def update_vendor(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a vendor to update.")
            return

        vendor_id = self.table.item(selected_row, 0).text()
        data = {
            "Name": self.table.item(selected_row, 1).text(),
            "Number": self.table.item(selected_row, 2).text(),
            "Website": self.table.item(selected_row, 3).text(),
            "Logo": self.table.item(selected_row, 4).text(),
            "Address": self.table.item(selected_row, 5).text(),
            "Region": self.table.item(selected_row, 8).text(),
            "Scale": self.table.item(selected_row, 9).text(),
        }
        dialog = AddRecordDialog(
            regions=["Region 1", "Region 2"], scales=["Scale 1", "Scale 2"], data=data
        )
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.values
            try:
                query = """
                    UPDATE vendor 
                    SET Name=%s, Number=%s, Website=%s, Logo=%s, Address=%s, 
                        RegionID=(SELECT ID FROM region WHERE Region=%s),
                        MinPrice=%s, MaxPrice=%s
                    WHERE ID=%s
                """
                cursor.execute(
                    query,
                    (
                        values["Name"],
                        values["Number"],
                        values["Website"],
                        values["Logo"],
                        values["Address"],
                        values["Region"],
                        int(
                            values["Price Range"]
                            .split("-")[0]
                            .replace("Rp", "")
                            .replace("juta", "")
                            .strip()
                        )
                        * 1_000_000,
                        int(
                            values["Price Range"]
                            .split("-")[1]
                            .replace("Rp", "")
                            .replace("juta", "")
                            .strip()
                        )
                        * 1_000_000,
                        vendor_id,
                    ),
                )
                mc.commit()
                QMessageBox.information(self, "Success", "Vendor updated successfully!")
                self.display_vendors()
            except mc.Error as err:
                QMessageBox.critical(self, "Error", f"Database error: {err}")

    def delete_vendor(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a vendor to delete.")
            return

        vendor_id = self.table.item(selected_row, 0).text()
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this vendor?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            try:
                query = "DELETE FROM vendor WHERE ID=%s"
                cursor.execute(query, (vendor_id,))
                mc.commit()
                QMessageBox.information(self, "Success", "Vendor deleted successfully!")
                self.display_vendors()
            except mc.Error as err:
                QMessageBox.critical(self, "Error", f"Database error: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec_())
