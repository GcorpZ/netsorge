import subprocess
import re
import platform

class NetstatMonitor:
    """
    Clase encargada de ejecutar comandos del sistema (netstat, tasklist)
    y procesar su salida para obtener información de red.
    """

    def get_network_connections(self):
        """
        Ejecuta netstat y combina la información con tasklist (en Windows)
        para devolver una lista de diccionarios con los datos.
        """
        connections = []
        
        # 1. Obtener datos de NETSTAT
        # -a: Muestra todas las conexiones y puertos de escucha.
        # -n: Muestra direcciones y números de puerto en formato numérico.
        # -o: Muestra el ID del proceso (PID) dueño de cada conexión.
        try:
            # Ejecutamos el comando y capturamos la salida
            # creationflags=0x08000000 es para evitar que salga la ventana de consola emergente en Windows
            creation_flags = 0
            if platform.system() == "Windows":
                 creation_flags = 0x08000000 # CREATE_NO_WINDOW

            result = subprocess.run(
                ['netstat', '-ano'], 
                capture_output=True, 
                text=True, 
                creationflags=creation_flags
            )
            netstat_output = result.stdout
        except Exception as e:
            print(f"Error ejecutando netstat: {e}")
            return []

        # 2. Obtener datos de TASKLIST (para mapear PID a Nombre de Proceso)
        pid_map = self.get_process_map()

        # 3. Procesar línea por línea la salida de netstat
        lines = netstat_output.splitlines()
        for line in lines:
            line = line.strip()
            # Buscamos líneas que empiecen por TCP o UDP
            if line.startswith('TCP') or line.startswith('UDP'):
                parts = line.split()
                # El formato usual de netstat -ano es:
                # Proto  Local Address          Foreign Address        State           PID
                # TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       445
                
                # A veces UDP no tiene estado, así que la longitud varía
                if len(parts) >= 4:
                    protocol = parts[0]
                    local_addr = parts[1]
                    remote_addr = parts[2]
                    state = "UNKNOWN"
                    pid = "0"

                    if protocol == 'TCP':
                        if len(parts) >= 5:
                            state = parts[3]
                            pid = parts[4]
                    elif protocol == 'UDP':
                        # UDP no suele mostrar estado en netstat -ano estándar de Windows, 
                        # el PID suele ser el último elemento.
                        state = "" # UDP es stateless
                        pid = parts[-1]

                    # Parsear IP y Puerto
                    local_ip, local_port = self.parse_ip_port(local_addr)
                    remote_ip, remote_port = self.parse_ip_port(remote_addr)

                    # Obtener info del proceso usando el PID
                    process_info = pid_map.get(pid, {"name": "Unknown", "mem": "0 K"})

                    # Construir el diccionario de datos para la fila
                    # Mapeamos a los headers que definiste en app.py
                    row_data = {
                        "Process Name": process_info["name"],
                        "Process ID": pid,
                        "Protocol": protocol,
                        "Local Port": local_port,
                        "Local Port Name": "-", # Requiere mapeo de servicios (ej. 80 -> http)
                        "Local Address": local_ip,
                        "Remote Port Name": "-",
                        "Remote Port": remote_port,
                        "Remote Name": "-", # Requiere resolución DNS inversa
                        "Remote Address": remote_ip,
                        "Remote Host Name": "-",
                        "State": state,
                        # Los siguientes campos no los da netstat simple, se necesitarían contadores o sniffers
                        "Sent Byte": "0", 
                        "Received Byte": "0",
                        "Sent Packets": "0",
                        "Received Packets": "0",
                        "Process Path": "-",
                        "Product Name": "-",
                        "File Version": "-",
                        "Company": "-",
                        "Process Create On": "-",
                        "User Name": "-",
                        "Process Services": "-",
                        "Process Attribute": "-",
                        "Added On": "-",
                        "Creation TimeStamp": "-",
                        "Module Filename": "-",
                        "Remote IP Country": "-",
                        "Remote IP ASN": "-",
                        "Remote IP Company": "-",
                        "Windows Tittle": "-"
                    }
                    connections.append(row_data)

        return connections

    def get_process_map(self):
        """
        Ejecuta tasklist para obtener un mapa {PID: InfoProceso}
        """
        mapping = {}
        try:
            creation_flags = 0
            if platform.system() == "Windows":
                 creation_flags = 0x08000000

            # tasklist /FO CSV /NH  -> Formato CSV, No Header
            result = subprocess.run(
                ['tasklist', '/FO', 'CSV', '/NH'], 
                capture_output=True, 
                text=True,
                creationflags=creation_flags
            )
            for line in result.stdout.splitlines():
                if not line.strip(): continue
                # Formato CSV: "Image Name","PID","Session Name","Session#","Mem Usage"
                # Ejemplo: "System Idle Process","0","Services","0","8 K"
                parts = line.split(',')
                if len(parts) >= 5:
                    name = parts[0].strip('"')
                    pid = parts[1].strip('"')
                    mem = parts[4].strip('"')
                    mapping[pid] = {"name": name, "mem": mem}
        except Exception as e:
            print(f"Error ejecutando tasklist: {e}")
        
        return mapping

    def parse_ip_port(self, addr_str):
        """Separa IP y Puerto de strings como 127.0.0.1:80 o [::]:80"""
        if ':' in addr_str:
            # Manejo básico para IPv4 e IPv6
            if '[' in addr_str: # IPv6
                parts = addr_str.split(']:')
                ip = parts[0].replace('[', '')
                port = parts[1] if len(parts) > 1 else ""
            else: # IPv4
                parts = addr_str.split(':')
                port = parts[-1]
                ip = ':'.join(parts[:-1])
            return ip, port
        return addr_str, ""
