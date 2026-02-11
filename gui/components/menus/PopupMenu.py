import tkinter as tk
from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font
from gui.theme.menus import get_menu_theme, MENU_SPECS
from gui.components.buttons.IconButton import IconButton

def PopupMenu(parent, x, y, menu_items, ui_mode="light"):
    """
    Componente funcional para mostrar un menú flotante.
    
    Args:
        menu_items (list): Lista de dicts. Ejemplo:
            [
                {"label": "Editar", "icon": "edit.svg", "command": func},
                {"type": "divider"},
                {"label": "Borrar", "is_destructive": True}
            ]
    """
    
    # 1. Configuración de Ventana
    menu = tk.Toplevel(parent)
    menu.overrideredirect(True) # Sin bordes
    menu.attributes("-topmost", True)
    
    # 2. Tema
    theme = get_menu_theme(ui_mode)
    
    # Helpers de color
    def resolve(val):
        return get_app_color(val[0], val[1]) if isinstance(val, (tuple, list)) else val

    bg_color = resolve(theme["bg"])
    text_color = resolve(theme["text"])
    hover_color = resolve(theme["hover"])
    
    menu.configure(bg=bg_color)
    
    # 3. Contenedor
    container = tk.Frame(menu, bg=bg_color, relief="flat", bd=0)
    container.pack(fill="both", expand=True, pady=MENU_SPECS["padding_vertical"])

    # 4. Renderizado de Items
    items_count = 0
    
    for item in menu_items:
        # A. MANEJO DE DIVISORES
        if item.get("type") == "divider":
            div_color = resolve(theme["divider"])
            tk.Frame(container, bg=div_color, height=1).pack(fill="x", pady=4)
            continue

        # B. MANEJO DE ITEMS NORMALES
        items_count += 1
        label = item.get("label", "Item")
        icon = item.get("icon")
        command = item.get("command")
        is_destructive = item.get("is_destructive", False)
        disabled = item.get("disabled", False)

        item_frame = tk.Frame(container, bg=bg_color, height=MENU_SPECS["item_height"])
        item_frame.pack(fill="x")
        item_frame.pack_propagate(False)

        # Colores del Item
        if disabled:
            fg_color = resolve(theme["text_disabled"])
        elif is_destructive:
            fg_color = get_app_color("error", "Basic")
        else:
            fg_color = text_color

        # Icono (Leading)
        if icon:
            icon_variant = "error" if is_destructive else "neutral"
            # Usamos IconButton pero desactivamos su click interno
            btn_icon = IconButton(
                item_frame, icon_path=icon, size=20, 
                bg_parent=bg_color, variant=icon_variant, ui_mode=ui_mode,
                on_click=None
            )
            btn_icon.place(x=12, rely=0.5, anchor="w")
            
            # Hack: Propagar eventos del icono al frame padre
            for child in btn_icon.winfo_children():
                child.bindtags((child, item_frame, ".", "all"))

        # Etiqueta
        lbl_x = 48 if icon else 16
        lbl = tk.Label(
            item_frame, text=label, bg=bg_color, fg=fg_color,
            font=get_font("body"), anchor="w"
        )
        lbl.place(x=lbl_x, rely=0.5, anchor="w")

        # C. EVENTOS (Hover y Click)
        if not disabled:
            def on_click(e, cmd=command):
                menu.destroy()
                if cmd: cmd()

            def on_enter(e, f=item_frame, l=lbl):
                f.configure(bg=hover_color)
                l.configure(bg=hover_color)

            def on_leave(e, f=item_frame, l=lbl):
                f.configure(bg=bg_color)
                l.configure(bg=bg_color)

            # Bindings a todo el frame y sus hijos
            for w in [item_frame, lbl]:
                w.bind("<Enter>", on_enter)
                w.bind("<Leave>", on_leave)
                w.bind("<Button-1>", on_click)

    # 5. Geometría y Cierre
    # Calcular altura basada en items (aprox)
    total_h = (items_count * MENU_SPECS["item_height"]) + (MENU_SPECS["padding_vertical"] * 2) + (len(menu_items) * 2)
    
    # Ajuste de posición (x - width para que salga a la izquierda del cursor)
    menu.geometry(f"{MENU_SPECS['width']}x{total_h}+{x-MENU_SPECS['width']}+{y}")

    # Cerrar al perder foco
    menu.bind("<FocusOut>", lambda e: menu.destroy())
    menu.bind("<Button-1>", lambda e: menu.destroy()) # Click fuera
    
    menu.focus_set()
    
    return menu