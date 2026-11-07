import os
import shutil
import winreg
import subprocess
import tkinter as tk
from tkinter import messagebox

# ==========================================
#          MOTORES DE OPTIMIZACIÓN
# ==========================================
def limpiar_temporales_windows():
    ruta_temp = os.path.join(os.environ['SystemRoot'], 'Temp')
    archivos_borrados = 0
    if os.path.exists(ruta_temp):
        for elemento in os.listdir(ruta_temp):
            try:
                ruta_completa = os.path.join(ruta_temp, elemento)
                if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                    os.unlink(ruta_completa)
                    archivos_borrados += 1
                elif os.path.isdir(ruta_completa):
                    shutil.rmtree(ruta_completa)
                    archivos_borrados += 1
            except Exception: pass
    return archivos_borrados

def limpiar_cache_usuario():
    ruta_cache = os.path.join(os.environ['LOCALAPPDATA'], 'Temp')
    archivos_borrados = 0
    if os.path.exists(ruta_cache):
        for elemento in os.listdir(ruta_cache):
            try:
                ruta_completa = os.path.join(ruta_cache, elemento)
                if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                    os.unlink(ruta_completa)
                    archivos_borrados += 1
                elif os.path.isdir(ruta_completa):
                    shutil.rmtree(ruta_completa)
                    archivos_borrados += 1
            except Exception: pass
    return archivos_borrados

def limpiar_basura_launchers():
    archivos_borrados = 0
    p1 = 'C:\\Program Files (x86)'
    rutas_launchers = {
        "Steam Cache": os.path.join(os.environ.get('PROGRAMFILES(X86)', p1), 'Steam', 'appcache'),
        "Steam Depot": os.path.join(os.environ.get('PROGRAMFILES(X86)', p1), 'Steam', 'depotcache'),
        "Epic Cache": os.path.join(os.environ.get('LOCALAPPDATA', ''), 'EpicGamesLauncher', 'Saved', 'webcache')
    }
    for ruta in rutas_launchers.values():
        if os.path.exists(ruta):
            for elemento in os.listdir(ruta):
                try:
                    ruta_completa = os.path.join(ruta, elemento)
                    if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                        os.unlink(ruta_completa)
                        archivos_borrados += 1
                    elif os.path.isdir(ruta_completa):
                        shutil.rmtree(ruta_completa)
                        archivos_borrados += 1
                except Exception: pass
    return archivos_borrados

def limpiar_shader_cache_y_updates():
    elementos_borrados = 0
    rutas_avanzadas = {
        "DirectX Shader Cache": os.path.join(os.environ.get('LOCALAPPDATA', ''), 'D3DSCache'),
        "DirectX NV Cache": os.path.join(os.environ.get('LOCALAPPDATA', ''), 'NVIDIA', 'DXCache'),
        "Windows Update Download": os.path.join(os.environ['SystemRoot'], 'SoftwareDistribution', 'Download')
    }
    for ruta in rutas_avanzadas.values():
        if os.path.exists(ruta):
            for elemento in os.listdir(ruta):
                try:
                    ruta_completa = os.path.join(ruta, elemento)
                    if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                        os.unlink(ruta_completa)
                        elementos_borrados += 1
                    elif os.path.isdir(ruta_completa):
                        shutil.rmtree(ruta_completa)
                        elementos_borrados += 1
                except Exception: pass
    return elementos_borrados

def aplicar_telemetria(modo):
    ruta_tel = r"SOFTWARE\Policies\Microsoft\Windows\DataCollection"
    try:
        clave_tel = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, ruta_tel, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(clave_tel, "AllowTelemetry", modo, winreg.REG_DWORD, 0)
        winreg.CloseKey(clave_tel)
        return True
    except PermissionError:
        return "admin_error"
    except Exception:
        return False

