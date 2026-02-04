import tkinter as tk
from gui.components.ImportResultsList import ImportResultsList
from gui.components.TextField import TextField 
from gui.components.buttons.Button import Pillow_Button
from gui.components.modals.ImportModal import ImportModal

# --- IMPORTS DE STORE Y TEMA ---
from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font
from store.slices.inventory_slice import actions
from store.selectors import select_current_colors, select_paginated_results, select_theme_mode
from service.inventory_service import search_products_action

def ImporterPage(parent, store_funcs):
    dispatch = store_funcs["dispatch"]
    subscribe = store_funcs["subscribe"]
    get_state = store_funcs["get_state"]
    
    # 1. OBTENER COLORES DEL TEMA ACTUAL
    state = get_state()
    current_mode = select_theme_mode(state) # "light" o "dark"
    colors = select_current_colors(state)
    
    bg_color = colors["background"]      # Fondo general (ej: #f5f9f4 o #1e1e1e)
    surface_color = colors["surface"]    # Fondo de tarjetas (ej: #ffffff o #2b2d31)
    text_color = colors["text"]          # Color de texto
    
    # 2. FRAME PRINCIPAL
    frame = tk.Frame(parent, bg=bg_color)

    # ==========================================
    # 3. HEADER (Título)
    # ==========================================
    header_frame = tk.Frame(frame, bg=bg_color)
    header_frame.pack(fill="x", padx=24, pady=(24, 0))
    
    lbl_title = tk.Label(
        header_frame, 
        text="Importador de Productos", 
        bg=bg_color, 
        fg=text_color, 
        font=get_font("h5")
    )
    lbl_title.pack(side="left")

    # ==========================================
    # 4. TARJETA DE FILTROS
    # ==========================================
    filter_frame = tk.Frame(frame, bg=surface_color)
    filter_frame.pack(fill="x", padx=24, pady=16)
    
    # Contenedor interno para dar padding dentro de la "tarjeta"
    # Usamos grid para alinear Inputs y Botón
    inner_filter = tk.Frame(filter_frame, bg=surface_color, padx=20, pady=20)
    inner_filter.pack(fill="x")

    # --- INPUT 1: CATEGORÍA ---
    inp_cat = TextField(
        inner_filter, 
        label="Categoría", 
        placeholder="Ej: Snacks", 
        width=220,
        ui_mode=current_mode,
        bg_parent=bg_color
    )
    inp_cat.grid(row=0, column=0, padx=(0, 16))

    # --- INPUT 2: PAÍS ---
    inp_country = TextField(
        inner_filter, 
        label="País", 
        placeholder="Ej: Ecuador", 
        width=220,
        ui_mode=current_mode,
        bg_parent=bg_color
    )
    inp_country.grid(row=0, column=1, padx=(0, 16))

    # --- BOTÓN BUSCAR ---
    def do_search():
        filters = {
            "categories": inp_cat.get_value(),
            "countries": inp_country.get_value()
        }
        # Solo buscamos si hay algo escrito para no spammear la API
        if any(filters.values()):
            dispatch(search_products_action(filters), ui_ref=frame)

    # Frame contenedor para alinear el botón verticalmente con los inputs
    # (A veces los inputs tienen labels arriba y el botón queda desalineado si no se ajusta)
    btn_container = tk.Frame(inner_filter, bg=surface_color, pady=2) 
    btn_container.grid(row=0, column=2, sticky="s") # sticky="s" lo empuja abajo

    btn_search = Pillow_Button(
        btn_container, 
        text="BUSCAR", 
        on_click=do_search, 
        variant="primary",       # Color principal
        bg_parent=surface_color, # Importante: Está sobre el filter_frame (surface)
        ui_mode=current_mode,    # Para texto blanco/negro correcto
        dimensions=(120, 44, 22) # Pill shape
    )
    btn_search.pack()

    # ==========================================
    # 5. LISTA DE RESULTADOS
    # ==========================================
    # Callbacks del Modal
    def on_modal_confirm(final_item_data):
        dispatch(actions["importBatch"]([final_item_data]))

    def open_modal_wrapper(product_data):
        ImportModal(
            parent=parent, # Nota: 'parent' aquí es el contenedor principal de la página
            product_data=product_data, 
            on_confirm=on_modal_confirm,
            ui_mode=current_mode # <--- ¡IMPORTANTE!
        )

    # Contenedor de la lista
    list_container = tk.Frame(frame, bg=bg_color)
    list_container.pack(fill="both", expand=True, padx=24)

    results_list = ImportResultsList(
        parent=list_container, 
        on_import_click=open_modal_wrapper, 
        height=450,
        colors=colors # <--- ¡AQUÍ PASAMOS EL TEMA!
    )
    results_list.pack(fill="both", expand=True)

    # ==========================================
    # 6. PAGINACIÓN (Footer)
    # ==========================================
    pagination_frame = tk.Frame(frame, bg=bg_color)
    pagination_frame.pack(fill="x", padx=24, pady=16)
    
    # Texto de Info (Reactivo al tema)
    lbl_page_info = tk.Label(
        pagination_frame, 
        text="Cargando...", 
        bg=bg_color, 
        fg=text_color, 
        font=("Segoe UI", 10)
    )
    lbl_page_info.pack(side="left")
    
    # Botones Next/Prev
    buttons_frame = tk.Frame(pagination_frame, bg=bg_color)
    buttons_frame.pack(side="right")

    # Botón Anterior
    btn_prev = Pillow_Button(
        buttons_frame, 
        text="<", 
        variant="surface", 
        bg_parent=bg_color,      # Está sobre el fondo general
        dimensions=(40, 32, 8),
        on_click=lambda: dispatch(actions["changePage"](-1)),
        ui_mode=current_mode
    )
    btn_prev.pack(side="left", padx=8)

    # Botón Siguiente
    btn_next = Pillow_Button(
        buttons_frame, 
        text=">", 
        variant="surface",
        bg_parent=bg_color,
        dimensions=(40, 32, 8),
        on_click=lambda: dispatch(actions["changePage"](1)),
        ui_mode=current_mode
    )
    btn_next.pack(side="left")

    # ==========================================
    # 7. UPDATE UI LOGIC
    # ==========================================
    def update_ui(state):
        if not frame.winfo_exists(): return
        
        view_data = select_paginated_results(state)
        
        # Actualizar datos de la tabla
        if hasattr(results_list, 'set_data'):
            results_list.set_data(view_data["rows"])
        
        # Actualizar label de paginación
        info_text = f"Página {view_data['current_page']} de {view_data['total_pages']} ({view_data['total_items']} items)"
        lbl_page_info.config(text=info_text)

    # Suscripción
    unsubscribe = subscribe(update_ui)
    
    # Carga inicial de datos visuales
    update_ui(get_state())

    # Limpieza al destruir
    frame.bind("<Destroy>", lambda e: unsubscribe() if e.widget == frame else None)

    return frame