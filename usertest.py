import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QGridLayout, QLabel, QLineEdit,
    QSlider, QComboBox, QHBoxLayout, QPushButton, QWidget, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from database import cursor


class VendorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vendor Application")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search vendors...")
        self.search_bar.textChanged.connect(self.update_vendor_list)

        # Filters
        self.scale_filter = QComboBox()
        self.scale_filter.addItem("All Scales")
        self.load_scales()

        self.min_price_slider = QSlider(Qt.Horizontal)
        self.min_price_slider.setRange(0, 100000)
        self.min_price_slider.setValue(0)
        self.min_price_slider.valueChanged.connect(self.update_vendor_list)

        self.max_price_slider = QSlider(Qt.Horizontal)
        self.max_price_slider.setRange(0, 100000)
        self.max_price_slider.setValue(100000)
        self.max_price_slider.valueChanged.connect(self.update_vendor_list)

        # Slider Labels
        self.min_price_label = QLabel("Min Price: 0")
        self.max_price_label = QLabel("Max Price: 100000")
        self.min_price_slider.valueChanged.connect(
            lambda: self.min_price_label.setText(f"Min Price: {self.min_price_slider.value()}")
        )
        self.max_price_slider.valueChanged.connect(
            lambda: self.max_price_label.setText(f"Max Price: {self.max_price_slider.value()}")
        )

        # Filters Layout
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Scale:"))
        filter_layout.addWidget(self.scale_filter)
        filter_layout.addWidget(self.min_price_label)
        filter_layout.addWidget(self.min_price_slider)
        filter_layout.addWidget(self.max_price_label)
        filter_layout.addWidget(self.max_price_slider)

        # Vendor Grid
        self.vendor_grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.vendor_grid_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.vendor_grid_widget)

        # Back Button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.show_main_menu)
        self.back_button.setVisible(False)

        # Detailed View Widget
        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_widget.setVisible(False)

        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addLayout(filter_layout)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.back_button)
        self.main_layout.addWidget(self.details_widget)

        # Load Vendors
        self.update_vendor_list()

    def load_scales(self):
        """Load scale options from the database."""
        cursor.execute("SELECT Scale FROM scale")
        scales = cursor.fetchall()
        for scale in scales:
            self.scale_filter.addItem(scale[0])
        self.scale_filter.currentIndexChanged.connect(self.update_vendor_list)

    def update_vendor_list(self):
        """Fetch vendor data based on filters and populate vendor cards in a grid."""
        search = self.search_bar.text()
        scale = self.scale_filter.currentText()
        min_price = self.min_price_slider.value()
        max_price = self.max_price_slider.value()

        # Base query
        query = """
            SELECT 
            v.ID, v.Name, v.MaxPrice, v.MinPrice, v.Logo, r.Region, 
            GROUP_CONCAT(s.Scale SEPARATOR ', ') AS Scales
        FROM 
            vendor v
        JOIN 
            region r ON v.RegionID = r.ID
        LEFT JOIN 
            vendorscale vs ON v.ID = vs.VendorID
        LEFT JOIN 
            scale s ON vs.ScaleID = s.ID
        WHERE 1=1
        """
        # Add filters to the query
        params = []
        if search:
            query += " AND v.Name LIKE %s"
            params.append(f"%{search}%")
        if scale != "All Scales":
            query += " AND s.Scale = %s"
            params.append(scale)
        if min_price > 0:
            query += " AND v.MinPrice >= %s"
            params.append(min_price)
        if max_price < 100000:
            query += " AND v.MaxPrice <= %s"
            params.append(max_price)
        query += " GROUP BY v.ID"

        # Execute query
        cursor.execute(query, params)
        vendors = cursor.fetchall()

        # Clear previous grid items
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add cards in grid
        row, col = 0, 0
        for vendor in vendors:
            vendor_id, name, max_price, min_price, logo, region, scales = vendor
            self.add_vendor_card(row, col, vendor_id, name, logo)
            col += 1
            if col > 2:  # 3 columns per row
                col = 0
                row += 1

    def add_vendor_card(self, row, col, vendor_id, name, logo):
        """Create a vendor card and add it to the grid layout."""
        card = QWidget()
        card_layout = QVBoxLayout()
        card.setFixedSize(200, 250)

        logo_label = QLabel()
        if logo:
            image = QImage(logo)  # Assume logo is a file path
            pixmap = QPixmap.fromImage(image)
            logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        else:
            logo_label.setText("No Logo")
            logo_label.setAlignment(Qt.AlignCenter)

        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        card_layout.addWidget(logo_label)
        card_layout.addWidget(name_label)
        card.setLayout(card_layout)

        card.setStyleSheet(
            """
            QWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QWidget:hover {
                background-color: #f9f9f9;
            }
            """
        )
        card.mousePressEvent = lambda event: self.display_vendor_details(vendor_id)
        self.grid_layout.addWidget(card, row, col)

    def display_vendor_details(self, vendor_id):
        """Display detailed vendor information."""
        self.scroll_area.setVisible(False)
        self.back_button.setVisible(True)
        self.details_widget.setVisible(True)

        # Fetch details for the selected vendor
        query = """
            SELECT 
            v.Name, v.MaxPrice, v.MinPrice, v.Address, v.Website, r.Region,
            GROUP_CONCAT(s.Scale SEPARATOR ', ') AS Scales
        FROM 
            vendor v
        JOIN 
            region r ON v.RegionID = r.ID
        LEFT JOIN 
            vendorscale vs ON v.ID = vs.VendorID
        LEFT JOIN 
            scale s ON vs.ScaleID = s.ID
        WHERE v.ID = %s
        GROUP BY v.ID
        """
        cursor.execute(query, (vendor_id,))
        vendor = cursor.fetchone()

        # Clear previous details
        for i in reversed(range(self.details_layout.count())):
            widget = self.details_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Populate details
        if vendor:
            name, max_price, min_price, address, website, region, scales = vendor
            self.details_layout.addWidget(QLabel(f"Name: {name}"))
            self.details_layout.addWidget(QLabel(f"Max Price: {max_price}"))
            self.details_layout.addWidget(QLabel(f"Min Price: {min_price}"))
            self.details_layout.addWidget(QLabel(f"Address: {address}"))
            self.details_layout.addWidget(QLabel(f"Website: {website}"))
            self.details_layout.addWidget(QLabel(f"Region: {region}"))
            self.details_layout.addWidget(QLabel(f"Scales: {scales}"))

    def show_main_menu(self):
        """Return to the main menu."""
        self.scroll_area.setVisible(True)
        self.back_button.setVisible(False)
        self.details_widget.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VendorApp()
    window.show()
    sys.exit(app.exec_())