# ==========================================
#       ACCIONES DE LOS BOTONES (LÓGICA)
# ==========================================
def accion_super_limpieza():
    arch_win = limpiar_temporales_windows()
    arch_usr = limpiar_cache_usuario()
    arch_launchers = limpiar_basura_launchers()
    arch_avanzados = limpiar_shader_cache_y_updates()
    total = arch_win + arch_usr + arch_launchers + arch_avanzados
    messagebox.showinfo("Limpieza Suprema v2.0", f"Modulo 1 Completado!\n\nSe purgaron un total de {total} archivos basura.")

def accion_maximo_gaming():
    res_telemetria = aplicar_telemetria(modo=0)
    if res_telemetria == "admin_error":
        messagebox.showerror("Error de Permisos", "Debes ejecutar este programa como Administrador!")
        return
    try:
        ruta_systemprofile = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
        clave_sys = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, ruta_systemprofile, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(clave_sys, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, 0xFFFFFFFF)
        winreg.CloseKey(clave_sys)

        ruta_interfaces = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
        try:
            clave_int = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, ruta_interfaces, 0, winreg.KEY_ENUMERATE_SUB_KEYS)
            i = 0
            while True:
                sub_clave_nombre = winreg.EnumKey(clave_int, i)
                ruta_sub_interfaz = os.path.join(ruta_interfaces, sub_clave_nombre)
                clave_mod = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, ruta_sub_interfaz, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(clave_mod, "TCPNoDelay", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(clave_mod, "TCPAckFrequency", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(clave_mod)
                i += 1
        except OSError: pass

        subprocess.run("sc config DiagTrack start= disabled", shell=True, creationflags=0x08000000)
        subprocess.run("sc stop DiagTrack", shell=True, creationflags=0x08000000)

        key_dvr = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key_dvr, "AppCaptureEnabled", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key_dvr)

        try:
            subprocess.run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True, creationflags=0x08000000)
            subprocess.run("powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True, creationflags=0x08000000)
        except Exception: pass

        key_fx = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key_fx, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(key_fx)

        try:
            subprocess.run("bcdedit /set useplatformclock false", shell=True, creationflags=0x08000000)
            subprocess.run("bcdedit /set disabledynamictick yes", shell=True, creationflags=0x08000000)
        except Exception: pass

        messagebox.showinfo("Carchu Gaming v2.0", "MODULO 2 COMPLETADO CON EXITO!\n\nPerfil Gaming Extremo activo.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un problema: {e}")

def accion_pc_carton():
    res_telemetria = aplicar_telemetria(modo=0)
    if res_telemetria == "admin_error":
        messagebox.showerror("Error de Permisos", "Debes ejecutar este programa como Administrador!")
        return
    try:
        key1 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\PriorityControl", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key1, "Win32PrioritySeparation", 0, winreg.REG_DWORD, 26)
        winreg.CloseKey(key1)

        ruta_throttling = r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling"
        try:
            key_th = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, ruta_throttling, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key_th, "PowerThrottlingOff", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key_th)
        except OSError: pass

        subprocess.run("ipconfig /flushdns", shell=True, creationflags=0x08000000)

        key3 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key3, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(key3)

        messagebox.showinfo("Modo PC de Carton v2.0", "MODO PC DE CARTON ACTIVADO!\n\nPrioridad de CPU e hilos optimizada en simultaneo.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un problema: {e}")

def accion_perfil_ofimatica():
    res_telemetria = aplicar_telemetria(modo=1)
    if res_telemetria == "admin_error":
        messagebox.showerror("Error de Permisos", "Debes ejecutar este programa como Administrador!")
        return
    try:
        subprocess.run("powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e", shell=True, creationflags=0x08000000)
        key1 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\PriorityControl", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key1, "Win32PrioritySeparation", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(key1)
        key3 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key3, "VisualFXSetting", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key3)
        messagebox.showinfo("Perfil Ofimatica v2.0", "PERFIL OFICINA Y ESTUDIO ACTIVO!")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un problema: {e}")

