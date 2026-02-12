import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from gui.components.buttons.IconButton import IconButton

from gui.components.menus.PopupMenu import PopupMenu
from gui.components.modals.ConfirmDialog import ConfirmDialog
from gui.components.modals.CreateModal import CreateModal
from gui.components.modals.UpdateModal import UpdateModal

from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font
from store.selectors import select_current_colors, select_theme_mode
from gui.utils import get_circle_avatar
from store.slices.inventory_slice import actions as inventory_actions


class InventoryTable(tk.Frame):
    def __init__(self, parent, colors, on_action_click):
        super().__init__(parent, bg=colors["background"])
        self.colors = colors
        self.on_action_click = on_action_click

        self.bg = colors["background"]
        self.text_primary = colors["text"]

        is_dark = (
            self.bg.startswith("#1") or self.bg.startswith("#2") or self.bg == "#000000"
        )
        if is_dark:
            self.text_secondary = "#9CA3AF"
            self.divider_color = get_app_color("dark", 600)
            self.hover_color = get_app_color("dark", 700)
        else:
            self.text_secondary = get_app_color("neutral", 400)
            self.divider_color = get_app_color("neutral", 100)
            self.hover_color = get_app_color("neutral", 50)

        self.col_config = {
            0: {"weight": 1, "minsize": 250},
            1: {"weight": 0, "minsize": 150},
            2: {"weight": 0, "minsize": 100},
            3: {"weight": 0, "minsize": 100},
            4: {"weight": 0, "minsize": 60},
        }

        self.header = tk.Frame(self, bg=self.bg, pady=8, padx=16)
        self.header.pack(fill="x")

        for col, cfg in self.col_config.items():
            self.header.grid_columnconfigure(
                col, weight=cfg["weight"], minsize=cfg["minsize"]
            )

        headers = ["PRODUCTO", "CATEGORÍA", "STOCK", "PRECIO", "ACCIÓN"]

        for i, text in enumerate(headers):
            lbl = tk.Label(
                self.header,
                text=text,
                bg=self.bg,
                fg=self.text_secondary,
                font=("Segoe UI", 9, "bold"),
                anchor="w" if text != "ACCIÓN" else "center",
            )
            lbl.grid(row=0, column=i, sticky="ew")

        tk.Frame(self, bg=self.divider_color, height=1).pack(fill="x")

        self.canvas = tk.Canvas(self, bg=self.bg, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def render_rows(self, products, ui_mode):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not products:
            tk.Label(
                self.scrollable_frame,
                text="No se encontraron productos.",
                bg=self.bg,
                fg=self.text_secondary,
                pady=20,
            ).pack()
            return

        for i, prod in enumerate(products):
            if isinstance(prod, dict):
                self.create_row(prod, is_last=(i == len(products) - 1), ui_mode=ui_mode)

    def create_row(self, prod, is_last, ui_mode):
        name = prod.get("name") or prod.get("product_name") or "Sin Nombre"
        code = prod.get("code") or prod.get("_id") or "---"
        brand = prod.get("brand") or "Genérico"
        category = prod.get("category") or "General"
        stock = prod.get("stock") or 0
        price = prod.get("price") or 0.0
        image_url = prod.get("image_url")

        row = tk.Frame(self.scrollable_frame, bg=self.bg, pady=8, padx=16)
        row.pack(fill="x", anchor="n")

        for col, cfg in self.col_config.items():
            row.grid_columnconfigure(col, weight=cfg["weight"], minsize=cfg["minsize"])

        cell_info = tk.Frame(row, bg=self.bg)
        cell_info.grid(row=0, column=0, sticky="ew")

        try:
            avatar_bg = get_app_color("primary", 50)
            img = get_circle_avatar(image_url, size=(32, 32), bg_color=avatar_bg)
            if img:
                lbl_img = tk.Label(cell_info, image=img, bg=self.bg)
                lbl_img.image = img
                lbl_img.pack(side="left", padx=(0, 10))
            else:
                tk.Label(
                    cell_info, text="📦", bg=self.bg, font=("Segoe UI Emoji", 14)
                ).pack(side="left", padx=(0, 10))
        except e:
            tk.Label(cell_info, text="📦", bg=self.bg).pack(side="left", padx=(0, 10))

        txt_frame = tk.Frame(cell_info, bg=self.bg)
        txt_frame.pack(side="left", fill="x")

        tk.Label(
            txt_frame,
            text=str(name)[:35],
            bg=self.bg,
            fg=self.text_primary,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            txt_frame,
            text=f"{code} • {brand}",
            bg=self.bg,
            fg=self.text_secondary,
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            row, text=str(category), bg=self.bg, fg=self.text_secondary, anchor="w"
        ).grid(row=0, column=1, sticky="ew", padx=5)

        try:
            s_val = int(stock)
            s_color = (
                get_app_color("error", "Basic") if s_val < 5 else self.text_primary
            )
        except e:
            s_val, s_color = 0, self.text_primary

        tk.Label(
            row,
            text=f"{s_val} u.",
            bg=self.bg,
            fg=s_color,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        ).grid(row=0, column=2, sticky="ew", padx=5)

        try:
            p_txt = f"${float(price):.2f}"
        except e:
            p_txt = "$0.00"
        tk.Label(row, text=p_txt, bg=self.bg, fg=self.text_primary, anchor="w").grid(
            row=0, column=3, sticky="ew", padx=5
        )

        action_cell = tk.Frame(row, bg=self.bg)
        action_cell.grid(row=0, column=4)

        btn = IconButton(
            action_cell,
            icon_path="more_vert.svg",
            size=20,
            bg_parent=self.bg,
            variant="neutral",
            ui_mode=ui_mode,
            on_click=None,
        )

        def manual_click(e):
            x_root, y_root = e.x_root, e.y_root
            self.on_action_click(prod, x_root, y_root)

        btn.bind("<Button-1>", manual_click)
        btn.pack()

        if not is_last:
            div = tk.Frame(self.scrollable_frame, bg=self.divider_color, height=1)
            div.pack(fill="x", padx=16)

        def set_hover_bg(widget, color):
            try:
                widget.configure(bg=color)
            except:
                pass
            for child in widget.winfo_children():
                set_hover_bg(child, color)

        def on_enter(e):
            set_hover_bg(row, self.hover_color)

        def on_leave(e):
            set_hover_bg(row, self.bg)

        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)


