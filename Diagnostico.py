import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import psutil
import platform
import threading
import GPUtil
import time
import socket 
from tkinter import filedialog
import winreg 
import subprocess 
import os 
import datetime

try:
    import winsound 
except ImportError:
    pass

try:
    import wmi
    import pythoncom
except ImportError:
    pass

try:
    import cv2
except ImportError:
    pass

class TechMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TechMaster Pro Ultimate - Diagnóstico Avanzado")
        self.root.geometry("1050x750")
        self.root.configure(bg="#eef2f5")
        
        
        self.cpu_name = "Cargando..."
        self.system_model = "Cargando..."
        self.gpu_name = "Cargando..."

        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background="#eef2f5")
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[15, 5])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        self.tab_monitor = ttk.Frame(self.notebook)
        self.tab_hardware = ttk.Frame(self.notebook)
        self.tab_red = ttk.Frame(self.notebook) 
        self.tab_opt = ttk.Frame(self.notebook) 
        self.tab_errores = ttk.Frame(self.notebook)
        self.tab_pruebas = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_monitor, text="🖥️ Escáner en Tiempo Real")
        self.notebook.add(self.tab_hardware, text="⚙️ Specs Detalladas")
        self.notebook.add(self.tab_red, text="🌐 Red y Conectividad")
        self.notebook.add(self.tab_opt, text="🚀 Optimización (Arranque)")
        self.notebook.add(self.tab_errores, text="🚨 Auditoría y Errores")
        self.notebook.add(self.tab_pruebas, text="🎮 Pruebas Físicas")
        
        self.build_monitor_tab()
        self.build_hardware_tab()
        self.build_red_tab()
        self.build_opt_tab()
        self.build_errores_tab()
        self.build_pruebas_tab()
        

        self.running = True
        threading.Thread(target=self.background_deep_scan, daemon=True).start()
        self.update_monitor()


    def build_monitor_tab(self):
        self.lbl_equipo = tk.Label(self.tab_monitor, text="Analizando sistema...", font=("Segoe UI", 14, "bold"), bg="#eef2f5", fg="#2c3e50")
        self.lbl_equipo.pack(pady=10)

        main_frame = tk.Frame(self.tab_monitor, bg="#eef2f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.lbl_cpu = self.create_card(main_frame, "PROCESADOR (CPU)", 0, 0)
        self.lbl_ram = self.create_card(main_frame, "MEMORIA RAM", 0, 1)
        self.lbl_disk = self.create_card(main_frame, "ALMACENAMIENTO (C:)", 1, 0)
        self.lbl_bat = self.create_card(main_frame, "BATERÍA / RED", 1, 1)

   
        btn_stress = tk.Button(self.tab_monitor, text="🔥 Iniciar Test de Estrés de CPU (10 Segundos)", font=("Segoe UI", 11, "bold"), bg="#e74c3c", fg="white", command=self.iniciar_stress_test)
        btn_stress.pack(pady=10)

    def iniciar_stress_test(self):
        respuesta = messagebox.askyesno("Prueba de Estrés", "¿Deseas poner la CPU al 100% de carga durante 10 segundos?\nEsto probará si hay problemas de sobrecalentamiento.")
        if respuesta:
            def carga_cpu():
                t_end = time.time() + 10
                while time.time() < t_end:
                    pass 
            

            for _ in range(psutil.cpu_count()):
                threading.Thread(target=carga_cpu, daemon=True).start()
            messagebox.showinfo("Prueba en proceso", "La CPU estará al 100% durante 10 segundos. ¡Mira el monitor!")

    def create_card(self, parent, title, row, col):
        frame = tk.Frame(parent, bg="white", bd=1, relief=tk.RIDGE)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(frame, text=title, font=("Segoe UI", 11, "bold"), bg="white", fg="#0078D7").pack(pady=(10,0))
        lbl_val = tk.Label(frame, text="Calculando...", font=("Consolas", 11), bg="white", fg="#34495e", justify=tk.LEFT)
        lbl_val.pack(pady=10, padx=15, anchor="w")
        return lbl_val

    def update_monitor(self):
        if not self.running: return
        
        cpu_pct = psutil.cpu_percent()
        freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
        self.lbl_cpu.config(text=f"Modelo: {self.cpu_name}\n"
                                 f"Uso Actual: {cpu_pct}%\n"
                                 f"Frecuencia: {freq:.0f} MHz\n"
                                 f"Núcleos/Hilos: {psutil.cpu_count(logical=False)} / {psutil.cpu_count()}")
        
        ram = psutil.virtual_memory()
        self.lbl_ram.config(text=f"En Uso: {ram.percent}%\n"
                                 f"Ocupado: {ram.used // (1024**3)} GB\n"
                                 f"Libre: {ram.available // (1024**3)} GB\n"
                                 f"Total Instalada: {ram.total // (1024**3)} GB")
        
        try:
            disk = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
            self.lbl_disk.config(text=f"Uso de Disco Principal: {disk.percent}%\n"
                                      f"Espacio Libre: {disk.free // (1024**3)} GB\n"
                                      f"Espacio Total: {disk.total // (1024**3)} GB")
        except: pass
        
        info_bat = ""
        bat = psutil.sensors_battery()
        if bat:
            estado = "Conectado" if bat.power_plugged else "En uso (Batería)"
            info_bat += f"Batería: {bat.percent}% ({estado})\n"
        else:
            info_bat += "Batería: No detectada (PC Escritorio)\n"

        net = psutil.net_io_counters()
        info_bat += f"\nTráfico Red Descarga: {net.bytes_recv // (1024**2)} MB\n"
        info_bat += f"Tráfico Red Subida: {net.bytes_sent // (1024**2)} MB"
        self.lbl_bat.config(text=info_bat)


        uptime_secs = time.time() - psutil.boot_time()
        horas = int(uptime_secs // 3600)
        minutos = int((uptime_secs % 3600) // 60)
        

        try:
            self.lbl_equipo.config(text=f"💻 EQUIPO: {self.system_model}   |   ⏱️ Tiempo encendido: {horas}h {minutos}m")
        except: pass

        self.root.after(1500, self.update_monitor)

#red y conectividad :v
    def build_red_tab(self):
        lbl_aviso = tk.Label(self.tab_red, text="Analizando adaptadores de red, Direcciones MAC e IPs...", font=("Segoe UI", 10, "italic"))
        lbl_aviso.pack(pady=5)
        
        btn_refresh_red = tk.Button(self.tab_red, text="🔄 Refrescar Datos de Red", font=("Segoe UI", 10), bg="#0078D7", fg="white", command=self.load_network_data)
        btn_refresh_red.pack(pady=5)


        btn_ping = tk.Button(self.tab_red, text="🌍 Test de Estabilidad (Ping a Google)", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", command=self.test_ping)
        btn_ping.pack(pady=5)

        self.red_text = scrolledtext.ScrolledText(self.tab_red, font=("Consolas", 11), bg="#1e293b", fg="#60a5fa", padx=15, pady=15)
        self.red_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_network_data()

    def load_network_data(self):
        self.red_text.config(state=tk.NORMAL)
        self.red_text.delete(1.0, tk.END)
        info = "================ INFORMACIÓN DE RED =================\n\n"
        
        try:
            nombre_equipo = socket.gethostname()
            ip_local = socket.gethostbyname(nombre_equipo)
            info += f"  Nombre del Equipo en Red: {nombre_equipo}\n"
            info += f"  IP Principal del Equipo:  {ip_local}\n\n"
            info += "[ ADAPTADORES FÍSICOS Y VIRTUALES ]\n"

            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()

            for interface_name, interface_addresses in interfaces.items():
                is_up = stats[interface_name].isup if interface_name in stats else False
                estado = "ACTIVO / CONECTADO" if is_up else "Desconectado"
                
                info += f"  Adaptador: {interface_name} ({estado})\n"
                
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        info += f"   ├─ IPv4: {address.address}\n"
                        info += f"   ├─ Máscara de Subred: {address.netmask}\n"
                    elif str(address.family) == 'AddressFamily.AF_LINK': # Aquí sacamos la MAC Address
                        info += f"   └─ MAC Address (Física): {address.address.upper().replace('-', ':')}\n"
                info += "  ---------------------------------------------------\n"
                
        except Exception as e:
            info += f"Error al cargar información de red: {e}"

        self.red_text.insert(tk.END, info)
        self.red_text.config(state=tk.DISABLED)


    def test_ping(self):
        self.red_text.config(state=tk.NORMAL)
        self.red_text.insert(tk.END, "\nRealizando Test de Ping (8.8.8.8)... Espere por favor...\n")
        self.red_text.see(tk.END)
        self.red_text.config(state=tk.DISABLED)
        
        def run_ping():
            try:
                # '-n 4' envía 4 paquetes en Windows
                output = subprocess.check_output(["ping", "-n", "4", "8.8.8.8"], stderr=subprocess.STDOUT, universal_newlines=True)
                resultado = f"\n[ RESULTADOS DEL PING ]\n{output}\n"
            except Exception as e:
                resultado = f"\n[ ERROR EN PING ]\nNo hay conexión a internet o el comando falló: {e}\n"
            
            self.root.after(0, lambda: self.update_red_ui_append(resultado))
            
        threading.Thread(target=run_ping, daemon=True).start()

    def update_red_ui_append(self, texto):
        self.red_text.config(state=tk.NORMAL)
        self.red_text.insert(tk.END, texto)
        self.red_text.see(tk.END)
        self.red_text.config(state=tk.DISABLED)

#optimizacion
    def build_opt_tab(self):
        lbl_aviso = tk.Label(self.tab_opt, text="Programas que se inician automáticamente con Windows (Ralentizan el encendido):", font=("Segoe UI", 10, "bold"))
        lbl_aviso.pack(pady=10)
        
        btn_refresh = tk.Button(self.tab_opt, text="🔄 Analizar Arranque", font=("Segoe UI", 10), bg="#8e44ad", fg="white", command=self.load_startup_programs)
        btn_refresh.pack(pady=5)

        self.opt_text = scrolledtext.ScrolledText(self.tab_opt, font=("Consolas", 10), bg="#1e1e1e", fg="#e0e0e0", padx=15, pady=15)
        self.opt_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_startup_programs()

    def load_startup_programs(self):
        self.opt_text.config(state=tk.NORMAL)
        self.opt_text.delete(1.0, tk.END)
        info = "================ PROGRAMAS DE INICIO (AUTOSTART) ================\n"
        info += "Si la PC arranca lento, el cliente debe deshabilitar estos programas en el Administrador de Tareas.\n\n"
        
        rutas_registro = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "Usuario Actual"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "Todos los Usuarios")
        ]
        
        for hkey, ruta, contexto in rutas_registro:
            info += f"[ Registro: {contexto} ]\n"
            try:
                clave = winreg.OpenKey(hkey, ruta, 0, winreg.KEY_READ)
                contador = 0
                try:
                    while True:
                        nombre, valor, tipo = winreg.EnumValue(clave, contador)
                        info += f"  📌 {nombre}\n      └─ Ruta: {valor}\n"
                        contador += 1
                except OSError:
                    pass # Fin de los valores en esta carpeta
                winreg.CloseKey(clave)
                
                if contador == 0:
                    info += "  (Ningún programa detectado en esta rama)\n"
            except Exception as e:
                info += f"  (Carpeta no accesible o vacía)\n"
            info += "\n"
            
        self.opt_text.insert(tk.END, info)
        self.opt_text.config(state=tk.DISABLED)

# los errores
    def background_deep_scan(self):
        try:
            pythoncom.CoInitialize()
            c = wmi.WMI()
            try:
                sys_info = c.Win32_ComputerSystem()[0]
                self.system_model = f"{sys_info.Manufacturer} {sys_info.Model}"
                cpu_info = c.Win32_Processor()[0]
                self.cpu_name = cpu_info.Name.strip()
                self.root.after(0, lambda: self.lbl_equipo.config(text=f"💻 EQUIPO: {self.system_model}"))
            except Exception as e: print("Error cargando nombres:", e)

            self.generate_hardware_report(c)
            self.audit_system_errors(c)
        except Exception as e:
            error_msg = f"Error crítico al leer WMI: {e}\n(Ejecute como Administrador)"
            self.root.after(0, lambda: self.hw_text.insert(tk.END, error_msg))

#Aqui dice toda la info
    def build_hardware_tab(self):
        self.hw_text = scrolledtext.ScrolledText(self.tab_hardware, font=("Consolas", 10), bg="#1e1e1e", fg="#5ce1e6", padx=10, pady=10)
        self.hw_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.hw_text.insert(tk.END, "Escaneando marcas, almacenamiento y salud de batería...\n")
        
        btn_exportar = tk.Button(self.tab_hardware, text="💾 Guardar Reporte en TXT", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", command=self.exportar_reporte)
        btn_exportar.pack(pady=5)

    def exportar_reporte(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt")], title="Guardar Reporte Técnico", initialfile=f"Reporte_{self.system_model}.txt")
        if not filepath: return
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.hw_text.get(1.0, tk.END))
            messagebox.showinfo("Éxito", "Reporte guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def generate_hardware_report(self, wmi_client):
        info = "================ REPORTE TÉCNICO AVANZADO ================\n\n"
        
        info += "[ LICENCIA DE WINDOWS ]\n"
        try:
            os_info = wmi_client.Win32_OperatingSystem()[0]
            info += f"  Sistema: {os_info.Caption}\n"
            try:
                lic = wmi_client.SoftwareLicensingService()[0]
                if lic.OA3xOriginalProductKey:
                    info += f"  Clave de Producto (OEM BIOS): {lic.OA3xOriginalProductKey}\n"
                else:
                    info += "  Clave de Producto: No hay clave OEM en la BIOS (Licencia Digital/Retail)\n"
            except: info += "  Clave de Producto: No detectada.\n"
        except: pass
        info += "  ------------------------\n\n"

        info += "[ PLACA BASE (MOTHERBOARD) ]\n"
        try:
            board = wmi_client.Win32_BaseBoard()[0]
            info += f"  Fabricante: {board.Manufacturer}\n"
            info += f"  Modelo Exacto: {board.Product}\n"
            info += f"  Versión: {board.Version}\n"
            info += f"  Número de Serie (SN): {board.SerialNumber}\n\n"
        except: info += "  No disponible.\n\n"

        info += "[ SALUD DE LA BATERÍA ]\n"
        try:
            wmi_root = wmi.WMI(namespace="wmi")
            static_data = wmi_root.BatteryStaticData()
            full_data = wmi_root.BatteryFullChargedCapacity()
            
            if static_data and full_data:
                design_cap = static_data[0].DesignedCapacity
                full_cap = full_data[0].FullChargedCapacity
                
                if design_cap > 0:
                    health_pct = (full_cap / design_cap) * 100
                    wear_level = 100 - health_pct
                    info += f"  Capacidad de Fábrica (Nueva):  {design_cap} mWh\n"
                    info += f"  Capacidad Máxima (Actual):     {full_cap} mWh\n"
                    info += f"  Salud Restante:                {health_pct:.1f}%\n"
                    info += f"  Nivel de Desgaste:             {wear_level:.1f}%\n"
                    if wear_level > 35: info += "  [!] ALERTA: Batería muy degradada, requiere reemplazo pronto.\n"
                else: info += "  Los sensores no reportan datos válidos.\n"
            else: info += "  No se encontraron registros de batería.\n"
        except: info += "  Batería no detectada (Equipo de escritorio o fallo sensor).\n"
        info += "  ------------------------\n\n"

        info += "[ MÓDULOS FÍSICOS DE MEMORIA RAM ]\n"
        for ram in wmi_client.Win32_PhysicalMemory():
            capacidad_gb = int(ram.Capacity) // (1024**3)
            info += f"  Fabricante/Marca:   {ram.Manufacturer}\n"
            info += f"  Modelo (Nº Parte):  {ram.PartNumber.strip() if ram.PartNumber else 'Desconocido'}\n"
            info += f"  Número de Serie:    {ram.SerialNumber.strip() if ram.SerialNumber else 'Desconocido'}\n"
            info += f"  Capacidad:          {capacidad_gb} GB\n"
            info += f"  Velocidad Actual:   {ram.Speed} MHz\n"
            info += f"  Ranura (Socket):    {ram.DeviceLocator}\n"
            info += "  ------------------------\n"
        info += "\n"

        info += "[ ALMACENAMIENTO (DISCOS Y UNIDADES) ]\n"
        tipo_discos = {}
        try:
            wmi_storage = wmi.WMI(namespace="Microsoft\\Windows\\Storage")
            for pdisk in wmi_storage.MSFT_PhysicalDisk():
                mtype = "Desconocido"
                if pdisk.MediaType == 3: mtype = "HDD (Disco Mecánico)"
                elif pdisk.MediaType == 4: mtype = "SSD (Estado Sólido)"
                tipo_discos[pdisk.FriendlyName.strip()] = mtype
        except: pass

        for disk in wmi_client.Win32_DiskDrive():
            size_gb = int(disk.Size) // (1024**3) if disk.Size else 0
            modelo_disco = disk.Model.strip()
            tipo_detectado = tipo_discos.get(modelo_disco, "No identificado (SATA/NVMe estándar)")
            info += f"  Marca / Modelo:     {modelo_disco}\n"
            info += f"  Tecnología:         {tipo_detectado}\n"
            info += f"  Número de Serie:    {disk.SerialNumber.strip() if disk.SerialNumber else 'Oculto'}\n"
            info += f"  Capacidad Total:    {size_gb} GB\n"
            info += f"  Interfaz Lógica:    {disk.InterfaceType}\n"
            info += "  ------------------------\n"
        info += "\n"
        
        info += "[ TARJETAS GRÁFICAS (GPU) ]\n"
        for gpu in wmi_client.Win32_VideoController():
            gpu_name = gpu.Name
            vram_mb = "Desconocida"
            if gpu.AdapterRAM:
                vram_bytes = int(gpu.AdapterRAM)
                if vram_bytes < 0 or vram_bytes == 4294967295: vram_mb = "+4096 MB (Supera lectura nativa Windows)"
                else: vram_mb = str(vram_bytes // (1024**2)) + " MB"
            info += f"  Nombre: {gpu_name}\n"
            info += f"  VRAM (Windows): {vram_mb}\n"
            info += "  ------------------------\n"
            
        try:
            gpus_nvidia = GPUtil.getGPUs()
            if gpus_nvidia:
                info += "  [ LECTURA DE HARDWARE EXACTA (NVIDIA) ]\n"
                for g in gpus_nvidia:
                    info += f"  Chip: {g.name}\n"
                    info += f"  VRAM Física Real: {int(g.memoryTotal)} MB\n"
                    info += "  ------------------------\n"
        except: pass

        self.root.after(0, self.update_hw_ui, info)

    def update_hw_ui(self, info):
        self.hw_text.delete(1.0, tk.END)
        self.hw_text.insert(tk.END, info)
        self.hw_text.config(state=tk.DISABLED)
# cosa que no recuerdo XD
    def build_errores_tab(self):
        lbl_aviso = tk.Label(self.tab_errores, text="Escaneando el Administrador de Dispositivos y estado S.M.A.R.T...", font=("Segoe UI", 10, "italic"))
        lbl_aviso.pack(pady=5)
        self.err_text = scrolledtext.ScrolledText(self.tab_errores, font=("Consolas", 11), bg="#111827", fg="#f87171", padx=15, pady=15)
        self.err_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.err_text.tag_config("verde", foreground="#4ade80")
        self.err_text.tag_config("rojo", foreground="#f87171")
        self.err_text.tag_config("amarillo", foreground="#facc15")

    def audit_system_errors(self, wmi_client):
        errores_encontrados = 0
        reporte_errores = [("============= AUDITORÍA DE SALUD DEL SISTEMA =============\n\n", "")]

        reporte_errores.append(("[ ESCÁNER DE DISCOS DUROS ]\n", ""))
        for disk in wmi_client.Win32_DiskDrive():
            if disk.Status and disk.Status.upper() != "OK":
                reporte_errores.append((f"  [ALERTA CRÍTICA] Disco: {disk.Model}\n  Estado SMART: {disk.Status} -> ¡POSIBLE FALLO INMINENTE!\n", "rojo"))
                errores_encontrados += 1
            else:
                reporte_errores.append((f"  [OK] Disco: {disk.Model} -> Salud Normal.\n", "verde"))
        reporte_errores.append(("\n", ""))

      
        reporte_errores.append(("[ ESCÁNER DE PANTALLAZOS AZULES (BSOD) ]\n", ""))
        minidump_dir = r"C:\Windows\Minidump"
        try:
            if os.path.exists(minidump_dir):
                dumps = os.listdir(minidump_dir)
                if dumps:
                    errores_encontrados += 1
                    reporte_errores.append((f"  [ALERTA] Se encontraron {len(dumps)} archivo(s) de error fatal en Minidump.\n", "rojo"))
                    reporte_errores.append(("  El equipo ha sufrido pantallazos azules o reinicios forzados recientemente.\n", "amarillo"))
                else:
                    reporte_errores.append(("  [OK] No se detectaron pantallazos azules recientes.\n", "verde"))
            else:
                reporte_errores.append(("  [OK] Carpeta Minidump vacía o no existe (Sistema estable).\n", "verde"))
        except Exception as e:
            reporte_errores.append((f"  No se pudo leer la carpeta de volcados (requiere Administrador).\n", "amarillo"))
        reporte_errores.append(("\n", ""))

        reporte_errores.append(("[ ESCÁNER DE DISPOSITIVOS Y DRIVERS ]\n", ""))
        dispositivos_con_error = wmi_client.query("SELECT * FROM Win32_PnPEntity WHERE ConfigManagerErrorCode != 0")
        
        if not dispositivos_con_error:
            reporte_errores.append(("  [OK] No se detectaron conflictos de hardware o drivers rotos.\n", "verde"))
        else:
            for dev in dispositivos_con_error:
                errores_encontrados += 1
                codigo = dev.ConfigManagerErrorCode
                motivo = "Error desconocido."
                if codigo == 22: motivo = "El dispositivo está deshabilitado."
                elif codigo == 28: motivo = "Faltan los drivers."
                elif codigo == 43: motivo = "Problema físico o de driver."
                elif codigo == 10: motivo = "El dispositivo no puede iniciar."
                reporte_errores.append((f"  [FALLO ENCONTRADO] Dispositivo: {dev.Name}\n", "amarillo"))
                reporte_errores.append((f"  └─ Código de Error: {codigo} - {motivo}\n\n", "rojo"))

        reporte_errores.append(("\n==========================================================\n", ""))
        if errores_encontrados == 0:
            reporte_errores.append(("ESTADO: EXCELENTE. El hardware funciona correctamente.", "verde"))
        else:
            reporte_errores.append((f"ESTADO: ALERTA. Se encontraron {errores_encontrados} problema(s).", "rojo"))

        self.root.after(0, self.update_err_ui, reporte_errores)

    def update_err_ui(self, reporte_errores):
        self.err_text.delete(1.0, tk.END)
        for texto, etiqueta in reporte_errores:
            if etiqueta: self.err_text.insert(tk.END, texto, etiqueta)
            else: self.err_text.insert(tk.END, texto)
        self.err_text.config(state=tk.DISABLED)

    def build_pruebas_tab(self):
     
        frame_top = tk.Frame(self.tab_pruebas)
    
        frame_top.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
      
        frame_teclado = tk.LabelFrame(frame_top, text=" Prueba de Teclado ", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
   
        frame_teclado.pack(side=tk.LEFT, fill=tk.X, expand=False, anchor="n", padx=5)
        tk.Label(frame_teclado, text="Presiona cualquier tecla:").pack()
        self.lbl_tecla = tk.Label(frame_teclado, text="Esperando...", font=("Consolas", 14, "bold"), fg="#e74c3c")
        self.lbl_tecla.pack(pady=5)
        self.root.bind('<Key>', self.tecla_presionada)

       
        frame_mouse = tk.LabelFrame(frame_top, text=" Prueba de Mouse ", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
       
        frame_mouse.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.lbl_mouse = tk.Label(frame_mouse, text="Mueve el ratón aquí", font=("Consolas", 10))
        self.lbl_mouse.pack()
       
        self.canvas_mouse = tk.Canvas(frame_mouse, bg="#e8f8f5", height=250)
        self.canvas_mouse.pack(fill=tk.BOTH, expand=True, pady=5)
        self.canvas_mouse.bind('<Motion>', self.mouse_movido)
        self.canvas_mouse.bind('<Button-1>', lambda e: self.mouse_click("Izq"))
        self.canvas_mouse.bind('<Button-3>', lambda e: self.mouse_click("Der"))

       
        frame_camara = tk.LabelFrame(self.tab_pruebas, text=" Prueba de Cámara Web ", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        frame_camara.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(frame_camara, text="📷 Iniciar Prueba de Cámara", font=("Segoe UI", 10), bg="#3498db", fg="white", command=self.test_camara).pack(pady=5)

        
        frame_pantalla = tk.LabelFrame(self.tab_pruebas, text=" Prueba de Pantalla (LCD/LED) ", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        frame_pantalla.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(frame_pantalla, text="📺 Iniciar Test de Píxeles Muertos", font=("Segoe UI", 10), bg="#8e44ad", fg="white", command=self.test_pixeles).pack(pady=5)

        
        frame_audio = tk.LabelFrame(self.tab_pruebas, text=" Prueba de Altavoces / Audio ", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        frame_audio.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(frame_audio, text="Enviará un pitido al sistema. Sube el volumen.", font=("Segoe UI", 9)).pack(pady=2)
        tk.Button(frame_audio, text="🔊 Probar Sonido del Sistema", font=("Segoe UI", 10), bg="#f39c12", fg="white", command=self.test_audio).pack(pady=5)

    def test_audio(self):
        if 'winsound' in globals():
            
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            messagebox.showinfo("Prueba de Audio", "¿Escuchaste el sonido?\n\nSi no escuchaste nada, verifica que el volumen no esté en 'Mute' o reinstala los drivers de Realtek/Audio.")
        else:
            messagebox.showerror("Error", "Prueba de audio solo compatible nativamente en Windows.")

    def test_pixeles(self):
        test_win = tk.Toplevel(self.root)
        test_win.attributes('-fullscreen', True)
        test_win.title("Test de Pantalla")
        
        colores = ["white", "black", "red", "green", "blue"]
        indice_color = [0]
        
        lbl_instruccion = tk.Label(test_win, text="Haz clic izquierdo para cambiar de color.\nPresiona 'Escape' para salir.", font=("Segoe UI", 24, "bold"), bg="white", fg="gray")
        lbl_instruccion.pack(expand=True)
        test_win.configure(bg=colores[indice_color[0]])

        def cambiar_color(event):
            lbl_instruccion.pack_forget()
            indice_color[0] = (indice_color[0] + 1) % len(colores)
            test_win.configure(bg=colores[indice_color[0]])

        test_win.bind("<Button-1>", cambiar_color)
        test_win.bind("<Escape>", lambda e: test_win.destroy())

    def tecla_presionada(self, event):
        self.lbl_tecla.config(text=f"[ {event.keysym} ]", fg="#27ae60")

    def mouse_movido(self, event):
        self.lbl_mouse.config(text=f"X={event.x}, Y={event.y}")

    def mouse_click(self, boton):
        self.lbl_mouse.config(text=f"Clic {boton}")
        self.canvas_mouse.config(bg="#d1f2eb")
        self.root.after(200, lambda: self.canvas_mouse.config(bg="#e8f8f5"))

    def test_camara(self):
        if 'cv2' not in globals():
            messagebox.showerror("Error", "Falta librería opencv-python")
            return
        def ejecutar_camara():
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Fallo de Hardware", "No se detectó cámara o está dañada.")
                return
            while True:
                ret, frame = cap.read()
                if not ret: break
                cv2.putText(frame, "Camara OK. Presiona 'Q' o la 'X' para salir.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('Prueba de Camara', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'): break
                if cv2.getWindowProperty('Prueba de Camara', cv2.WND_PROP_VISIBLE) < 1: break
            cap.release()
            cv2.destroyAllWindows()
        threading.Thread(target=ejecutar_camara, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TechMasterApp(root)
    def on_closing():
        app.running = False
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()