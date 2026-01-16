import tkinter as tk
from ui.components.Table import Table
from ui.components.buttons.Button import Button, Styled_Button
from ui.components.inputs.Text_Input import Text_Input

def TabMonitor(parent, hooks, **props):
    frame_top = tk.Frame(parent, bg=props['bg_app'])
    frame_top.pack(fill='x', pady=10, padx=10)
    
    _, search_entry = Text_Input(frame_top, "Buscar Producto: ", hooks, **props)
    
    frame_btns = tk.Frame(frame_top, bg=props['bg_app'])
    frame_btns.pack(fill='x', pady=5)
    Styled_Button(
    frame_btns, 
    "Filtrar", 
    lambda: print("Click!"), 
    hooks, 
    width=200, 
    height=40, 
    radius=20,
    **props
).pack(side='left', padx=5)
    # Button(frame_btns, "🔍 Filtrar", lambda: print("Fltrando..."), hooks, **props).pack(side='left', padx=5)
    
    Button(frame_btns, '🔄️ Recargar API', lambda: print("Seeding..."), hooks, type="secondary").pack(side='left')
    
    cols = [
        {"id": "cod", "text": "Código", "width": 80},
        {"id": "prod", "text": "Producto", "width": 200},
        {"id": "marca", "text": "Marca", "width": 100},
        {"id": "cat", "text": "Categoría", "width": 200},
        {"id": "stock", "text": "Stock", "width": 60},
        {"id": "precio", "text": "Precio", "width": 80},
    ]
    
    dummy_data = [("001", "Leche", "Vita", "Lacteos", "10", "$0.80")]
    
    Table(parent, cols, dummy_data, hooks, **props)

    lbl_status = tk.Label(parent, text="Total productos cargados: 1", bg=props["bg_app"])
    lbl_status.pack(side='bottom', anchor="w", padx=10, pady=5)
    hooks['subscribe'](lbl_status, lambda w, p: w.configure(bg=p['bg_app'], fg=p['text_main']))