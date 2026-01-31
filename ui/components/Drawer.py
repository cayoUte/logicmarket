import tkinter as tk
from ui import styles, utils
from ui.components.buttons.Button import Pillow_Button

def DrawerLayout(root, routes, hooks, **initial_props):
    """
    DrawerLayout: The main skeleton of the application.
    
    Args:
        root: The parent Tkinter widget.
        routes: Dictionary {'Route Name': render_function}.
        hooks: Dictionary for state management/event subscription.
        **initial_props: Theme properties and configuration.
    """
    defaults = styles.get_theme("light")
    props = utils.props_to_obj(defaults, initial_props)
    
    # --- 1. MAIN STRUCTURE (2-COLUMN GRID) ---
    # We use pack side='left' for the drawer and fill='both' for the content
    
    # Sidebar Container (Left)
    sidebar = tk.Frame(root, bg=props.bg_sidebar, width=250)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False) # Force fixed width
    
    # Vertical Divider Line (Aesthetic)
    tk.Frame(root, bg=props.divider, width=1).pack(side="left", fill="y")

    # Content Container (Right - Dynamic)
    content_area = tk.Frame(root, bg=props.bg_app)
    content_area.pack(side="right", expand=True, fill="both")

    # --- 2. NAVIGATION LOGIC (ROUTER) ---
    nav_state = {"current": list(routes.keys())[0]} # Store current route
    button_refs = {} # Store references to update button styles (Active/Inactive)

    def update_buttons():
        """Recorre los botones y llama a SU función de actualización específica."""
        # Desempaquetamos la tupla (widget, update_func)
        for route, (btn_widget, btn_update_func) in button_refs.items():
            is_active = (route == nav_state["current"])
            
            # Definimos estilos "Activo" vs "Inactivo"
            state_style = {
                 # Mezclamos props globales para mantener fuentes/tamaños
                **initial_props,
                "bg_app": props.bg_sidebar, 
                
                # Lógica Visual:
                # Si es activo, el color primario es el azul claro, si no, es transparente (bg_sidebar)
                "primary": props.sidebar_active if is_active else props.bg_sidebar,
                # El texto cambia de color
                "text_btn": props.sidebar_active_text if is_active else props.text_sidebar,
                # Hover estados
                "primary_active": props.sidebar_active,
                "primary_hover": props.sidebar_active if is_active else props.sidebar_active
            }
            
            # --- LA SOLUCIÓN ---
            # Llamamos directamente a la función de actualización que nos dio el botón
            btn_update_func(state_style)


    def navigate_to(route_name):
        # A. Actualizar Estado Visual de Botones PRIMERO
        nav_state["current"] = route_name
        update_buttons()

        # ... (Resto de la función navigate_to igual: limpiar y renderizar contenido) ...
        # B. Clear Content Area
        for widget in content_area.winfo_children():
            widget.destroy()
        # C. Render New View
        render_func = routes[route_name]
        render_func(content_area, hooks, **initial_props)
        # D. Ensure content area background is correct
        content_area.configure(bg=props.bg_app)

    # --- 3. SIDEBAR CONSTRUCTION ---
    
    # App Logo / Title
    lbl_logo = tk.Label(
        sidebar, 
        text="LogicMarket", 
        font=(props.family[0], 18, "bold"),
        bg=props.bg_sidebar,
        fg=props.primary,
        pady=30
    )
    lbl_logo.pack(anchor="center")

    # Generate Navigation Buttons
    for route_name in routes.keys():
        
        def create_command(r):
            return lambda: navigate_to(r)

        # Estilo inicial (Inactivo)
        nav_btn_style = {
            "bg_app": props.bg_sidebar,
            "primary": props.bg_sidebar,
            "text_btn": props.text_sidebar,
            "font_btn": (props.family[0], 11, "bold")
        }
        
        # --- CAMBIO AQUÍ ---
        # Recibimos EL WIDGET y LA FUNCIÓN DE UPDATE
        btn_widget, btn_update_func = Pillow_Button(
            sidebar, 
            text=route_name, 
            on_click=create_command(route_name), 
            hooks=hooks, 
            width=210, 
            height=45, 
            radius=10, 
            **nav_btn_style
        )
        btn_widget.pack(pady=5)
        
        # Guardamos ambos en el diccionario de referencias
        button_refs[route_name] = (btn_widget, btn_update_func)
        
    # Footer (Optional)
    tk.Label(
        sidebar, 
        text="v1.0.0", 
        bg=props.bg_sidebar, 
        fg=props.text_sidebar, 
        font=(props.family[0], 8)
    ).pack(side="bottom", pady=20)

    # --- 4. INITIAL LOAD ---
    # Load the first route by default
    # Al llamar esto aquí, se ejecutará update_buttons() y pintará el activo inicial
    navigate_to(list(routes.keys())[0]) 

    # Hooks globales
    hooks['subscribe'](sidebar, lambda w, p: w.configure(bg=p['bg_sidebar']))
    hooks['subscribe'](content_area, lambda w, p: w.configure(bg=p['bg_app']))