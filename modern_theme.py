"""
Estilos modernos para Netsorge - Inspirados en Tailwind CSS.

Este archivo contiene todos los estilos de la aplicación organizados
para fácil mantenimiento y personalización.
"""

class ModernTheme:
    """
    Clase que define los temas visuales modernos de la aplicación.
    Inspirado en diseños Tailwind CSS con colores armoniosos y diseño limpio.
    """
    
    # Paleta de colores moderna
    COLORS = {
        # Dark Theme Colors
        'dark': {
            'bg_primary': '#1a1a2e',      # Fondo principal oscuro profundo
            'bg_secondary': '#16213e',    # Fondo secundario
            'bg_tertiary': '#0f3460',     # Acentos y cards
            'text_primary': '#eaeaea',    # Texto principal
            'text_secondary': '#a0a0a0',  # Texto secundario
            'accent': '#e94560',          # Color de acento (rosa/rojo moderno)
            'accent_hover': '#ff6b81',    # Acento hover
            'success': '#4ecca3',         # Verde éxito
            'warning': '#ffa502',         # Naranja advertencia
            'danger': '#eb4d4b',          # Rojo peligro
            'info': '#5f27cd',            # Morado info
            'border': '#2c3e50',          # Bordes
            'shadow': 'rgba(0, 0, 0, 0.3)' # Sombras
        },
        # Light Theme Colors
        'light': {
            'bg_primary': '#f8f9fa',      # Fondo claro
            'bg_secondary': '#ffffff',    # Blanco puro
            'bg_tertiary': '#e9ecef',     # Gris muy claro
            'text_primary': '#2d3436',    # Texto oscuro
            'text_secondary': '#636e72',  # Gris medio
            'accent': '#6c5ce7',          # Morado moderno
            'accent_hover': '#a29bfe',    # Morado claro
            'success': '#00b894',         # Verde
            'warning': '#fdcb6e',         # Amarillo
            'danger': '#d63031',          # Rojo
            'info': '#0984e3',            # Azul
            'border': '#dfe6e9',          # Borde claro
            'shadow': 'rgba(0, 0, 0, 0.1)' # Sombra suave
        }
    }
    
    @staticmethod
    def get_stylesheet(theme_name='dark'):
        """
        Retorna el stylesheet completo para el tema especificado.
        Incluye estilos modernos con bordes redondeados, sombras, y gradientes.
        """
        colors = ModernTheme.COLORS[theme_name]
        
        return f"""
        /* === ESTILOS GENERALES === */
        QMainWindow, QDialog {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
            font-family: 'Segoe UI', 'SF Pro Display', -apple-system, system-ui, sans-serif;
            font-size: 13px;
        }}
        
        QWidget {{
            background-color: transparent;
            color: {colors['text_primary']};
        }}
        
        /* === TABLA === */
        QTableWidget {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            gridline-color: {colors['border']};
            border: none;
            border-radius: 8px;
            selection-background-color: {colors['accent']};
            selection-color: white;
            outline: none;
            padding: 4px;
        }}
        
        QTableWidget::item {{
            padding: 8px 12px;
            border-bottom: 1px solid {colors['border']};
        }}
        
        QTableWidget::item:hover {{
            background-color: {colors['bg_tertiary']};
        }}
        
        QTableWidget::item:selected {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        /* === ENCABEZADOS DE TABLA === */
        QHeaderView::section {{
            background-color: {colors['bg_tertiary']};
            color: {colors['text_primary']};
            padding: 10px 12px;
            border: none;
            border-right: 1px solid {colors['border']};
            border-bottom: 2px solid {colors['accent']};
            font-weight: 600;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.5px;
        }}
        
        QHeaderView::section:hover {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        /* === TOOLBAR === */
        QToolBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['bg_tertiary']}, 
                stop:1 {colors['bg_secondary']});
            border: none;
            border-bottom: 1px solid {colors['border']};
            spacing: 8px;
            padding: 8px 12px;
        }}
        
        QToolButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 6px;
            padding: 6px 12px;
            color: {colors['text_primary']};
            margin: 2px;
        }}
        
        QToolButton:hover {{
            background-color: {colors['accent']};
            border: 1px solid {colors['accent_hover']};
            color: white;
        }}
        
        QToolButton:pressed {{
            background-color: {colors['accent_hover']};
        }}
        
        /* === MENÚ === */
        QMenuBar {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            border-bottom: 1px solid {colors['border']};
            padding: 4px;
        }}
        
        QMenuBar::item {{
            padding: 6px 12px;
            border-radius: 4px;
            margin: 2px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        QMenu {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 8px;
        }}
        
        QMenu::item {{
            padding: 8px 24px;
            border-radius: 4px;
            margin: 2px;
        }}
        
        QMenu::item:selected {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        QMenu::separator {{
            height: 1px;
            background-color: {colors['border']};
            margin: 6px 12px;
        }}
        
        /* === BOTONES === */
        QPushButton {{
            background-color: {colors['accent']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 13px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['accent_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['accent']};
            padding: 11px 19px 9px 21px;
        }}
        
        /* === INPUTS === */
        QLineEdit {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
        }}
        
        QLineEdit:focus {{
            border: 2px solid {colors['accent']};
        }}
        
        /* === SCROLLBAR === */
        QScrollBar:vertical {{
            background-color: {colors['bg_secondary']};
            width: 12px;
            border-radius: 6px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['accent']};
            border-radius: 6px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['accent_hover']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: {colors['bg_secondary']};
            height: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {colors['accent']};
            border-radius: 6px;
            min-width: 30px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {colors['accent_hover']};
        }}
        
        /* === CHECKBOXES === */
        QCheckBox {{
            color: {colors['text_primary']};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {colors['border']};
            border-radius: 4px;
            background-color: {colors['bg_secondary']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {colors['accent']};
            border: 2px solid {colors['accent']};
        }}
        
        /* === LABELS === */
        QLabel {{
            color: {colors['text_primary']};
        }}
        
        /* === STATUS BAR === */
        QStatusBar {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_secondary']};
            border-top: 1px solid {colors['border']};
            padding: 4px 8px;
        }}
        """
