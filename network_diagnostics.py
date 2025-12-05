"""
Utilidades de diagnóstico de red.
Ejecuta comandos como ping, traceroute, whois, etc.
"""
import subprocess
import platform

class NetworkDiagnostics:
    """
    Clase para ejecutar herramientas de diagnóstico de red.
    """
    
    @staticmethod
    def ping(host, count=4):
        """
        Ejecuta ping a un host.
        
        Args:
            host: IP o hostname a hacer ping
            count: Número de paquetes a enviar
            
        Returns:
            Tupla (success: bool, output: str)
        """
        try:
            # Windows usa -n, Linux/Mac usan -c
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            
            # Crear banderas para ocultar la ventana de consola en Windows
            creationflags = 0
            if platform.system() == "Windows":
                creationflags = 0x08000000  # CREATE_NO_WINDOW
            
            result = subprocess.run(
                ['ping', param, str(count), host],
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=creationflags
            )
            
            return (result.returncode == 0, result.stdout)
            
        except subprocess.TimeoutExpired:
            return (False, "Ping timeout - Host may be unreachable or blocking ICMP")
        except Exception as e:
            return (False, f"Error executing ping: {str(e)}")
    
    @staticmethod
    def traceroute(host):
        """
        Ejecuta traceroute/tracert a un host.
        
        Args:
            host: IP o hostname
            
        Returns:
            Tupla (success: bool, output: str)
        """
        try:
            # Windows usa tracert, Linux/Mac usan traceroute
            cmd = 'tracert' if platform.system().lower() == 'windows' else 'traceroute'
            
            creationflags = 0
            if platform.system() == "Windows":
                creationflags = 0x08000000
            
            result = subprocess.run(
                [cmd, host],
                capture_output=True,
                text=True,
                timeout=60,
                creationflags=creationflags
            )
            
            return (True, result.stdout)
            
        except subprocess.TimeoutExpired:
            return (False, "Traceroute timeout")
        except Exception as e:
            return (False, f"Error executing traceroute: {str(e)}")
    
    @staticmethod
    def nslookup(host):
        """
        Ejecuta nslookup para resolver DNS.
        
        Args:
            host: IP o hostname
            
        Returns:
            Tupla (success: bool, output: str)
        """
        try:
            creationflags = 0
            if platform.system() == "Windows":
                creationflags = 0x08000000
            
            result = subprocess.run(
                ['nslookup', host],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=creationflags
            )
            
            return (True, result.stdout)
            
        except Exception as e:
            return (False, f"Error executing nslookup: {str(e)}")
    
    @staticmethod
    def port_scan_basic(host, port):
        """
        Verifica si un puerto específico está abierto usando telnet.
        
        Args:
            host: IP o hostname
            port: Puerto a verificar
            
        Returns:
            Tupla (success: bool, message: str)
        """
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, int(port)))
            sock.close()
            
            if result == 0:
                return (True, f"Port {port} is OPEN")
            else:
                return (False, f"Port {port} is CLOSED or filtered")
                
        except Exception as e:
            return (False, f"Error scanning port: {str(e)}")
    
    @staticmethod
    def get_reputation_check_url(ip):
        """
        Devuelve URLs de servicios de reputación de IP.
        
        Args:
            ip: Dirección IP
            
        Returns:
            Dict con nombres y URLs de servicios
        """
        return {
            "AbuseIPDB": f"https://www.abuseipdb.com/check/{ip}",
            "VirusTotal": f"https://www.virustotal.com/gui/ip-address/{ip}",
            "Shodan": f"https://www.shodan.io/host/{ip}",
            "ThreatCrowd": f"https://www.threatcrowd.org/ip.php?ip={ip}",
            "IPVoid": f"https://www.ipvoid.com/ip-blacklist-check/",
            "Whois": f"https://who.is/whois-ip/ip-address/{ip}"
        }
