import sys
import csv
import json
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QFileDialog, QMessageBox, QStatusBar, QAbstractItemView)
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import Qt, QTimer
from toolbar import ToolbarManager
from menubar import MenuManager
from netstat_monitor import NetstatMonitor
from config_window import ConfigWindow
from details_window import DetailsWindow
from modern_theme import ModernTheme
from ui_components import SearchBar, StatsPanel

class NetsorgeWindow(QMainWindow):
    """
    Ventana Principal de Netsorge - Monitor de Red Moderno.
    
    Características principales:
    - Monitoreo en tiempo real de conexiones de red
    - Interfaz moderna inspirada en Tailwind CSS
    - Búsqueda y filtrado en tiempo real
    - Estadísticas visuales
    - Temas dark/light
    - Exportación de datos
    - Geolocalización de IPs
    - Herramientas de diagnóstico (ping, traceroute, etc.)
    """
    def __init__(self):
        super().__init__()
        
        # === 1. COMPONENTES CORE ===
        self.netstat_monitor = NetstatMonitor()
        self.timer = QTimer()
        self.is_paused = False
        self.all_connections = []  # Almacena todas las conexiones sin filtrar
        
        # === 2. CONFIGURACIÓN INICIAL ===
        self.current_theme = "dark"
        self.column_visibility = []
        
        # === 3. CONSTRUIR UI ===
        self.setup_ui()
        
        # === 4. GESTORES ===
        self.toolbar_manager = ToolbarManager(self)
        self.menu_manager = MenuManager(self)
        
        # === 5. DATOS INICIALES ===
        self.load_data()
        self.start_auto_refresh()
        
        # === 6. APLICAR TEMA MODERNO ===
        self.apply_modern_theme("dark")

    def setup_ui(self):
        """
        Configura la interfaz de usuario completa.
        Layout moderno con separación clara de componentes.
        """
        self.setWindowTitle("Netsorge - Network Security Monitor")
        self.setWindowIcon(QIcon("netsorge_icon2.png"))
        self.resize(1200, 800)
        
        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # === PANEL DE ESTADÍSTICAS ===
        self.stats_panel = StatsPanel()
        main_layout.addWidget(self.stats_panel)
        
        # === BARRA DE BÚSQUEDA ===
        self.search_bar = SearchBar()
        self.search_bar.textChanged.connect(self.filter_table)
        main_layout.addWidget(self.search_bar)
        
        # === TABLA DE CONEXIONES ===
        self.setup_table()
        main_layout.addWidget(self.table_widget)
        
        # === BARRA DE ESTADO ===
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("Ready")
        
        # === SEÑALES ===
        self.table_widget.cellDoubleClicked.connect(self.open_details)

    def setup_table(self):
        """Configura la tabla principal de conexiones."""
        self.table_widget = QTableWidget()
        
        # Definir columnas
        self.headers = [
            "Process Name", "Process ID", "Protocol", "Local Port", 
            "Local Port Name", "Local Address", "Remote Port Name", "Remote Port", 
            "Remote Name", "Remote Address", "Remote Host Name", "State",
            "Sent Byte", "Received Byte", "Sent Packets", "Received Packets", 
            "Process Path", "Product Name", "File Version", "Company", 
            "Process Create On", "User Name", "Process Services", "Process Attribute", 
            "Added On", "Creation TimeStamp", "Module Filename", "Remote IP Country", 
            "Remote IP ASN", "Remote IP Company", "Windows Title"
        ]
        
        self.table_widget.setColumnCount(len(self.headers))
        self.table_widget.setHorizontalHeaderLabels(self.headers)
        
        # Configuración de tabla
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
        
        # *** CRÍTICO: Hacer la tabla SOLO LECTURA - No editable ***
        # Esto previene que el usuario pueda modificar los datos de red mostrados
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Ajustar columnas
        self.table_widget.resizeColumnsToContents()

    def start_auto_refresh(self):
        """Inicia el temporizador de actualización automática (cada 3 segundos)."""
        self.timer.timeout.connect(self.load_data)
        self.timer.start(3000)
        self.is_paused = False
        self.update_status("Auto-refresh enabled (every 3s)")

    def toggle_auto_refresh(self):
        """Pausa o reanuda la actualización automática."""
        if self.is_paused:
            self.timer.start(3000)
            self.is_paused = False
            self.update_status("Auto-refresh resumed")
        else:
            self.timer.stop()
            self.is_paused = True
            self.update_status("Auto-refresh paused")

    def load_data(self):
        """
        Carga los datos de red desde netstat y actualiza la tabla.
        También actualiza las estadísticas.
        """
        self.all_connections = self.netstat_monitor.get_network_connections()
        self.populate_table(self.all_connections)
        self.update_statistics()

    def populate_table(self, connections):
        """
        Rellena la tabla con las conexiones proporcionadas.
        Mantiene el rendimiento deshabilitando el ordenamiento temporalmente.
        """
        self.table_widget.setRowCount(len(connections))
        self.table_widget.setSortingEnabled(False)

        for row_idx, data in enumerate(connections):
            for col_idx, header in enumerate(self.headers):
                val = data.get(header, "")
                item = QTableWidgetItem(str(val))
                
                # Alineación
                if header in ["Process ID", "Local Port", "Remote Port"]:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                
                # Coloración del estado
                if header == "State":
                    self.apply_state_color(item, val)
                
                self.table_widget.setItem(row_idx, col_idx, item)
        
        self.table_widget.setSortingEnabled(True)

    def apply_state_color(self, item, state):
        """Aplica colores basados en el estado de la conexión."""
        colors = ModernTheme.COLORS[self.current_theme]
        
        if state == "ESTABLISHED":
            item.setForeground(QColor(colors['success']))
        elif state == "LISTENING":
            item.setForeground(QColor(colors['info']))
        elif state == "TIME_WAIT":
            item.setForeground(QColor(colors['warning']))
        elif state in ["CLOSE_WAIT", "CLOSING"]:
            item.setForeground(QColor(colors['danger']))

    def filter_table(self, search_text):
        """
        Filtra la tabla basándose en el texto de búsqueda.
        Busca en múltiples columnas: Process Name, Remote Address, Local Port, State.
        """
        search_text = search_text.lower()
        
        if not search_text:
            # Mostrar todas las conexiones
            self.populate_table(self.all_connections)
            return
        
        # Filtrar conexiones
        filtered = []
        search_columns = ["Process Name", "Remote Address", "Local Address", 
                         "Local Port", "Remote Port", "State", "Protocol"]
        
        for conn in self.all_connections:
            # Buscar en las columnas especificadas
            for col in search_columns:
                value = str(conn.get(col, "")).lower()
                if search_text in value:
                    filtered.append(conn)
                    break
        
        self.populate_table(filtered)
        self.update_status(f"Showing {len(filtered)} of {len(self.all_connections)} connections")

    def update_statistics(self):
        """Actualiza las tarjetas de estadísticas."""
        total = len(self.all_connections)
        established = sum(1 for c in self.all_connections if c.get("State") == "ESTABLISHED")
        listening = sum(1 for c in self.all_connections if c.get("State") == "LISTENING")
        
        # Contar procesos únicos
        unique_processes = set(c.get("Process Name", "") for c in self.all_connections)
        processes = len(unique_processes)
        
        self.stats_panel.update_stats(total, established, listening, processes)

    def update_status(self, message):
        """Actualiza el mensaje en la barra de estado."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_bar.showMessage(f"[{timestamp}] {message}")

    def open_config(self):
        """Abre la ventana de configuración de columnas."""
        current_vis = []
        for i in range(self.table_widget.columnCount()):
            current_vis.append(not self.table_widget.isColumnHidden(i))
            
        dialog = ConfigWindow(self, self.headers, current_vis)
        if dialog.exec():
            new_vis = dialog.get_visibility_map()
            for i, visible in enumerate(new_vis):
                self.table_widget.setColumnHidden(i, not visible)
            self.update_status("Column visibility updated")

    def open_details(self, row, column):
        """
        Abre la ventana de detalles al hacer doble clic en una fila.
        Muestra geolocalización y herramientas de diagnóstico.
        """
        try:
            remote_addr_idx = self.headers.index("Remote Address")
            item = self.table_widget.item(row, remote_addr_idx)
            if item:
                ip_address = item.text()
                
                # Limpiar IP (quitar puerto si existe)
                if ":" in ip_address and "]" not in ip_address:
                    ip_address = ip_address.split(":")[0]
                elif "]" in ip_address:
                    ip_address = ip_address.split("]:")[0].replace("[", "")
                
                # Pausar mientras se ve el detalle
                was_paused = self.is_paused
                if not was_paused:
                    self.toggle_auto_refresh()

                details = DetailsWindow(ip_address, self, self.current_theme)
                details.exec()
                
                if not was_paused:
                    self.toggle_auto_refresh()
                    
                self.update_status(f"Viewed details for {ip_address}")

        except ValueError:
            self.update_status("Error: Remote Address column not found")

    def export_to_csv(self):
        """Exporta los datos actuales a un archivo CSV."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.headers)
                    writer.writeheader()
                    writer.writerows(self.all_connections)
                
                self.update_status(f"Data exported to {filename}")
                QMessageBox.information(self, "Export Successful", 
                                       f"Data exported successfully to:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Error: {str(e)}")
                self.update_status(f"Export failed: {str(e)}")

    def export_to_json(self):
        """Exporta los datos actuales a un archivo JSON."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export to JSON", "", "JSON Files (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(self.all_connections, file, indent=2)
                
                self.update_status(f"Data exported to {filename}")
                QMessageBox.information(self, "Export Successful", 
                                       f"Data exported successfully to:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Error: {str(e)}")
                self.update_status(f"Export failed: {str(e)}")

    def toggle_theme(self):
        """Alterna entre tema oscuro y claro."""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_modern_theme(new_theme)
        self.update_status(f"Theme changed to {new_theme} mode")

    def apply_modern_theme(self, theme_name):
        """
        Aplica el tema visual moderno.
        Usa el sistema de temas de modern_theme.py.
        """
        self.current_theme = theme_name
        stylesheet = ModernTheme.get_stylesheet(theme_name)
        self.setStyleSheet(stylesheet)
        
        # Re-aplicar colores de estado
        self.populate_table(self.all_connections)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetsorgeWindow()
    window.show()
    sys.exit(app.exec())