from PySide6.QtWidgets import (QApplication, QWidget,QMainWindow,
                                QTableWidgetItem, QTableWidget, 
                                QVBoxLayout, QAbstractItemView)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import sys


class mymainapp(QMainWindow):

    def __init__(self):
        super().__init__()
        #Creating the main window charactristics
        self.setWindowIcon(QIcon("netsorge_icon2.png"))
        self.setWindowTitle("Netsorge")
        self.resize(800, 500) #Width, Height of the window

        #Creating the main window layout
        self.layout=QVBoxLayout()
        self.setLayout(self.layout)

        central_widget= QWidget()
        self.setCentralWidget(central_widget)
        layout=QVBoxLayout()
        central_widget.setLayout(layout)   

        self.QTableWidget=QTableWidget()   
        layout.addWidget(self.QTableWidget)

        # Define the headers exactly as they appear in the image
        headers = [
            "Almacén", "Ubicación", "Producto", "Descripción", 
            "Centro Co", "Unidad de Medida", "Cantidad", "Costo", 
            "Trazable", "Vto. Lote", "N'Lote", "Cod. Comercial Pr"
        ]
        self.QTableWidget.setColumnCount(len(headers))
        self.QTableWidget.setHorizontalHeaderLabels(headers)    
        self.QTableWidget.setRowCount(5) #Set a Reasonable Number of Rows

         # Set some default data and specific styling for the first row as seen in the image
        self.set_cell_data(0, 2, "0")
        self.set_cell_data(0, 6, "0,0000")
        self.set_cell_data(0, 7, "0,0000")
        self.set_cell_data(0, 8, "/")
        self.set_cell_data(0, 9, "/")

                # Apply specific styling for the "Centro Co" and "Unidad de Medida" columns (Columns 4 and 5)
        # This uses Qt Stylesheets (CSS-like)
        self.QTableWidget.setStyleSheet("""
            QTableWidget::item {
                /* Default item styling */
                padding: 4px;
            }
            QTableWidget::item:focus {
                /* Remove the default focus outline if needed */
                outline: none;
            }
        """)
        
        # Apply a specific background color to the header items for the blue columns
        for col in [4, 5]:
            header_item = self.QTableWidget.horizontalHeaderItem(col)
            header_item.setBackground(Qt.cyan) # Use a QBrush with the color you need

        # To color the cells in the first row blue as well (optional, not strictly in your image but common practice)
        for col in [4, 5]:
             item = QTableWidgetItem()
             item.setBackground(Qt.cyan)
             self.QTableWidget.setItem(0, col, item)

    def set_cell_data(self, row, column, text):
        """Helper to set text and ensure proper alignment/flags"""
        item = QTableWidgetItem(text)
        # Align text to the right for numerical values
        if column in [2, 6, 7]:
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.QTableWidget.setItem(row, column, item)    


if __name__ == "__main__":
    app=QApplication(sys.argv)
    window=mymainapp()
    window.show()
    sys.exit(app.exec())