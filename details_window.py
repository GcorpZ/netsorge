"""
Ventana de detalles moderna con herramientas de diagnóstico.
"""
import json
import urllib.request
import webbrowser
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QFormLayout, QWidget, QPushButton, QTabWidget,
                               QTextEdit, QGroupBox, QProgressBar)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, Qt, QThread, Signal
from PySide6.QtGui import QFont
from modern_theme import ModernTheme
from network_diagnostics import NetworkDiagnostics

class DiagnosticWorker(QThread):
    """
    Worker thread para ejecutar diagnósticos sin bloquear la UI.
    """
    finished = Signal(bool, str)  # (success, output)
    
    def __init__(self, diagnostic_func, *args):
        super().__init__()
        self.diagnostic_func = diagnostic_func
        self.args = args
    
    def run(self):
        success, output = self.diagnostic_func(*self.args)
        self.finished.emit(success, output)


class DetailsWindow(QDialog):
    """
    Ventana de detalles moderna para análisis de conexiones remotas.
    
    Características:
    - Información de geolocalización
    - Mapa interactivo
    - Herramientas de diagnóstico (ping, traceroute, nslookup)
    - Enlaces a servicios de reputación de IPs
    - Diseño moderno con tabs
    """
    def __init__(self, ip_address, parent=None, theme="dark"):
        super().__init__(parent)
        self.ip_address = ip_address
        self.theme = theme
        self.diagnostics = NetworkDiagnostics()
        self.worker = None
        
        self.setWindowTitle(f"🔍 Network Analysis - {ip_address}")
        self.resize(900, 700)
        
        self.setup_ui()
        self.apply_theme()
        self.fetch_geolocation_data()

    def setup_ui(self):
        """Construye la interfaz con tabs y diseño moderno."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === HEADER ===
        header = self.create_header()
        main_layout.addWidget(header)
        
        # === TABS ===
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Tab 1: Información y Mapa
        self.info_tab = self.create_info_tab()
        self.tabs.addTab(self.info_tab, "📍 Geolocation & Map")
        
        # Tab 2: Diagnósticos
        self.diag_tab = self.create_diagnostics_tab()
        self.tabs.addTab(self.diag_tab, "🔧 Network Diagnostics")
        
        # Tab 3: Reputación y Seguridad
        self.security_tab = self.create_security_tab()
        self.tabs.addTab(self.security_tab, "🛡️ Security & Reputation")
        
        main_layout.addWidget(self.tabs)

    def create_header(self):
        """Crea el encabezado de la ventana."""
        header = QWidget()
        header.setObjectName("header")
        layout = QVBoxLayout(header)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title = QLabel(f"Network Connection Analysis")
        title_font = QFont("Segoe UI", 18, QFont.Bold)
        title.setFont(title_font)
        
        # IP Address
        ip_label = QLabel(f"🌐 {self.ip_address}")
        ip_font = QFont("Segoe UI", 14)
        ip_label.setFont(ip_font)
        
        layout.addWidget(title)
        layout.addWidget(ip_label)
        
        return header

    def create_info_tab(self):
        """Tab con información de geolocalización y mapa."""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Left: Info
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        
        info_group = QGroupBox("📊 Geolocation Information")
        self.info_form = QFormLayout(info_group)
        self.info_form.setSpacing(12)
        
        info_layout.addWidget(info_group)
        info_layout.addStretch()
        
        # Right: Map
        map_group = QGroupBox("🗺️ Location Map")
        map_layout = QVBoxLayout(map_group)
        
        self.map_view = QWebEngineView()
        map_layout.addWidget(self.map_view)
        
        layout.addWidget(info_container, 1)
        layout.addWidget(map_group, 2)
        
        return tab

    def create_diagnostics_tab(self):
        """Tab con herramientas de diagnóstico de red."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        
        self.ping_btn = QPushButton("📡 Ping")
        self.ping_btn.clicked.connect(self.run_ping)
        
        self.traceroute_btn = QPushButton("🛣️ Traceroute")
        self.traceroute_btn.clicked.connect(self.run_traceroute)
        
        self.nslookup_btn = QPushButton("🔍 DNS Lookup")
        self.nslookup_btn.clicked.connect(self.run_nslookup)
        
        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.clicked.connect(self.clear_diagnostics)
        
        buttons_layout.addWidget(self.ping_btn)
        buttons_layout.addWidget(self.traceroute_btn)
        buttons_layout.addWidget(self.nslookup_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.clear_btn)
        
        layout.addLayout(buttons_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximumHeight(4)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Output area
        output_group = QGroupBox("💻 Diagnostic Output")
        output_layout = QVBoxLayout(output_group)
        
        self.diagnostic_output = QTextEdit()
        self.diagnostic_output.setReadOnly(True)
        self.diagnostic_output.setFont(QFont("Consolas", 10))
        
        output_layout.addWidget(self.diagnostic_output)
        layout.addWidget(output_group)
        
        return tab

    def create_security_tab(self):
        """Tab con información de seguridad y reputación."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Descripción
        desc = QLabel(
            "Check the reputation of this IP address using various security services.\n"
            "Click on any button to open the service in your browser."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Reputación
        reputation_group = QGroupBox("🔐 IP Reputation Services")
        rep_layout = QVBoxLayout(reputation_group)
        
        urls = self.diagnostics.get_reputation_check_url(self.ip_address)
        
        for service_name, url in urls.items():
            btn = QPushButton(f"🌐 Check on {service_name}")
            btn.clicked.connect(lambda checked, u=url: webbrowser.open(u))
            rep_layout.addWidget(btn)
        
        layout.addWidget(reputation_group)
        
        # Consejos de seguridad
        tips_group = QGroupBox("💡 Security Tips")
        tips_layout = QVBoxLayout(tips_group)
        
        tips_text = QTextEdit()
        tips_text.setReadOnly(True)
        tips_text.setMaximumHeight(200)
        tips_text.setHtml("""
        <ul>
            <li><b>Connections to unknown IPs:</b> Investigate processes making these connections.</li>
            <li><b>High number of connections:</b> Could indicate malware or data exfiltration.</li>
            <li><b>Unusual ports:</b> Check if the port is expected for the application.</li>
            <li><b>Foreign countries:</b> Verify if your applications should connect internationally.</li>
            <li><b>Use reputation services:</b> Check if the IP is known for malicious activity.</li>
        </ul>
        """)
        
        tips_layout.addWidget(tips_text)
        layout.addWidget(tips_group)
        
        layout.addStretch()
        
        return tab

    def fetch_geolocation_data(self):
        """Obtiene datos de geolocalización de la IP."""
        # Verificar IPs locales
        if self.is_local_ip():
            self.add_info_row("Status", "Local Network Address")
            self.add_info_row("Note", "Geolocation not applicable for local IPs")
            self.map_view.setHtml(self.get_local_ip_html())
            return

        try:
            url = f"http://ip-api.com/json/{self.ip_address}"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                
            if data.get("status") == "success":
                self.add_info_row("🌍 Country", data.get("country", "-"))
                self.add_info_row("🏙️ City", data.get("city", "-"))
                self.add_info_row("📍 Region", data.get("regionName", "-"))
                self.add_info_row("🏢 ISP", data.get("isp", "-"))
                self.add_info_row("🏛️ Organization", data.get("org", "-"))
                self.add_info_row("🕐 Timezone", data.get("timezone", "-"))
                
                lat = data.get("lat")
                lon = data.get("lon")
                self.add_info_row("📐 Coordinates", f"{lat}, {lon}")
                
                self.load_map(lat, lon)
            else:
                self.add_info_row("Status", "Failed to get geolocation")
                self.map_view.setHtml(self.get_error_html())
                
        except Exception as e:
            self.add_info_row("Error", str(e))
            self.map_view.setHtml(self.get_error_html())

    def is_local_ip(self):
        """Verifica si la IP es local."""
        return (self.ip_address.startswith("127.") or 
                self.ip_address.startswith("192.168.") or 
                self.ip_address.startswith("10.") or
                self.ip_address.startswith("172.") or
                self.ip_address == "0.0.0.0" or 
                self.ip_address == "::")

    def add_info_row(self, label, value):
        """Agrega una fila al formulario de información."""
        value_label = QLabel(str(value))
        value_label.setWordWrap(True)
        value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.info_form.addRow(f"<b>{label}:</b>", value_label)

    def load_map(self, lat, lon):
        """Carga el mapa de OpenStreetMap."""
        delta = 0.05
        bbox = f"{lon-delta},{lat-delta},{lon+delta},{lat+delta}"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body, html {{ margin: 0; padding: 0; height: 100%; overflow: hidden; }}
                iframe {{ width: 100%; height: 100%; border: none; }}
            </style>
        </head>
        <body>
            <iframe src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&layer=mapnik&marker={lat},{lon}"></iframe>
        </body>
        </html>
        """
        self.map_view.setHtml(html)

    def get_local_ip_html(self):
        """HTML para IPs locales."""
        return """
        <html>
        <body style='display: flex; align-items: center; justify-content: center; height: 100%; background: #1a1a2e; color: #eaeaea; font-family: sans-serif;'>
            <div style='text-align: center;'>
                <h2>🏠 Local IP Address</h2>
                <p>This is a local network address.<br>Geolocation is not available.</p>
            </div>
        </body>
        </html>
        """

    def get_error_html(self):
        """HTML para errores."""
        return """
        <html>
        <body style='display: flex; align-items: center; justify-content: center; height: 100%; background: #1a1a2e; color: #eaeaea; font-family: sans-serif;'>
            <div style='text-align: center;'>
                <h2>⚠️ Map Unavailable</h2>
                <p>Could not load location map.</p>
            </div>
        </body>
        </html>
        """

    def run_ping(self):
        """Ejecuta ping en un thread separado."""
        self.append_diagnostic(f"\n🔄 Running ping to {self.ip_address}...\n")
        self.set_buttons_enabled(False)
        self.show_progress()
        
        self.worker = DiagnosticWorker(self.diagnostics.ping, self.ip_address, 4)
        self.worker.finished.connect(self.on_diagnostic_finished)
        self.worker.start()

    def run_traceroute(self):
        """Ejecuta traceroute en un thread separado."""
        self.append_diagnostic(f"\n🔄 Running traceroute to {self.ip_address}...\n")
        self.set_buttons_enabled(False)
        self.show_progress()
        
        self.worker = DiagnosticWorker(self.diagnostics.traceroute, self.ip_address)
        self.worker.finished.connect(self.on_diagnostic_finished)
        self.worker.start()

    def run_nslookup(self):
        """Ejecuta nslookup."""
        self.append_diagnostic(f"\n🔄 Running DNS lookup for {self.ip_address}...\n")
        self.set_buttons_enabled(False)
        self.show_progress()
        
        self.worker = DiagnosticWorker(self.diagnostics.nslookup, self.ip_address)
        self.worker.finished.connect(self.on_diagnostic_finished)
        self.worker.start()

    def on_diagnostic_finished(self, success, output):
        """Callback cuando termina un diagnóstico."""
        self.hide_progress()
        self.set_buttons_enabled(True)
        
        status = "✅ Success" if success else "❌ Failed"
        self.append_diagnostic(f"{status}\n")
        self.append_diagnostic(output)
        self.append_diagnostic("\n" + "="*60 + "\n")

    def append_diagnostic(self, text):
        """Agrega texto al output de diagnósticos."""
        self.diagnostic_output.append(text)

    def clear_diagnostics(self):
        """Limpia el output de diagnósticos."""
        self.diagnostic_output.clear()

    def set_buttons_enabled(self, enabled):
        """Habilita/deshabilita botones de diagnóstico."""
        self.ping_btn.setEnabled(enabled)
        self.traceroute_btn.setEnabled(enabled)
        self.nslookup_btn.setEnabled(enabled)

    def show_progress(self):
        """Muestra la barra de progreso indeterminada."""
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.show()

    def hide_progress(self):
        """Oculta la barra de progreso."""
        self.progress_bar.hide()
        self.progress_bar.setRange(0, 100)

    def apply_theme(self):
        """Aplica el tema visual."""
        stylesheet = ModernTheme.get_stylesheet(self.theme)
        
        # Estilos adicionales específicos para esta ventana
        extra_styles = """
        #header {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #e94560, stop:1 #0f3460);
            border-radius: 0px;
            color: white;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #2c3e50;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
        }
        """
        
        self.setStyleSheet(stylesheet + extra_styles)
