import tkinter as tk
from ui.components.Table import Table
# Ya no importamos Styled_Button porque se ve pixelado
from ui.components.buttons.Button import Pillow_Button 
from ui.components.inputs.Text_Input import Text_Input

def TabMonitor(parent, hooks, **props):
    # 1. Configuración del Fondo General
    parent.configure(bg=props['bg_app'])
    
    # --- SECCIÓN SUPERIOR: INPUT ---
    frame_top = tk.Frame(parent, bg=props['bg_app'])
    frame_top.pack(fill='x', pady=10, padx=10)
    
    # Input de Búsqueda
    _, search_entry = Text_Input(frame_top, "Buscar Producto: ", hooks, **props)
    
    # --- SECCIÓN DE ACCIONES (BOTONES) ---
    frame_btns = tk.Frame(frame_top, bg=props['bg_app'])
    frame_btns.pack(fill='x', pady=10) # Un poco más de aire vertical
    
    # BOTÓN 1: FILTRAR (Acción Principal - Violeta)
    # Usamos Pillow_Button para bordes suaves
    Pillow_Button(
        frame_btns, 
        text="🔍 Filtrar", 
        on_click=lambda: print("Filtrando..."), 
        hooks=hooks, 
        width=150,      # Un poco más compacto
        height=40, 
        radius=20,
        **props         # Hereda color primario (Violeta) por defecto
    ).pack(side='left', padx=5)

    # BOTÓN 2: RECARGAR (Acción Secundaria - Gris)
    # Sobrescribimos los colores 'primary' para que este botón sea gris
    Pillow_Button(
        frame_btns, 
        text="🔄 Recargar API", 
        on_click=lambda: print("Recargando..."), 
        hooks=hooks, 
        width=150, 
        height=40, 
        radius=20,        
        **props
    ).pack(side='left', padx=5)
    
    # --- SECCIÓN CENTRAL: TABLA ---
    cols = [
        {"id": "cod", "text": "Código", "width": 80},
        {"id": "prod", "text": "Producto", "width": 200},
        {"id": "marca", "text": "Marca", "width": 100},
        {"id": "cat", "text": "Categoría", "width": 200},
        {"id": "stock", "text": "Stock", "width": 60},
        {"id": "precio", "text": "Precio", "width": 80},
    ]
    
    dummy_data = [("001", "Leche", "Vita", "Lacteos", "10", "$0.80")]
    
    # La tabla debe manejar internamente su estilo, pero le pasamos props
    Table(parent, cols, dummy_data, hooks, **props)

    # --- SECCIÓN INFERIOR: STATUS ---
    # Importante: Definir fg inicial para que sea visible desde el arranque
    lbl_status = tk.Label(
        parent, 
        text="Total productos cargados: 1", 
        bg=props["bg_app"],
        fg=props["text_main"], # <--- AGREGADO: Color de texto inicial
        font=(props.get("font_family", "Arial"), 9)
    )
    lbl_status.pack(side='bottom', anchor="w", padx=10, pady=5)
    
    # --- SUSCRIPCIONES (HOOKS) ---
    # Actualizan los colores si cambias de tema en tiempo real
    hooks['subscribe'](lbl_status, lambda w, p: w.configure(bg=p['bg_app'], fg=p['text_main']))
    hooks['subscribe'](frame_top, lambda w, p: w.configure(bg=p['bg_app']))
    hooks['subscribe'](frame_btns, lambda w, p: w.configure(bg=p['bg_app']))