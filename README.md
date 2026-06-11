# Analiza-pcs-laptops-y-femboys
Sirve :v espero que si
🛠️ anliza pcs laptops y femboys

anliza pcs laptops y femboys es una herramienta portátil, liviana y de código abierto desarrollada en Python, diseñada específicamente para técnicos de soporte, talleres de reparación de PC y entusiastas del hardware.

Su propósito es agilizar el diagnóstico de computadoras con Windows, extrayendo información profunda que el sistema operativo normalmente oculta, auditando errores de hardware en tiempo real y realizando pruebas físicas de periféricos sin necesidad de instalar programas pesados de terceros.

⚙️ Características Principales

📊 Monitor en Tiempo Real: Supervisa el uso de CPU (porcentajes, frecuencias y núcleos), uso de RAM, estado de los discos principales, batería y tráfico de red en vivo, incluyendo el tiempo de encendido real (Uptime). Incluye un botón para Test de Estrés (Stress Test).

🔎 Specs Detalladas y WMI: Extrae los modelos exactos, marcas, números de serie y firmware de la Placa Base, módulos de RAM y almacenamiento.

🔋 Diagnóstico de Batería: Lee el chip de energía para calcular la capacidad de fábrica vs. la actual, determinando el porcentaje exacto de desgaste y emitiendo alertas si requiere reemplazo.

⚠️ Auditoría y Errores PnP: Escanea de forma silenciosa el registro de Windows, el Administrador de Dispositivos y los registros SMART para encontrar discos a punto de fallar, drivers faltantes (Errores 43, 28, etc.) o Pantallazos Azules (Minidumps) recientes.

🚀 Análisis de Arranque (Autostart): Lee el registro de Windows (Regedit) para enlistar los programas ocultos que ralentizan el encendido del equipo.

🖱️ Pruebas Físicas (Periféricos):

Test de pulsaciones de Teclado ⌨️.

Área de pruebas para sensibilidad de Mouse / Touchpad y clics.

Test de cámara web integrado (OpenCV) 📷.

Test de Píxeles Muertos (cambio de colores primarios en pantalla completa) 🖥️.

Prueba de altavoces/audio del sistema operativo 🔊.

🔑 Recuperación de Claves: Intenta extraer la clave OEM (Product Key) de Windows incrustada en la BIOS/UEFI.

💾 Exportación de Reportes: Guarda todo el inventario de hardware en un archivo .txt para entregar al cliente o guardar en base de datos.

📥 Requisitos e Instalación

El programa está diseñado para ejecutarse en Windows (debido al uso intensivo de la API WMI y el Registro).

1. Requisitos Previos

Asegúrate de tener instalado Python 3.8 o superior. Durante la instalación, es vital marcar la casilla "Add Python to PATH".

2. Instalación de Dependencias

Abre tu terminal (Símbolo del sistema o PowerShell) e instala las librerías necesarias ejecutando el siguiente comando:

pip install psutil GPUtil wmi pypiwin32 opencv-python


Nota: tkinter, socket, subprocess, winreg y winsound son librerías estándar de Python y no requieren instalación adicional.

3. Ejecución

Descarga el archivo principal y ejecútalo con doble clic.
(Al tener la extensión .pyw, se ejecutará en modo ventana sin mostrar la consola negra de fondo).

⚠️ Importante: Para obtener resultados completos en la pestaña de "Auditoría y Errores" o para leer ciertas claves de la BIOS, se recomienda ejecutar el script con Permisos de Administrador.

🤝 Cómo contribuir

¡Las contribuciones son bienvenidas! Si tienes ideas para añadir nuevos tests (como lectura directa de temperaturas de CPU mediante puentes de hardware) o mejorar la interfaz gráfica:

Haz un Fork del repositorio.

Crea una rama con tu nueva función (git checkout -b feature/NuevaFuncion).

Haz Commit de tus cambios (git commit -m 'Añadida NuevaFuncion').

Haz Push a la rama (git push origin feature/NuevaFuncion).

Abre un Pull Request 🛠️.

📜 Licencia

Este proyecto está bajo la Licencia MIT. Siéntete libre de modificarlo, mejorarlo y utilizarlo en tu taller de servicio técnico.
