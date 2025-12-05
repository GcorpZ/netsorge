"""
Componentes de UI modernos reutilizables.
"""
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                               QLineEdit, QPushButton)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

class SearchBar(QWidget):
    """
    Barra de búsqueda moderna con icono y placeholder.
    Emite una señal cuando el texto cambia.
    """
    textChanged = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Input de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search connections... (Process, IP, Port)")
        self.search_input.textChanged.connect(self.textChanged.emit)
        
        # Botón de limpiar
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setMaximumWidth(80)
        self.clear_btn.clicked.connect(self.clear_search)
        
        layout.addWidget(self.search_input)
        layout.addWidget(self.clear_btn)
    
    def clear_search(self):
        self.search_input.clear()
    
    def get_text(self):
        return self.search_input.text()


class StatsCard(QWidget):
    """
    Tarjeta de estadísticas moderna (card component).
    Muestra un título, un valor y opcionalmente un icono.
    """
    def __init__(self, title, value="0", icon_path=None, parent=None):
        super().__init__(parent)
        self.title = title
        self.value_text = value
        self.icon_path = icon_path
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Título
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            font-size: 11px; 
            font-weight: 600; 
            text-transform: uppercase;
            letter-spacing: 0.5px;
            opacity: 0.7;
        """)
        
        # Valor
        self.value_label = QLabel(self.value_text)
        self.value_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: 700;
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        
        # Estilo del card
        self.setStyleSheet("""
            StatsCard {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
    
    def update_value(self, new_value):
        """Actualiza el valor mostrado en la tarjeta."""
        self.value_label.setText(str(new_value))


class StatsPanel(QWidget):
    """
    Panel que contiene múltiples tarjetas de estadísticas.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(12)
        
        # Tarjetas de estadísticas
        self.total_card = StatsCard("Total Connections", "0")
        self.established_card = StatsCard("Established", "0")
        self.listening_card = StatsCard("Listening", "0")
        self.processes_card = StatsCard("Processes", "0")
        
        layout.addWidget(self.total_card)
        layout.addWidget(self.established_card)
        layout.addWidget(self.listening_card)
        layout.addWidget(self.processes_card)
    
    def update_stats(self, total, established, listening, processes):
        """Actualiza todas las estadísticas."""
        self.total_card.update_value(total)
        self.established_card.update_value(established)
        self.listening_card.update_value(listening)
        self.processes_card.update_value(processes)
