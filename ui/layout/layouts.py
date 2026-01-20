import tkinter as tk
from ui.components.Table import Table
# Ya no importamos Styled_Button porque se ve pixelado
from ui.components.buttons.Button import Pillow_Button 
from ui.components.buttons.Icon_Button import IconButton
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
    frame_actions = tk.Frame(frame_top, bg=props['bg_app'])
    frame_actions.pack(fill='x', pady=10) # Un poco más de aire vertical
    
    # Filter Icon Button
    IconButton(
        frame_actions,
        icon_path="filter_alt.svg", 
        on_click=lambda: print("Filter clicked"),
        hooks=hooks,
        size=28, # Slightly larger icon
        **props
    ).pack(side="left", padx=5)

    # Refresh Icon Button
    IconButton(
        frame_actions,
        icon_path="sync.svg",
        on_click=lambda: print("Refresh clicked"),
        hooks=hooks,
        size=28,
        **props
    ).pack(side="left", padx=5)
    
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
    hooks['subscribe'](frame_actions, lambda w, p: w.configure(bg=p['bg_app']))