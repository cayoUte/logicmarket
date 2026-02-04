import tkinter as tk
from gui.components.Table import Table
from gui.components.buttons.Button import Pillow_Button

def InventoryPage(parent):

    # --- 1. CONFIGURACIÓN GENERAL ---
    bg_color = "#ffffff" # Fondo de la página
    frame = tk.Frame(parent, bg=bg_color)
    
    # Título (Opcional, si no está en el layout global)
    # tk.Label(frame, text="Inventario", font=("Segoe UI", 20, "bold"), bg=bg_color).pack(pady=(20, 10), padx=30, anchor="w")

    # ==========================================
    # 2. ACTION BAR (Barra de Herramientas)
    # ==========================================
    action_bar = tk.Frame(frame, bg=bg_color)
    action_bar.pack(fill="x", padx=30, pady=20)

    # --- ZONA IZQUIERDA (Búsqueda + Filtro) ---
    left_actions = tk.Frame(action_bar, bg=bg_color)
    left_actions.pack(side="left")

    
    

    # B. Botón Filtrar (Oscuro con Lupa)
    def on_filter():
        # term = search_input.get_value()
        print(f"Filtrando por: {'...' }")

    btn_filter = Pillow_Button(
        left_actions,
        text="Filtrar",
        icon_path="search.svg", # Asegúrate de tener este icono
        on_click=on_filter,
        dimensions=(110, 35, 10), # Más compacto (height 35 coincide con TextInput)
        variant="dark" # Tema oscuro nuevo
    )
    btn_filter.pack(side="left")

    # --- ZONA DERECHA (Recargar API) ---
    # C. Botón Recargar (Blanco con Borde)
    def on_reload():
        print("Recargando API...")
        # Aquí llamarías a tu lógica de fetch
    
    btn_reload = Pillow_Button(
        action_bar,
        text="Recargar API",
        icon_path="sync.svg", # Asegúrate de tener este icono
        on_click=on_reload,
        dimensions=(140, 35, 10),
        variant="surface" # Tema blanco con borde nuevo
    )
    btn_reload.pack(side="right")

    # ==========================================
    # 3. TABLA DE DATOS
    # ==========================================
    
    # Columnas
    cols = [
        {"id": "id", "text": "ID", "width": 50},
        {"id": "prod", "text": "Producto", "width": 250},
        {"id": "cat", "text": "Categoría", "width": 120},
        {"id": "stock", "text": "Stock", "width": 80},
        {"id": "price", "text": "Precio", "width": 100},
        {"id": "status", "text": "Estado", "width": 100},
    ]
    
    # Datos de ejemplo
    dummy_data = [
        ("001", "Laptop Gamer X1", "Electrónica", 15, "$1200.00", "Activo"),
        ("002", "Mouse Inalámbrico", "Accesorios", 120, "$25.50", "Activo"),
        ("003", "Monitor 4K 27''", "Electrónica", 8, "$350.00", "Bajo Stock"),
        ("004", "Teclado Mecánico", "Accesorios", 45, "$85.00", "Activo"),
    ]

    table = Table(
        frame,
        columns=cols,
        data=dummy_data,
        variant="primary",
        height=20
    )
    table.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    return frame


    
