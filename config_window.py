from PySide6.QtWidgets import (QDialog, QVBoxLayout, QCheckBox, 
                               QDialogButtonBox, QScrollArea, QWidget)
from PySide6.QtCore import Qt

class ConfigWindow(QDialog):
    """
    Ventana de configuración para seleccionar qué columnas mostrar.
    """
    def __init__(self, parent=None, all_headers=None, current_visibility=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration - Column Selection")
        self.resize(400, 500)
        
        self.all_headers = all_headers or []
        self.current_visibility = current_visibility or []
        self.checkboxes = []

        # Layout principal
        layout = QVBoxLayout(self)

        # Área de scroll para las columnas (son muchas)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Crear un checkbox por cada columna
        for idx, header in enumerate(self.all_headers):
            cb = QCheckBox(header)
            # Si el índice está en current_visibility (o es True), marcarlo
            is_visible = True
            if self.current_visibility and idx < len(self.current_visibility):
                is_visible = self.current_visibility[idx]
            
            cb.setChecked(is_visible)
            self.checkboxes.append(cb)
            scroll_layout.addWidget(cb)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Botones OK / Cancel
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_visibility_map(self):
        """Retorna una lista de booleanos indicando si la columna N debe mostrarse."""
        return [cb.isChecked() for cb in self.checkboxes]
