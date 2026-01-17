import tkinter as tk
from types import SimpleNamespace
from ui.components.buttons.Button import Pillow_Button # Reusamos tu botón con pillow

def DrawerLayout(root, rutas, hooks, **props):
    """
    rutas: Diccionario {'Nombre': funcion_renderizadora}
    """
    p = SimpleNamespace(**props)
    
    # --- 1. ESTRUCTURA PRINCIPAL (GRID 2 COLUMNAS) ---
    # Usamos pack side='left' para el drawer y fill='both' para el contenido
    
    # Contenedor del Sidebar (Izquierda)
    sidebar = tk.Frame(root, bg=p.bg_sidebar, width=250)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False) # Forzar ancho fijo
    
    # Línea divisoria vertical (Estética)
    tk.Frame(root, bg=p.divider, width=1).pack(side="left", fill="y")

    # Contenedor de Contenido (Derecha - Dinámico)
    content_area = tk.Frame(root, bg=p.bg_app)
    content_area.pack(side="right", expand=True, fill="both")

    # --- 2. LOGICA DE NAVEGACIÓN (ROUTER) ---
    estado_nav = {"actual": list(rutas.keys())[0]} # Guardamos la ruta actual
    botones_refs = {} # Para actualizar estilos de botones (activo/inactivo)

    def navegar_a(nombre_ruta):
        # A. Actualizar Estado Visual de Botones
        estado_nav["actual"] = nombre_ruta
        actualizar_botones()

        # B. Limpiar Área de Contenido
        for widget in content_area.winfo_children():
            widget.destroy()
        
        # C. Renderizar Nueva Vista
        render_func = rutas[nombre_ruta]
        render_func(content_area, hooks, **props)
        
        # D. Asegurar que el fondo del content area sea correcto
        content_area.configure(bg=p.bg_app)

    def actualizar_botones():
        """Recorre los botones y cambia su color según si están activos"""
        for ruta, btn_update_func in botones_refs.items():
            es_activo = (ruta == estado_nav["actual"])
            
            # Definimos estilos "Activo" vs "Inactivo"
            nuevos_estilos = {
                "bg_app": p.sidebar_active if es_activo else p.bg_sidebar, # Fondo del botón
                "primary": p.bg_sidebar, # Truco: Fondo transparente simulado
                "text_btn": p.sidebar_active_text if es_activo else p.text_sidebar,
                # Quitamos sombra o elevación si no está activo
                "primary_active": p.sidebar_active,
                "primary_hover": p.sidebar_active if es_activo else "#f5f5f5"
            }
            # Llamamos al hook de actualización del botón (asumiendo que Pillow_Button lo expone)
            # NOTA: Pillow_Button necesita exponer una forma de actualizarse. 
            # Si usas el sistema reactivo, esto se hace solo al redibujar, 
            # pero aquí forzamos un redibujado manual o usamos hooks.
            pass 

    # --- 3. CONSTRUCCIÓN DEL SIDEBAR ---
    
    # Logo / Título de la App
    lbl_logo = tk.Label(
        sidebar, 
        text="LogicMarket", 
        font=(p.family[0], 18, "bold"),
        bg=p.bg_sidebar,
        fg=p.primary,
        pady=30
    )
    lbl_logo.pack(anchor="center")

    # Generar Botones de Navegación
    for nombre_ruta in rutas.keys():
        
        # Wrapper para capturar el nombre de la ruta en la lambda
        def crear_comando(r):
            return lambda: navegar_a(r)

        # Usamos Pillow_Button pero "Plano" (estilo Ghost)
        # Necesitamos pasarle colores específicos para que parezca menú
        estilo_btn_nav = {
            **props,
            "bg_app": p.bg_sidebar, # El fondo del canvas debe coincidir con el sidebar
            "primary": p.bg_sidebar, # Color base (transparente visualmente)
            "text_btn": p.text_sidebar,
            "font_btn": (p.family[0], 11, "bold")
        }
        
        btn = Pillow_Button(
            sidebar, 
            text=nombre_ruta, 
            on_click=crear_comando(nombre_ruta), 
            hooks=hooks, 
            width=210, 
            height=45, 
            radius=10, 
            **estilo_btn_nav
        )
        btn.pack(pady=5)
        
    # Footer (Opcional)
    tk.Label(
        sidebar, 
        text="v1.0.0", 
        bg=p.bg_sidebar, 
        fg=p.text_sidebar, 
        font=(p.family[0], 8)
    ).pack(side="bottom", pady=20)

    # --- 4. CARGA INICIAL ---
    navegar_a(list(rutas.keys())[0])

    # Hooks para Tema (Reactividad global)
    hooks['subscribe'](sidebar, lambda w, prop: w.configure(bg=prop['bg_sidebar']))
    hooks['subscribe'](content_area, lambda w, prop: w.configure(bg=prop['bg_app']))