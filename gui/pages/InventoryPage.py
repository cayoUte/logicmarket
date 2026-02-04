import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# --- IMPORTS DE COMPONENTES ---
from gui.components.TextField import TextField
from gui.components.buttons.Button import Pillow_Button
from gui.components.buttons.IconButton import IconButton

# --- IMPORTS DE STORE Y TEMA ---
from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font
from store.selectors import select_current_colors, select_theme_mode
from gui.utils import get_circle_avatar 

# ==========================================
# COMPONENTE INTERNO: TABLA DE INVENTARIO
# ==========================================
class InventoryTable(tk.Frame):
    def __init__(self, parent, colors, on_action_click):
        super().__init__(parent, bg=colors["background"])
        self.colors = colors
        self.on_action_click = on_action_click
        
        # Configuración de colores
        self.bg = colors["background"]
        self.text_primary = colors["text"]
        
        # Ajuste de colores secundarios según tema
        is_dark = self.bg.startswith("#1") or self.bg.startswith("#2") or self.bg == "#000000"
        
        if is_dark:
            self.text_secondary = "#9CA3AF"
            self.divider_color = get_app_color("dark", 600)
            self.hover_color = get_app_color("dark", 700)
        else:
            self.text_secondary = get_app_color("neutral", 400)
            self.divider_color = get_app_color("neutral", 100) 
            self.hover_color = get_app_color("neutral", 50)

        # --- HEADER DE LA TABLA ---
        self.header = tk.Frame(self, bg=self.bg, pady=8, padx=16)
        self.header.pack(fill="x")
        
        headers = [
            ("PRODUCTO", 0.4), 
            ("CATEGORÍA", 0.2), 
            ("STOCK", 0.1), 
            ("PRECIO", 0.1), 
            ("ACCIÓN", 0.1)
        ]
        
        for text, weight in headers:
            lbl = tk.Label(
                self.header, 
                text=text, 
                bg=self.bg, 
                fg=self.text_secondary,
                font=("Segoe UI", 9, "bold"),
                anchor="w" if text != "ACCIÓN" else "center"
            )
            lbl.pack(side="left", fill="x", expand=True)

        # Separador Header
        tk.Frame(self, bg=self.divider_color, height=1).pack(fill="x")

        # --- AREA SCROLLABLE ---
        self.canvas = tk.Canvas(self, bg=self.bg, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=parent.winfo_width())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Binding para ajustar ancho
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas.find_all()[0], width=e.width))

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def render_rows(self, products, ui_mode):
        # Limpiar filas anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        if not products:
            tk.Label(
                self.scrollable_frame, 
                text="No hay productos en inventario.", 
                bg=self.bg, 
                fg=self.text_secondary, 
                pady=20
            ).pack()
            return

        for i, prod in enumerate(products):
            # Validamos que prod sea un diccionario
            if isinstance(prod, dict):
                self.create_row(prod, is_last=(i == len(products) - 1), ui_mode=ui_mode)

    def create_row(self, prod, is_last, ui_mode):
        # --- EXTRACCIÓN DEFENSIVA DE DATOS (FIX KEYERROR) ---
        # Usamos .get() para evitar crasheos si faltan datos en el JSON
        name = prod.get("name", "Producto Desconocido")
        code = prod.get("code", "S/N")
        brand = prod.get("brand", "Genérico")
        category = prod.get("category", "General")
        stock = prod.get("stock", 0)
        price = prod.get("price", 0.0)
        image_url = prod.get("image_url", None)

        # Contenedor de Fila
        row = tk.Frame(self.scrollable_frame, bg=self.bg, pady=12, padx=16)
        row.pack(fill="x", anchor="n")

        # --- COL 1: INFO PRODUCTO (Avatar + Nombre + Código) ---
        col_info = tk.Frame(row, bg=self.bg)
        col_info.pack(side="left", fill="x", expand=True)
        
        # Avatar (FIX AVATAR ERROR)
        try:
            # get_circle_avatar debe manejar paths None internamente, pero por si acaso:
            img_path = image_url if image_url else None
            avatar_bg = get_app_color("primary", 50)
            img = get_circle_avatar(img_path, size=(36,36), bg_color=avatar_bg)
            
            if img:
                lbl_img = tk.Label(col_info, image=img, bg=self.bg)
                lbl_img.image = img # Mantener referencia
                lbl_img.pack(side="left", padx=(0, 12))
            else:
                raise ValueError("Img None")
        except Exception:
            # Fallback si falla la carga de imagen
            tk.Label(col_info, text="📦", bg=self.bg, fg=self.text_secondary, font=("Arial", 16)).pack(side="left", padx=(0, 12))

        # Textos
        txt_frame = tk.Frame(col_info, bg=self.bg)
        txt_frame.pack(side="left", fill="x")
        
        tk.Label(
            txt_frame, 
            text=str(name)[:35], # Convertimos a str por seguridad
            bg=self.bg, 
            fg=self.text_primary, 
            font=("Segoe UI", 10, "bold"), 
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            txt_frame, 
            text=f"{code} • {brand}", 
            bg=self.bg, 
            fg=self.text_secondary, 
            font=("Segoe UI", 9), 
            anchor="w"
        ).pack(fill="x")

        # --- COL 2: CATEGORÍA ---
        col_cat = tk.Frame(row, bg=self.bg, width=150) 
        col_cat.pack_propagate(False)
        col_cat.pack(side="left", padx=10)
        
        tk.Label(
            col_cat, 
            text=str(category), 
            bg=self.bg, 
            fg=self.text_secondary, 
            anchor="w"
        ).pack(fill="x", expand=True)

        # --- COL 3: STOCK ---
        col_stock = tk.Frame(row, bg=self.bg, width=80)
        col_stock.pack_propagate(False)
        col_stock.pack(side="left", padx=10)
        
        # Color condicional para stock bajo
        try:
            stock_val = int(stock)
            stock_color = get_app_color("error", "Basic") if stock_val < 5 else self.text_primary
        except:
            stock_val = 0
            stock_color = self.text_primary
        
        tk.Label(
            col_stock, 
            text=f"{stock_val} u.", 
            bg=self.bg, 
            fg=stock_color, 
            font=("Segoe UI", 10, "bold")
        ).pack()

        # --- COL 4: PRECIO ---
        col_price = tk.Frame(row, bg=self.bg, width=80)
        col_price.pack_propagate(False)
        col_price.pack(side="left", padx=10)
        
        try:
            price_txt = f"${float(price):.2f}"
        except:
            price_txt = "$0.00"

        tk.Label(col_price, text=price_txt, bg=self.bg, fg=self.text_primary).pack()

        # --- COL 5: ACCIÓN (Expand More) ---
        col_action = tk.Frame(row, bg=self.bg, width=50)
        col_action.pack(side="right")
        
        # IconButton
        btn_more = IconButton(
            col_action,
            icon_path="more_vert.svg", 
            size=20,
            bg_parent=self.bg,
            variant="neutral",
            ui_mode=ui_mode,
            on_click=lambda p=prod: self.on_action_click(p)
        )
        btn_more.pack()

        # --- DIVIDER ---
        if not is_last:
            tk.Frame(self.scrollable_frame, bg=self.divider_color, height=1).pack(fill="x", padx=16)

        # --- HOVER EFFECT ---
        def on_enter(e):
            row.configure(bg=self.hover_color)
            col_info.configure(bg=self.hover_color)
            txt_frame.configure(bg=self.hover_color)
            col_cat.configure(bg=self.hover_color)
            col_stock.configure(bg=self.hover_color)
            col_price.configure(bg=self.hover_color)
            col_action.configure(bg=self.hover_color)

        def on_leave(e):
            row.configure(bg=self.bg)
            col_info.configure(bg=self.bg)
            txt_frame.configure(bg=self.bg)
            col_cat.configure(bg=self.bg)
            col_stock.configure(bg=self.bg)
            col_price.configure(bg=self.bg)
            col_action.configure(bg=self.bg)

        # Bind hover a todo
        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)
        for child in [col_info, txt_frame, col_cat, col_stock, col_price, col_action]:
             child.bind("<Enter>", on_enter)
             child.bind("<Leave>", on_leave)


