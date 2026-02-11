import tkinter as tk
from gui.components.inputs.SearchInput import SearchInput
from gui.theme.fonts import get_font
from gui.utils import get_circle_avatar 
from store.selectors import select_current_colors 
from store.slices.theme_slice import theme_actions 
# IMPORTAR ACCIONES DE INVENTARIO
from store.slices.inventory_slice import actions as inventory_actions 

def AppBar(parent, store_funcs, user_data):
    dispatch = store_funcs["dispatch"]
    get_state = store_funcs["get_state"]

    internal_state = {
        "current_page": "dashboard",
        "current_title": "Inicio"
    }

    # ==========================================
    # 1. CREACIÓN DE WIDGETS (Estructura)
    # ==========================================
    # Inicializamos sin colores específicos, 'update_theme_visuals' los pondrá.
    app_bar = tk.Frame(parent, height=64)
    app_bar.pack_propagate(False) 
    
    app_bar.columnconfigure(0, weight=0)
    app_bar.columnconfigure(1, weight=1)
    app_bar.columnconfigure(2, weight=0)

    # --- SECCIÓN IZQUIERDA ---
    left_frame = tk.Frame(app_bar)
    left_frame.grid(row=0, column=0, sticky="w", padx=(24, 12))
    
    lbl_logo = tk.Label(left_frame, text="LOGICMARKET", font=get_font("h5"), cursor="hand2")
    lbl_logo.pack(side="left")

    # --- SECCIÓN CENTRAL ---
    center_frame = tk.Frame(app_bar)
    center_frame.grid(row=0, column=1, sticky="ew")

    # --- SECCIÓN DERECHA ---
    right_frame = tk.Frame(app_bar)
    right_frame.grid(row=0, column=2, sticky="e", padx=(12, 24))

    # Botón Toggle Tema
    def toggle_theme():
        dispatch(theme_actions["toggleMode"]())
    
    btn_theme = tk.Label(right_frame, text="🌗", font=("Segoe UI Emoji", 14), cursor="hand2")
    btn_theme.pack(side="left", padx=8)
    btn_theme.bind("<Button-1>", lambda e: toggle_theme())

    # Notificaciones
    btn_notif = tk.Label(right_frame, text="🔔", font=("Segoe UI Emoji", 14), cursor="hand2")
    btn_notif.pack(side="left", padx=8)

    # Separador
    sep = tk.Frame(right_frame, width=1, height=24)
    sep.pack(side="left", padx=12)

    # Avatar Container
    avatar_container = tk.Frame(right_frame) 
    avatar_container.pack(side="left")
    
    # ==========================================
    # 2. LOGICA DE RENDERIZADO REACTIVO
    # ==========================================

    def render_center_content(colors):
        surface = colors["surface"]
        text = colors["text"]
        input_bg = colors["input_bg"]
        
        for w in center_frame.winfo_children(): w.destroy()

        page_id = internal_state["current_page"]
        
        # Solo mostramos el buscador en páginas relevantes
        if page_id in ["importer", "inventory"]:
            
            search_canvas, search_entry = SearchInput(
                center_frame,
                placeholder="Buscar productos...",
                width=480, height=44, radius=22,
                bg_color=input_bg,
                text_color=text
            )
            search_canvas.pack(anchor="center")
            
            # --- NUEVO: LÓGICA DE FILTRADO EN TIEMPO REAL ---
            def on_search_change(event):
                query = search_entry.get()
                # Despachamos al store global
                dispatch(inventory_actions["setSearchParams"]({"query": query}))

            # Vinculamos al soltar tecla para efecto inmediato
            search_entry.bind("<KeyRelease>", on_search_change)
            
            # Restaurar valor previo si existe en el store (para que no se borre al cambiar tema)
            current_params = get_state()["inventory"].get("search_params", {})
            if current_params.get("query"):
                search_entry.delete(0, tk.END)
                search_entry.insert(0, current_params["query"])
                search_entry.config(fg=text) # Quitar color de placeholder

        else:
            # HEADLINE
            tk.Label(center_frame, text=internal_state["current_title"], 
                     bg=surface, fg=text, font=get_font("h5")).pack(anchor="center")

    def update_avatar(surface_color, text_color): # <--- FIX: Recibe text_color explícitamente
        """Regenera el avatar para mezclar bordes con el nuevo fondo"""
        for w in avatar_container.winfo_children(): w.destroy()
        try:
            img = get_circle_avatar(user_data.get("avatar_path"), size=(32,32), bg_color=surface_color)
            if img:
                l = tk.Label(avatar_container, image=img, bg=surface_color, cursor="hand2")
                l.image = img
                l.pack()
                return
        except:
            pass
        
        # Fallback usando el text_color que recibimos
        tk.Label(avatar_container, text="👤", bg=surface_color, fg=text_color, font=("Arial", 16)).pack()

    def update_theme_visuals():
        """
        Función Maestra: Obtiene colores del store y actualiza TODOS los widgets existentes.
        Se llama desde main.py cuando cambia el tema.
        """
        # 1. Obtener colores frescos del Store
        colors = select_current_colors(get_state())
        
        surface = colors["surface"]
        text = colors["text"]
        
        # 2. Actualizar Contenedores
        app_bar.config(bg=surface)
        left_frame.config(bg=surface)
        center_frame.config(bg=surface)
        right_frame.config(bg=surface)
        avatar_container.config(bg=surface)
        
        # 3. Actualizar Widgets Estáticos
        lbl_logo.config(bg=surface, fg=text)
        btn_theme.config(bg=surface, fg=text)
        btn_notif.config(bg=surface, fg=text)
        
        # Separador cambia de color sutilmente según el tema
        sep_color = "#E0E2E5" if text == "#1A1C1E" else "#49454F"
        sep.config(bg=sep_color)
        
        # 4. Actualizar Componentes Complejos
        update_avatar(surface, text) # Pasamos ambos colores
        render_center_content(colors)

    def update_route(page_id, title=""):
        # Guardamos el estado de navegación
        internal_state["current_page"] = page_id
        internal_state["current_title"] = title
        
        # Al cambiar de ruta, necesitamos renderizar el centro de nuevo
        # Podemos reusar la lógica de tema para refrescar todo
        update_theme_visuals()

    # Inicialización: Aplicar tema por primera vez al crear
    update_theme_visuals()

    return {
        "widget": app_bar,
        "update_route": update_route,
        "update_theme": update_theme_visuals
    }