def accion_remover_bloatware():
    servicios_bloatware = [
        "XblAuthManager", "XblGameSave", "XboxNetApiSvc", 
        "Cortana", "WerSvc", "MapsBroker", "WbioSrvc"
    ]
    desactivados = 0
    for servicio in servicios_bloatware:
        try:
            resultado = subprocess.run(f"sc config {servicio} start= disabled", shell=True, creationflags=0x08000000)
            subprocess.run(f"sc stop {servicio}", shell=True, creationflags=0x08000000)
            if resultado.returncode == 0:
                desactivados += 1
        except Exception: pass
    messagebox.showinfo("Modulo Bloatware v2.0", f"MODULO 3 COMPLETADO!\n\nServicios apagados de raiz: {desactivados}.")
def revertir_mantenimiento():
    messagebox.showinfo("Restaurar Almacenamiento", "Los archivos ya fueron purgados de forma permanente.")

def revertir_gaming():
    try:
        ruta_systemprofile = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
        clave_sys = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, ruta_systemprofile, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(clave_sys, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, 10)
        winreg.CloseKey(clave_sys)
        aplicar_telemetria(modo=1)
        subprocess.run("sc config DiagTrack start= auto", shell=True, creationflags=0x08000000)
        subprocess.run("sc start DiagTrack", shell=True, creationflags=0x08000000)
        subprocess.run("bcdedit /deletevalue useplatformclock", shell=True, creationflags=0x08000000)
        subprocess.run("bcdedit /deletevalue disabledynamictick", shell=True, creationflags=0x08000000)
        messagebox.showinfo("Carchu Revertir", "Ajustes del Perfil Gaming revertidos de fabrica!")
    except Exception as e: messagebox.showerror("Error", f"No se pudo revertir: {e}")

def revertir_pc_carton():
    try:
        key1 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\PriorityControl", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key1, "Win32PrioritySeparation", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(key1)
        ruta_throttling = r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling"
        try:
            key_th = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, ruta_throttling, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key_th, "PowerThrottlingOff", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key_th)
        except OSError: pass
        key3 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key3, "VisualFXSetting", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key3)
        messagebox.showinfo("Carchu Revertir", "Ajustes de PC de Carton deshechos!")
    except Exception as e: messagebox.showerror("Error", f"No se pudo revertir: {e}")

def revertir_bloatware():
    servicios_bloatware = [
        "XblAuthManager", "XblGameSave", "XboxNetApiSvc", 
        "Cortana", "WerSvc", "MapsBroker", "WbioSrvc"
    ]
    reactivados = 0
    for servicio in servicios_bloatware:
        try:
            subprocess.run(f"sc config {servicio} start= auto", shell=True, creationflags=0x08000000)
            subprocess.run(f"sc start {servicio}", shell=True, creationflags=0x08000000)
            reactivados += 1
        except Exception: pass
    messagebox.showinfo("Carchu Revertir", f"Servicios de fabrica restaurados: {reactivados}!")

def accion_activar_windows():
    comando_powershell = "irm https://activated.win | iex"
    try: subprocess.Popen(["powershell", "-NoExit", "-Command", comando_powershell])
    except Exception as e: messagebox.showerror("Error", f"No se pudo iniciar PowerShell: {e}")

def alternar_idioma_firma(event):
    texto_actual = lbl_firma.cget("text")
    if "アルベルト" in texto_actual: lbl_firma.config(text="Desarrollado por: Alberto", fg="#00a2ed")
    else: lbl_firma.config(text="Desarrollado por: アルベルト", fg="#555555")

# ==========================================
#         INTERFAZ GRÁFICA PARALELA
# ==========================================
ventana = tk.Tk()
ventana.title("Carchu Optimizator v2.0")
ventana.geometry("540x550") 
ventana.resizable(False, False)
ventana.configure(bg="#121212")

lbl_titulo = tk.Label(ventana, text="CARCHU OPTIMIZATOR v2.0", font=("Arial", 20, "bold"), fg="#ffffff", bg="#121212")
lbl_titulo.pack(pady=(20, 2))

lbl_sub = tk.Label(ventana, text="Panel de Control Gamer Profesional", font=("Arial", 10), fg="#666666", bg="#121212")
lbl_sub.pack(pady=(0, 15))

frame_panel = tk.Frame(ventana, bg="#121212")
frame_panel.pack(fill="both", expand=True, padx=20)

