# Table Extractor - Edge
## Resumen
Table Extractor - Edge es una aplicación de escritorio desarrollada en Python que permite extraer automáticamente tablas y datos estructurados de páginas web utilizando Microsoft Edge WebDriver. La aplicación proporciona una interfaz gráfica intuitiva que facilita la conexión con el navegador Edge, la inspección de páginas web, y la extracción masiva de tablas HTML y grids CSS para su posterior exportación en diferentes formatos.
## Features
Conexión automática con Microsoft Edge: Abre una nueva instancia del navegador Edge para navegación manual
Inspección de páginas web: Analiza la estructura de la página actual mostrando información detallada sobre elementos HTML
Detección inteligente de tablas: Encuentra automáticamente tablas HTML tradicionales, grids CSS y contenedores con datos numéricos
Extracción masiva de datos: Extrae todas las tablas encontradas en una sola operación
Vista previa de datos: Permite visualizar los datos extraídos antes de guardarlos
Múltiples formatos de exportación: Guarda los datos en formato CSV, Excel (.xlsx) o texto plano (.txt)
Interfaz gráfica intuitiva: GUI desarrollada con tkinter para facilidad de uso
Log en tiempo real: Muestra el progreso y estado de todas las operaciones
Procesamiento en hilos separados: Evita el bloqueo de la interfaz durante operaciones largas
## Librerías
### Librerías estándar de Python:
tkinter - Interfaz gráfica de usuario
time - Manejo de timestamps y pausas
threading - Ejecución de tareas en hilos separados
### Librerías de terceros:
selenium - Automatización del navegador web
pandas - Manipulación y análisis de datos
webdriver (Edge WebDriver) - Control específico de Microsoft Edge
##H ow to Run the Project
### Requisitos previos:
Python 3.7 o superior instalado en el sistema
Microsoft Edge instalado
Edge WebDriver descargado y configurado en el PATH del sistema
## Instalación de dependencias:
pip install selenium pandas openpyxl
## Configuración del Edge WebDriver:
Descarga Edge WebDriver desde: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Asegúrate de que la versión coincida con tu versión de Microsoft Edge
Coloca el archivo msedgedriver.exe en una carpeta incluida en tu PATH del sistema
## Instrucciones de uso:
Conectar a Edge: Haz clic en "Conectar a Edge" para abrir una nueva instancia del navegador
Navegar: Ve a la página web que contiene las tablas que deseas extraer
Inspeccionar: Usa "Inspeccionar Página" para ver información sobre la estructura de la página
Buscar tablas: Utiliza "Buscar Tablas" para identificar todos los elementos tipo tabla disponibles
Extraer datos: Haz clic en "Extraer Todas las Tablas" para obtener todos los datos automáticamente
Vista previa: Revisa los datos extraídos con el botón "Vista Previa"
Guardar: Exporta los datos en el formato deseado usando "Guardar CSV"
## Solución de problemas comunes:
Error de WebDriver: Verifica que Edge WebDriver esté instalado y en el PATH
No se encuentran tablas: Algunas páginas usan JavaScript dinámico; espera a que la página cargue completamente
Datos incompletos: Algunas tablas pueden requerir interacción manual (scroll, clicks) antes de la extracción
