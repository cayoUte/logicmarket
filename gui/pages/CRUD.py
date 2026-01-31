import tkinter as tk
from gui.components.inputs.TextInput import TextInput
from gui.components.buttons.Button import Pillow_Button
from gui.components.Table import Table
from service.inventory_service import search_products_action


def ImporterPage(parent, store_funcs):
    dispatch = store_funcs["dispatch"]
    subscribe = store_funcs["subscribe"]
    get_state = store_funcs["get_state"]
    print(f"Current state: {get_state()}")
    bg_color = "#f0f0f0"
    frame = tk.Frame(parent, bg=bg_color)

    # --- TÍTULO ---
    tk.Label(frame, text="Importador de API", font=("Arial", 16, "bold"), bg=bg_color).pack(pady=10)

    # ==========================================
    # 1. BARRA DE BÚSQUEDA Y CONFIGURACIÓN DE LOTE
    # ==========================================
    control_panel = tk.Frame(frame, bg=bg_color)
    control_panel.pack(fill="x", padx=20, pady=10)

    # A. Buscador
    tk.Label(control_panel, text="Buscar en API:", bg=bg_color).grid(row=0, column=0, sticky="w")
    inp_search = TextInput(control_panel, placeholder="Ej: Cookies", width=200)
    inp_search.grid(row=1, column=0, padx=5)

    # B. Configuración Masiva (Para no ir uno por uno)
    tk.Label(control_panel, text="Stock Inicial:", bg=bg_color).grid(row=0, column=1, sticky="w")
    inp_stock = TextInput(control_panel, placeholder="Ej: 50", width=80)
    inp_stock.grid(row=1, column=1, padx=5)

    tk.Label(control_panel, text="Precio Venta:", bg=bg_color).grid(row=0, column=2, sticky="w")
    inp_price = TextInput(control_panel, placeholder="Ej: 1.50", width=80)
    inp_price.grid(row=1, column=2, padx=5)

    # --- ACCIONES ---
    def do_search():
        term = inp_search.get_value()
        # Llamada directa a la función dispatch del closure
        dispatch(search_products_action(term), ui_ref=frame)

    btn_search = Pillow_Button(control_panel, text="Buscar", on_click=do_search, variant="dark", dimensions=(100,30,5))
    btn_search.grid(row=1, column=3, padx=10)

    # ==========================================
    # 2. TABLA DE PREVISUALIZACIÓN
    # ==========================================
    # Columnas simplificadas para la vista previa
    cols = [
        {"id": "code", "text": "Código", "width": 100},
        {"id": "name", "text": "Producto Detectado", "width": 300},
        {"id": "brand", "text": "Marca", "width": 150}
    ]
    
    table = Table(frame, columns=cols, data=[], height=10)
    table.pack(fill="both", expand=True, padx=20, pady=10)

    # ==========================================
    # 3. BOTÓN FINAL DE IMPORTACIÓN
    # ==========================================
    def import_batch():
        # 1. Obtenemos estado actual invocando la función (ya no es un método de clase)
        current_state = get_state() 
        api_results = current_state.get("resultados_api", [])
        
        if not api_results:
            print("⚠️ Nada que importar")
            return

        # 2. Obtenemos valores de los inputs (Esto es UI puro)
        stock_val = inp_stock.get_value() or "0"
        price_val = inp_price.get_value() or "0.0"
        
        # Validación básica para no enviar basura al reducer
        config = {
            "stock": int(stock_val) if stock_val.isdigit() else 0,
            "precio": float(price_val) if price_val.replace('.','',1).isdigit() else 0.0,
            "proveedor": "OpenFood Import"
        }

        # 3. Despachamos la acción ('TIPO', PAYLOAD)
        # El payload es una tupla: (La lista cruda, La configuración a aplicar)
        dispatch(('IMPORTAR_LOTE', (api_results, config)))
        
        # 4. Limpiamos la búsqueda (Opcional, para UX)
        dispatch(('LIMPIAR_BUSQUEDA', None))

    # Botón
    btn_import = Pillow_Button(frame, text="IMPORTAR LOTE", on_click=import_batch, variant="primary", dimensions=(300, 40, 10))
    btn_import.pack(pady=20)

    # --- SUSCRIPCIÓN ---
    def update_ui(state):
        # PROTECCIÓN EXTRA: Si el frame ya murió, no hacemos nada.
        try:
            if not frame.winfo_exists():
                return
        except:
            return

        raw_data = state.get("resultados_api", [])
        
        # Mapping para la tabla
        table_rows = []
        for p in raw_data:
            code = p.get('code', 'S/N')
            name = p.get('product_name', 'Desconocido')
            brand = p.get('brands', '')
            table_rows.append((code, name, brand))
        
        if hasattr(table, "set_data"):
            try:
                table.set_data(table_rows)
            except tk.TclError:
                pass # Ignoramos errores si el widget muere justo ahora

    # 1. Guardamos la función de 'darse de baja'
    unsubscribe_fn = subscribe(update_ui)

    # 2. Detectamos cuando el frame se destruye (al cambiar de página)
    def on_destroy(event):
        # El evento <Destroy> se propaga a los hijos. 
        # Solo nos desuscribimos si el que muere es EL FRAME PRINCIPAL de la página.
        if event.widget == frame:
            unsubscribe_fn()
            # Opcional: print("Desuscribiendo ImporterPage del Store")

    # 3. Bind al evento
    frame.bind("<Destroy>", on_destroy)
    
    return frame