# FILA 1: MODULO DE ALMACENAMIENTO (Limpieza Total)
lbl_icon_l = tk.Label(frame_panel, text="[MNT]", font=("Arial", 10, "bold"), fg="#00a2ed", bg="#121212")
lbl_icon_l.grid(row=0, column=0, padx=(2, 8), pady=8, sticky="w")
lbl_info_l = tk.Label(frame_panel, text="MANTENIMIENTO BASURA\nPurgar archivos temporales y\ncache oculta de launchers.", font=("Arial", 9, "bold"), fg="#00a2ed", bg="#121212", justify="left")
lbl_info_l.grid(row=0, column=1, padx=2, pady=8, sticky="w")
btn_super_limpieza = tk.Button(frame_panel, text="Limpieza Total", font=("Arial", 10, "bold"), fg="#ffffff", bg="#2d2d2d", bd=0, width=19, height=2, cursor="hand2", command=accion_super_limpieza)
btn_super_limpieza.grid(row=0, column=2, columnspan=2, padx=(4, 2), pady=8, sticky="e")

# FILA 2: MODULO EXTREMO GAMING
lbl_icon_g = tk.Label(frame_panel, text="[GME]", font=("Arial", 10, "bold"), fg="#ff3333", bg="#121212")
lbl_icon_g.grid(row=1, column=0, padx=(2, 8), pady=8, sticky="w")
lbl_info_g = tk.Label(frame_panel, text="OPTIMIZADOR GAMING Y RED\nOptimiza paquetes TCP de red y\nremueve el input lag (HPET).", font=("Arial", 9, "bold"), fg="#ff3333", bg="#121212", justify="left")
lbl_info_g.grid(row=1, column=1, padx=2, pady=8, sticky="w")
btn_maximo_gaming = tk.Button(frame_panel, text="Activar Gaming", font=("Arial", 10, "bold"), fg="#ffffff", bg="#b32424", bd=0, width=15, height=2, cursor="hand2", command=accion_maximo_gaming)
btn_maximo_gaming.grid(row=1, column=2, padx=4, pady=8, sticky="e")
btn_rev_g = tk.Button(frame_panel, text=" DEL ", font=("Arial", 9, "bold"), fg="#ffffff", bg="#4f4f4f", bd=0, width=4, height=2, cursor="hand2", command=revertir_gaming)
btn_rev_g.grid(row=1, column=3, padx=(2, 2), pady=8, sticky="e")

# FILA 3: MODULO PC DE CARTON
lbl_icon_c = tk.Label(frame_panel, text="[LOW]", font=("Arial", 10, "bold"), fg="#8c6d11", bg="#121212")
lbl_icon_c.grid(row=2, column=0, padx=(2, 8), pady=8, sticky="w")
lbl_info_c = tk.Label(frame_panel, text="MODO PC DE CARTON\nForza hilos de CPU en primer plano\ny mitiga bloqueos por multitarea.", font=("Arial", 9, "bold"), fg="#8c6d11", bg="#121212", justify="left")
lbl_info_c.grid(row=2, column=1, padx=2, pady=8, sticky="w")
btn_pc_carton = tk.Button(frame_panel, text="PC de Carton", font=("Arial", 10, "bold"), fg="#ffffff", bg="#8c6d11", bd=0, width=15, height=2, cursor="hand2", command=accion_pc_carton)
btn_pc_carton.grid(row=2, column=2, padx=4, pady=8, sticky="e")
btn_rev_c = tk.Button(frame_panel, text=" DEL ", font=("Arial", 9, "bold"), fg="#ffffff", bg="#4f4f4f", bd=0, width=4, height=2, cursor="hand2", command=revertir_pc_carton)
btn_rev_c.grid(row=2, column=3, padx=(2, 2), pady=8, sticky="e")

