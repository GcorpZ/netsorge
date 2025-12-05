from PySide6.QtWidgets import QToolBar, QMainWindow
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QSize

class ToolbarManager:
    """
    Clase para manejar la barra de herramientas (Toolbar).
    Utiliza los iconos Fugue para dar un look profesional.
    """
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        self.init_toolbar()

    def init_toolbar(self):
        """Crea y configura la barra de herramientas moderna con iconos Fugue."""
        self.toolbar = QToolBar("Main Toolbar")
        # Los iconos Fugue son de 16x16 píxeles
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.setMovable(False) # Fija para look moderno
        self.main_window.addToolBar(self.toolbar)

        # --- Acciones con Iconos Fugue ---
        
        # Refresh (icono de flechas circulares dobles)
        refresh_icon = self.load_icon("icons/icons/arrow-circle-double.png")
        refresh_action = QAction(refresh_icon, "Refresh", self.main_window)
        refresh_action.setStatusTip("Refresh Network Data Immediately")
        refresh_action.triggered.connect(self.main_window.load_data)
        self.toolbar.addAction(refresh_action)

        # Pause/Resume Auto-Refresh (icono de pausa)
        pause_icon = self.load_icon("icons/icons/control-pause.png")
        pause_action = QAction(pause_icon, "Pause/Resume", self.main_window)
        pause_action.setStatusTip("Pause or Resume Auto-Refresh")
        pause_action.triggered.connect(self.main_window.toggle_auto_refresh)
        self.toolbar.addAction(pause_action)

        self.toolbar.addSeparator()

        # Settings / Options (icono de engranaje)
        options_icon = self.load_icon("icons/icons/gear.png")
        options_action = QAction(options_icon, "Options", self.main_window)
        options_action.setStatusTip("Configure Visible Columns")
        options_action.triggered.connect(self.main_window.open_config)
        self.toolbar.addAction(options_action)
        
        # Theme Toggle (icono de bombilla)
        theme_icon = self.load_icon("icons/icons/light-bulb.png")
        theme_action = QAction(theme_icon, "Toggle Theme", self.main_window)
        theme_action.setStatusTip("Switch between Dark and Light Mode")
        theme_action.triggered.connect(self.main_window.toggle_theme)
        self.toolbar.addAction(theme_action)

        self.toolbar.addSeparator()

        # Exit (icono de control-poder/apagado)
        exit_icon = self.load_icon("icons/icons/control-power.png")
        exit_action = QAction(exit_icon, "Exit", self.main_window)
        exit_action.setStatusTip("Exit Application")
        exit_action.triggered.connect(self.main_window.close)
        self.toolbar.addAction(exit_action)

    def load_icon(self, path):
        """
        Carga un icono desde la ruta especificada.
        Si falla, devuelve un icono vacío para evitar errores.
        """
        icon = QIcon(path)
        if icon.isNull():
            print(f"Warning: Failed to load icon from {path}")
        return icon