# ==========================================
# PÁGINA PRINCIPAL: INVENTORY PAGE
# ==========================================
def InventoryPage(parent, store_funcs):
    dispatch = store_funcs["dispatch"]
    subscribe = store_funcs["subscribe"]
    get_state = store_funcs["get_state"]
    
    # 1. TEMAS Y COLORES
    state = get_state()
    current_mode = select_theme_mode(state)
    colors = select_current_colors(state)
    
    bg_color = colors["background"]
    text_color = colors["text"]

    # 2. CONTENEDOR PRINCIPAL
    frame = tk.Frame(parent, bg=bg_color)
    
    # ==========================================
    # HEADER
    # ==========================================
    header_frame = tk.Frame(frame, bg=bg_color)
    header_frame.pack(fill="x", padx=24, pady=(24, 0))
    
    tk.Label(
        header_frame, 
        text="Gestión de Inventario", 
        font=("Segoe UI", 20, "bold"),
        bg=bg_color, 
        fg=text_color
    ).pack(side="left")

    btn_add = Pillow_Button(
        header_frame,
        text="Nuevo Producto",
        variant="primary",
        bg_parent=bg_color,
        ui_mode=current_mode,
        dimensions=(140, 40, 20),
        on_click=lambda: print("Abrir modal manual")
    )
    btn_add.pack(side="right")

    # ==========================================
    # BARRA DE HERRAMIENTAS (Filtros)
    # ==========================================
    toolbar = tk.Frame(frame, bg=bg_color)
    toolbar.pack(fill="x", padx=24, pady=20)
    
    search_input = TextField(
        toolbar,
        placeholder="Filtrar inventario...",
        width=350,
        bg_parent=bg_color,
        ui_mode=current_mode,
        leading_icon="search.svg"
    )
    search_input.pack(side="left")
    
    # Callback Filtrado
    def on_search_change(event=None):
        query = search_input.get_value().lower()
        full_inventory = state["inventory"].get("inventario", [])
        
        # Filtrado defensivo (comprobar que los campos existen)
        filtered = []
        for p in full_inventory:
            p_name = p.get("name", "").lower()
            p_code = p.get("code", "").lower()
            p_brand = p.get("brand", "").lower()
            
            if query in p_name or query in p_code or query in p_brand:
                filtered.append(p)
                
        table.render_rows(filtered, current_mode)

    # El entry_widget ahora sí existe gracias al fix anterior
    if hasattr(search_input, 'entry_widget'):
        search_input.entry_widget.bind("<KeyRelease>", on_search_change)

    # ==========================================
    # TABLA
    # ==========================================
    def handle_row_action(product):
        print(f"🔧 Acción: {product.get('name')}")

    table_container = tk.Frame(frame, bg=bg_color)
    table_container.pack(fill="both", expand=True, padx=24, pady=(0, 24))

    table = InventoryTable(table_container, colors, on_action_click=handle_row_action)
    table.pack(fill="both", expand=True)

    # ==========================================
    # LOGICA UPDATE
    # ==========================================
    def update_ui(new_state):
        if not frame.winfo_exists(): return
        
        # Recuperación segura del inventario
        inventory_slice = new_state.get("inventory", {})
        inventory_data = inventory_slice.get("inventario", [])
        
        table.render_rows(inventory_data, current_mode)

    unsubscribe = subscribe(update_ui)
    
    # Carga inicial (Defensiva)
    try:
        update_ui(get_state())
    except Exception as e:
        print(f"Error renderizado inicial: {e}")

    frame.bind("<Destroy>", lambda e: unsubscribe() if e.widget == frame else None)

    return frame