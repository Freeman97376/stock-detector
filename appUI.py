import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                               QVBoxLayout, QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import Qt

#my own files
import data_fetcher
from data_fetcher import YFinanceProvider


class StockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Trader")
        self.setMinimumSize(400, 300)
       
        # 1. Initialize the Data Provider
        # We create the "worker" here so it's ready to use later
        self.provider = YFinanceProvider()

        # 2. UI Setup (Same as before)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Enter Symbol (e.g., AAPL, 600519.SS)")
        
        self.search_btn = QPushButton("Get Price")
        
        self.price_label = QLabel("Price: -")
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.price_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.layout.addWidget(self.symbol_input)
        self.layout.addWidget(self.search_btn)
        self.layout.addWidget(self.price_label)

        # 3. Connect the Button to the Function
        # This tells Qt: "When clicked, run self.fetch_price"
        self.search_btn.clicked.connect(self.fetch_price)

    def fetch_price(self):
        """
        This function runs every time the button is clicked.
        """
        symbol = self.symbol_input.text().strip().upper()
        
        if not symbol:
            self.price_label.setText("Please enter a symbol")
            return

        self.price_label.setText("Loading...")
        # Force the UI to update the text immediately before freezing
        QApplication.processEvents() 

        try:
            # Call our data provider
            price = self.provider.get_realtime_price(symbol)
            self.price_label.setText(f"Price: {price:.2f}")
        except Exception as e:
            self.price_label.setText(f"Error: {str(e)}")

if __name__ == "__main__":
    # The QApplication manages the GUI's control flow and main settings.
    app = QApplication(sys.argv)
    
    window = StockApp()
    window.show()
    
    # Start the event loop (sys.exit ensures a clean exit when the window closes)
    sys.exit(app.exec())