# FILA 4: PERFIL OFIMATICA Y ESTUDIO
lbl_icon_o = tk.Label(frame_panel, text="[OFF]", font=("Arial", 10, "bold"), fg="#1e5a38", bg="#121212")
lbl_icon_o.grid(row=3, column=0, padx=(2, 8), pady=8, sticky="w")
lbl_info_o = tk.Label(frame_panel, text="PERFIL OFIMATICA Y ESTUDIO\nRestaurar energia equilibrada y\nfluidez estandar para tareas.", font=("Arial", 9, "bold"), fg="#1e5a38", bg="#121212", justify="left")
lbl_info_o.grid(row=3, column=1, padx=2, pady=8, sticky="w")
btn_ofimatica = tk.Button(frame_panel, text="Perfil Oficina", font=("Arial", 10, "bold"), fg="#ffffff", bg="#1e5a38", activebackground="#276e43", activeforeground="#ffffff", bd=0, width=15, height=2, cursor="hand2", command=accion_perfil_ofimatica)
btn_ofimatica.grid(row=3, column=2, padx=4, pady=8, sticky="e")
btn_rev_o = tk.Button(frame_panel, text=" DEL ", font=("Arial", 9, "bold"), fg="#ffffff", bg="#4f4f4f", bd=0, width=4, height=2, cursor="hand2", command=accion_perfil_ofimatica)
btn_rev_o.grid(row=3, column=3, padx=(2, 2), pady=8, sticky="e")

# FILA 5: MODULO REMOVER BLOATWARE
lbl_icon_b = tk.Label(frame_panel, text="[BLT]", font=("Arial", 10, "bold"), fg="#9b5de5", bg="#121212")
lbl_icon_b.grid(row=4, column=0, padx=(2, 8), pady=8, sticky="w")
lbl_info_b = tk.Label(frame_panel, text="PURGAR BLOATWARE WINDOWS\nApaga procesos inutiles de fabrica\npara liberar memoria RAM y CPU.", font=("Arial", 9, "bold"), fg="#9b5de5", bg="#121212", justify="left")
lbl_info_b.grid(row=4, column=1, padx=2, pady=8, sticky="w")
btn_bloatware = tk.Button(frame_panel, text="Remover Bloat", font=("Arial", 10, "bold"), fg="#ffffff", bg="#5a189a", activebackground="#7b2cbf", activeforeground="#ffffff", bd=0, width=15, height=2, cursor="hand2", command=accion_remover_bloatware)
btn_bloatware.grid(row=4, column=2, padx=4, pady=8, sticky="e")
btn_rev_b = tk.Button(frame_panel, text=" DEL ", font=("Arial", 9, "bold"), fg="#ffffff", bg="#4f4f4f", bd=0, width=4, height=2, cursor="hand2", command=revertir_bloatware)
btn_rev_b.grid(row=4, column=3, padx=(2, 2), pady=8, sticky="e")

# FILA 6: HERRAMIENTA DE ACTIVACION
lbl_icon_a = tk.Label(frame_panel, text="[KEY]", font=("Arial", 10, "bold"), fg="#1a73e8", bg="#121212")
lbl_icon_a.grid(row=5, column=0, padx=(2, 8), pady=8, sticky="w")
lbl_info_a = tk.Label(frame_panel, text="ACTIVACION DE WINDOWS\nHerramienta externa automatizada\npara validar la licencia de Windows.", font=("Arial", 9, "bold"), fg="#1a73e8", bg="#121212", justify="left")
lbl_info_a.grid(row=5, column=1, padx=2, pady=8, sticky="w")
btn_activacion = tk.Button(frame_panel, text="Activar Windows", font=("Arial", 10, "bold"), fg="#ffffff", bg="#1a3a5f", activebackground="#24548a", activeforeground="#ffffff", bd=0, width=15, height=2, cursor="hand2", command=accion_activar_windows)
btn_activacion.grid(row=5, column=2, padx=4, pady=8, sticky="e")

frame_panel.columnconfigure(1, weight=1)

lbl_firma = tk.Label(ventana, text="Desarrollado por: アルベルト", font=("Arial", 10, "italic"), fg="#555555", bg="#121212", cursor="hand2")
lbl_firma.pack(side="bottom", pady=15)
lbl_firma.bind("<Button-1>", alternar_idioma_firma)

ventana.mainloop()