def InventoryPage(parent, store_funcs):
    dispatch = store_funcs["dispatch"]
    subscribe = store_funcs["subscribe"]
    get_state = store_funcs["get_state"]

    state = get_state()
    current_mode = select_theme_mode(state)
    colors = select_current_colors(state)

    bg_color = colors["background"]
    text_color = colors["text"]

    frame = tk.Frame(parent, bg=bg_color)

    header_frame = tk.Frame(frame, bg=bg_color)
    header_frame.pack(fill="x", padx=24, pady=(24, 0))

    tk.Label(
        header_frame,
        text="Gestión de Inventario",
        font=("Segoe UI", 20, "bold"),
        bg=bg_color,
        fg=text_color,
    ).pack(side="left")

    def open_create_modal():
        def handle_create(new_data):
            print(f"✨ Creando: {new_data['name']}")
            dispatch(inventory_actions["createProduct"](new_data))

        CreateModal(parent=frame, on_confirm=handle_create, ui_mode=current_mode)

    btn_add = IconButton(
        header_frame,
        icon_path="add_circle.svg",
        size=32,
        variant="primary",
        bg_parent=bg_color,
        ui_mode=current_mode,
        on_click=open_create_modal,
    )
    btn_add.pack(side="right")

    def do_delete(product):
        stock = int(product.get("stock", 0))

        if stock > 0:
            ConfirmDialog(
                parent=frame,
                title="No se puede eliminar",
                message=f"El producto '{product.get('name')}' tiene {stock} unidades. Debes dejar el stock en 0 antes de borrarlo.",
                is_error=True,
                ui_mode=current_mode,
            )
        else:

            def confirm_deletion():
                print(f"🗑️ Eliminando: {product.get('code')}")
                dispatch(inventory_actions["deleteProduct"](product["code"]))

            ConfirmDialog(
                parent=frame,
                title="Confirmar eliminación",
                message=f"¿Eliminar '{product.get('name')}' permanentemente?",
                on_confirm=confirm_deletion,
                ui_mode=current_mode,
            )

    def do_update(product):
        def save_changes(updated_data):
            print(f"💾 Guardando cambios: {updated_data['code']}")
            dispatch(inventory_actions["updateProduct"](updated_data))

        UpdateModal(
            parent=frame,
            current_data=product,
            on_confirm=save_changes,
            ui_mode=current_mode,
        )

    def handle_row_action(product, x, y):
        actions_list = [
            {
                "label": "Actualizar",
                "icon": "edit.svg",
                "command": lambda: do_update(product),
            },
            {"type": "divider"},
            {
                "label": "Eliminar",
                "icon": "delete.svg",
                "is_destructive": True,
                "command": lambda: do_delete(product),
            },
        ]

        PopupMenu(parent=frame, x=x, y=y, menu_items=actions_list, ui_mode=current_mode)

    table_container = tk.Frame(frame, bg=bg_color)
    table_container.pack(fill="both", expand=True, padx=24, pady=24)

    table = InventoryTable(table_container, colors, on_action_click=handle_row_action)
    table.pack(fill="both", expand=True)

    def update_ui(new_state):
        if not frame.winfo_exists():
            return

        inventory_slice = new_state.get("inventory", {})
        full_data = inventory_slice.get("inventario", [])

        search_params = inventory_slice.get("search_params", {})
        query = search_params.get("query", "").lower()

        if query:
            filtered = []
            for p in full_data:
                p_str = (
                    str(p.get("name")) + str(p.get("code")) + str(p.get("brand"))
                ).lower()
                if query in p_str:
                    filtered.append(p)
        else:
            filtered = full_data

        table.render_rows(filtered, current_mode)

    unsubscribe = subscribe(update_ui)

    try:
        update_ui(get_state())
    except Exception as e:
        print(f"InventoryPage Init Error: {e}")

    frame.bind("<Destroy>", lambda e: unsubscribe() if e.widget == frame else None)

    return frame
