from PySide6.QtWidgets import QMenuBar, QMenu, QMainWindow
from PySide6.QtGui import QAction

class MenuManager:
    """
    Clase para manejar la barra de menús (MenuBar).
    """
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        self.init_menu()

    def init_menu(self):
        # Obtenemos la barra de menú de la ventana principal
        menu_bar = self.main_window.menuBar()

        # --- Menú Archivo (File) ---
        # addMenu crea un menú desplegable en la barra
        file_menu = menu_bar.addMenu("&File") # El '&' indica que Alt+F abre este menú

        # Exportar a CSV
        export_csv_action = QAction("Export to CSV...", self.main_window)
        export_csv_action.setShortcut("Ctrl+E")
        export_csv_action.triggered.connect(self.main_window.export_to_csv)
        file_menu.addAction(export_csv_action)

        # Exportar a JSON
        export_json_action = QAction("Export to JSON...", self.main_window)
        export_json_action.triggered.connect(self.main_window.export_to_json)
        file_menu.addAction(export_json_action)

        file_menu.addSeparator()

        # Acción Salir
        exit_action = QAction("Exit", self.main_window)
        exit_action.setShortcut("Ctrl+Q") # Atajo de teclado
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)

        # --- Menú Ver (View) ---
        view_menu = menu_bar.addMenu("&View")
        
        # Ejemplo: Acción para refrescar datos
        refresh_action = QAction("Refresh Data", self.main_window)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.on_refresh)
        view_menu.addAction(refresh_action)

        # --- Menú Ayuda (Help) ---
        help_menu = menu_bar.addMenu("&Help")
        
        about_action = QAction("About", self.main_window)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)

        # --- Menú Herramientas (Tools) ---
        tools_menu = menu_bar.addMenu("&Tools")

        # Submenú Temas
        theme_menu = tools_menu.addMenu("Theme")
        
        dark_action = QAction("Dark Mode", self.main_window)
        dark_action.triggered.connect(lambda: self.main_window.apply_theme("dark"))
        theme_menu.addAction(dark_action)

        light_action = QAction("Light Mode", self.main_window)
        light_action.triggered.connect(lambda: self.main_window.apply_theme("light"))
        theme_menu.addAction(light_action)

        tools_menu.addSeparator()

        # Opción Configuración
        config_action = QAction("Options...", self.main_window)
        config_action.setShortcut("Ctrl+O")
        config_action.triggered.connect(self.main_window.open_config)
        tools_menu.addAction(config_action)

    def on_refresh(self):
        print("Refrescando datos desde el menú...")
        # Aquí podríamos llamar a una función de la ventana principal para actualizar la tabla
        # Por ejemplo: self.main_window.refresh_table_data()

    def on_about(self):
        print("Acerca de Netsorge...")
