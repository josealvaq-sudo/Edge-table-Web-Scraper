import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
import pandas as pd
import time
import threading

class TableExtractorEdge:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Extractor - Edge")
        self.root.geometry("700x600")
        
        self.driver = None
        self.extracted_data = None
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Extractor de Tablas WEB - Microsoft Edge", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Instrucciones simplificadas
        instructions_frame = ttk.LabelFrame(main_frame, text="Instrucciones", padding="10")
        instructions_frame.pack(fill=tk.X, pady=10)
        
        instructions_text = """
Pasos para usar el extractor:
1. Haz clic en "Conectar a Edge" para abrir un nuevo navegador
2. Navega a la página web con las tablas que quieres extraer
3. Haz clic en "Inspeccionar Página" para ver información de la página
4. Usa "Extraer Todas las Tablas" para obtener todos los datos automáticamente
        """
        
        ttk.Label(instructions_frame, text=instructions_text, justify=tk.LEFT).pack()
        
        # Botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.connect_btn = ttk.Button(button_frame, text="Conectar a Edge", 
                                     command=self.connect_to_edge)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        self.inspect_btn = ttk.Button(button_frame, text="Inspeccionar Página", 
                                     command=self.inspect_page, state=tk.DISABLED)
        self.inspect_btn.pack(side=tk.LEFT, padx=5)
        
        # Herramientas de extracción
        extract_frame = ttk.LabelFrame(main_frame, text="Herramientas de Extracción", padding="10")
        extract_frame.pack(fill=tk.X, pady=10)
        
        # Botones de extracción
        extract_buttons = ttk.Frame(extract_frame)
        extract_buttons.pack(pady=5)
        
        ttk.Button(extract_buttons, text="Buscar Tablas", 
                  command=self.find_tables, state=tk.DISABLED).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(extract_buttons, text="Extraer Todas las Tablas", 
                  command=self.extract_all_tables, state=tk.DISABLED).pack(side=tk.LEFT, padx=5)
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, height=12, width=80)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=10)
        
        self.preview_btn = ttk.Button(action_frame, text="Vista Previa", 
                                     command=self.preview_data, state=tk.DISABLED)
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(action_frame, text="Guardar CSV", 
                                  command=self.save_data, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Cerrar Conexión", 
                  command=self.close_connection).pack(side=tk.LEFT, padx=5)
    
    def log(self, message):
        timestamp = time.strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def connect_to_edge(self):
        def connect():
            try:
                # Siempre abrir nuevo Edge
                options = EdgeOptions()
                options.add_argument("--start-maximized")
                self.driver = webdriver.Edge(options=options)
                
                self.log("✓ Conectado a Microsoft Edge (nueva instancia)")
                
                # Habilitar botones
                for widget in self.root.winfo_children():
                    self.enable_buttons_recursive(widget)
                
                # Mostrar información de la página actual
                try:
                    current_url = self.driver.current_url
                    page_title = self.driver.title
                    self.log(f"Página actual: {page_title}")
                    self.log(f"URL: {current_url}")
                except:
                    self.log("Navega a tu página web con las tablas")
                
            except Exception as e:
                self.log(f"✗ Error al conectar: {str(e)}")
                messagebox.showerror("Error", f"No se pudo conectar a Edge:\n{str(e)}\n\nAsegúrate de tener Edge WebDriver instalado")
        
        # Ejecutar en hilo separado para no bloquear la UI
        thread = threading.Thread(target=connect)
        thread.daemon = True
        thread.start()
    
    def enable_buttons_recursive(self, widget):
        for child in widget.winfo_children():
            if isinstance(child, ttk.Button):
                if any(text in child.cget("text") for text in ["Buscar", "Extraer", "Inspeccionar"]):
                    child.config(state=tk.NORMAL)
            elif hasattr(child, 'winfo_children'):
                self.enable_buttons_recursive(child)
    
    def inspect_page(self):
        if not self.driver:
            return
        
        try:
            # Obtener información de la página
            page_info_script = """
            return {
                title: document.title,
                url: window.location.href,
                tables: document.querySelectorAll('table').length,
                divs: document.querySelectorAll('div').length,
                forms: document.querySelectorAll('form').length,
                inputs: document.querySelectorAll('input').length
            };
            """
            
            info = self.driver.execute_script(page_info_script)
            
            self.log("=== INFORMACIÓN DE LA PÁGINA ===")
            self.log(f"Título: {info['title']}")
            self.log(f"URL: {info['url']}")
            self.log(f"Tablas HTML: {info['tables']}")
            self.log(f"Divs: {info['divs']}")
            self.log(f"Formularios: {info['forms']}")
            self.log(f"Inputs: {info['inputs']}")
            
        except Exception as e:
            self.log(f"✗ Error al inspeccionar: {str(e)}")
    
    def find_tables(self):
        if not self.driver:
            return
        
        try:
            # Script para encontrar todas las posibles tablas
            find_script = """
            const results = [];
            
            // 1. Tablas HTML tradicionales
            document.querySelectorAll('table').forEach((table, index) => {
                const rows = table.querySelectorAll('tr').length;
                const cells = table.querySelectorAll('td, th').length;
                if (rows > 0) {
                    results.push({
                        type: 'HTML Table',
                        selector: `table:nth-of-type(${index + 1})`,
                        rows: rows,
                        cells: cells,
                        id: table.id || 'sin-id',
                        class: table.className || 'sin-clase',
                        preview: table.textContent.substring(0, 100).replace(/\\s+/g, ' ')
                    });
                }
            });
            
            // 2. Grids CSS comunes
            const gridSelectors = [
                '[class*="grid"]',
                '[class*="table"]', 
                '[class*="data"]',
                '[class*="list"]',
                '[role="grid"]',
                '[role="table"]'
            ];
            
            gridSelectors.forEach(selector => {
                document.querySelectorAll(selector).forEach((element, index) => {
                    const children = element.children.length;
                    if (children > 2) {
                        results.push({
                            type: 'CSS Grid/Table',
                            selector: selector + `:nth-of-type(${index + 1})`,
                            rows: children,
                            cells: element.querySelectorAll('*').length,
                            id: element.id || 'sin-id',
                            class: element.className || 'sin-clase',
                            preview: element.textContent.substring(0, 100).replace(/\\s+/g, ' ')
                        });
                    }
                });
            });
            
            // 3. Contenedores con muchos números
            document.querySelectorAll('div, section, article').forEach((element, index) => {
                const text = element.textContent || '';
                const numbers = text.match(/\\d+(\\.\\d+)?/g);
                const children = element.children.length;
                
                if (numbers && numbers.length > 10 && children > 5) {
                    results.push({
                        type: 'Numeric Container',
                        selector: `${element.tagName.toLowerCase()}:nth-of-type(${index + 1})`,
                        rows: children,
                        cells: numbers.length,
                        id: element.id || 'sin-id',
                        class: element.className || 'sin-clase',
                        preview: text.substring(0, 100).replace(/\\s+/g, ' ')
                    });
                }
            });
            
            return results;
            """
            
            results = self.driver.execute_script(find_script)
            
            self.log("=== TABLAS/GRIDS ENCONTRADOS ===")
            if results:
                for i, result in enumerate(results[:10]):  # Mostrar solo los primeros 10
                    self.log(f"\n{i+1}. {result['type']}")
                    self.log(f"   Selector: {result['selector']}")
                    self.log(f"   Filas: {result['rows']}, Celdas: {result['cells']}")
                    if result['id'] != 'sin-id':
                        self.log(f"   ID: {result['id']}")
                    if result['class'] != 'sin-clase':
                        self.log(f"   Clase: {result['class'][:50]}")
                    self.log(f"   Preview: {result['preview'][:80]}...")
                
                self.log(f"\n✓ Total encontrados: {len(results)}")
            else:
                self.log("✗ No se encontraron tablas o grids")
                
        except Exception as e:
            self.log(f"✗ Error al buscar tablas: {str(e)}")
    
    def extract_all_tables(self):
        """Extrae todas las tablas encontradas en la página"""
        if not self.driver:
            return
        
        try:
            self.log("Extrayendo todas las tablas de la página...")
            
            # Script para extraer todas las tablas
            extract_all_script = """
            const allData = [];
            let tableCounter = 0;
            
            // Función para extraer texto limpio
            function getCleanText(el) {
                return (el.textContent || el.innerText || '').trim().replace(/\\s+/g, ' ');
            }
            
            // 1. Extraer todas las tablas HTML
            document.querySelectorAll('table').forEach((table, tableIndex) => {
                const tableData = [];
                const rows = table.querySelectorAll('tr');
                
                rows.forEach(row => {
                    const cells = row.querySelectorAll('td, th');
                    if (cells.length > 0) {
                        const rowData = Array.from(cells).map(cell => getCleanText(cell));
                        if (rowData.some(cell => cell.length > 0)) {
                            tableData.push(rowData);
                        }
                    }
                });
                
                if (tableData.length > 0) {
                    allData.push({
                        type: 'HTML Table',
                        index: tableIndex + 1,
                        data: tableData,
                        info: `Tabla HTML #${tableIndex + 1} (${tableData.length} filas)`
                    });
                    tableCounter++;
                }
            });
            
            // 2. Extraer grids CSS comunes
            const gridSelectors = [
                '[class*="grid"]',
                '[class*="table"]', 
                '[class*="data"]',
                '[role="grid"]',
                '[role="table"]'
            ];
            
            gridSelectors.forEach(selector => {
                document.querySelectorAll(selector).forEach((element, index) => {
                    if (element.tagName !== 'TABLE') { // Evitar duplicados
                        const gridData = [];
                        const rows = Array.from(element.children);
                        
                        rows.forEach(row => {
                            const cells = Array.from(row.children);
                            if (cells.length > 0) {
                                const rowData = cells.map(cell => getCleanText(cell));
                                if (rowData.some(cell => cell.length > 0)) {
                                    gridData.push(rowData);
                                }
                            }
                        });
                        
                        if (gridData.length > 1) { // Al menos 2 filas para considerar como tabla
                            allData.push({
                                type: 'CSS Grid',
                                index: index + 1,
                                data: gridData,
                                info: `Grid CSS (${selector}) #${index + 1} (${gridData.length} filas)`
                            });
                            tableCounter++;
                        }
                    }
                });
            });
            
            return {tables: allData, totalTables: tableCounter};
            """
            
            result = self.driver.execute_script(extract_all_script)
            all_tables = result['tables']
            total_tables = result['totalTables']
            
            if all_tables and len(all_tables) > 0:
                self.log(f"✓ Se encontraron {total_tables} tablas en la página")
                
                # Combinar todas las tablas en un solo DataFrame
                combined_data = []
                table_info = []
                
                for table in all_tables:
                    self.log(f"Procesando: {table['info']}")
                    
                    # Agregar separador entre tablas
                    if combined_data:
                        combined_data.append(['--- SEPARADOR DE TABLA ---'] * max(len(row) for row in combined_data[-5:] if row))
                    
                    # Agregar información de la tabla
                    combined_data.append([f"=== {table['info']} ==="])
                    
                    # Agregar datos de la tabla
                    combined_data.extend(table['data'])
                    
                    table_info.append(table['info'])
                
                if combined_data:
                    # Crear DataFrame
                    df = pd.DataFrame(combined_data)
                    
                    # Limpiar datos vacíos
                    df = df.dropna(how='all').reset_index(drop=True)
                    
                    if not df.empty:
                        self.extracted_data = df
                        self.log(f"✓ Extracción completa exitosa!")
                        self.log(f"Total de filas extraídas: {len(df)}")
                        self.log(f"Total de columnas: {len(df.columns)}")
                        self.log(f"Tablas procesadas: {len(table_info)}")
                        
                        # Mostrar resumen de tablas
                        for info in table_info:
                            self.log(f"  - {info}")
                        
                        # Habilitar botones
                        self.preview_btn.config(state=tk.NORMAL)
                        self.save_btn.config(state=tk.NORMAL)
                    else:
                        self.log("✗ No se encontraron datos válidos después del procesamiento")
                else:
                    self.log("✗ No se pudieron extraer datos de las tablas")
            else:
                self.log("✗ No se encontraron tablas en la página")
                self.log("Intenta usar 'Buscar Tablas' primero para ver qué elementos están disponibles")
                
        except Exception as e:
            self.log(f"✗ Error en extracción de tablas: {str(e)}")
    
    def preview_data(self):
        if self.extracted_data is None:
            return
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Vista Previa de Datos")
        preview_window.geometry("900x500")
        
        # Frame principal
        main_frame = ttk.Frame(preview_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información
        info_label = ttk.Label(main_frame, 
                              text=f"Datos extraídos: {len(self.extracted_data)} filas, {len(self.extracted_data.columns)} columnas")
        info_label.pack(pady=5)
        
        # Texto con scroll
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(text_frame, wrap=tk.NONE)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=text_widget.xview)
        
        text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid
        text_widget.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        # Mostrar datos
        preview_text = self.extracted_data.head(100).to_string(max_cols=20, max_colwidth=30)
        text_widget.insert(tk.END, preview_text)
        
        if len(self.extracted_data) > 100:
            text_widget.insert(tk.END, f"\n\n... y {len(self.extracted_data) - 100} filas más")
    
    def save_data(self):
        if self.extracted_data is None:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("Text files", "*.txt")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.xlsx'):
                    self.extracted_data.to_excel(filename, index=False)
                elif filename.endswith('.txt'):
                    self.extracted_data.to_csv(filename, index=False, sep='\t')
                else:
                    self.extracted_data.to_csv(filename, index=False, encoding='utf-8')
                
                self.log(f"✓ Datos guardados en: {filename}")
                messagebox.showinfo("Éxito", f"Datos guardados exitosamente!\n\nArchivo: {filename}\nFilas: {len(self.extracted_data)}")
                
            except Exception as e:
                self.log(f"✗ Error al guardar: {str(e)}")
                messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")
    
    def close_connection(self):
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.log("✓ Conexión cerrada")
                
                # Deshabilitar botones
                for widget in self.root.winfo_children():
                    self.disable_buttons_recursive(widget)
                    
            except Exception as e:
                self.log(f"Error al cerrar: {str(e)}")
    
    def disable_buttons_recursive(self, widget):
        for child in widget.winfo_children():
            if isinstance(child, ttk.Button):
                if any(text in child.cget("text") for text in ["Buscar", "Extraer", "Inspeccionar", "Vista", "Guardar"]):
                    child.config(state=tk.DISABLED)
            elif hasattr(child, 'winfo_children'):
                self.disable_buttons_recursive(child)

def main():
    root = tk.Tk()
    app = TableExtractorEdge(root)
    root.mainloop()

if __name__ == "__main__":
    main()