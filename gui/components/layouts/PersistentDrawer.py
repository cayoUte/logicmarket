import tkinter as tk
from gui.theme.app_pallete import get_app_color
from gui.components.buttons.IconButton import IconButton
from gui.theme.layouts import get_drawer_theme # <--- IMPORTAR TEMA

def PersistentDrawer(
    parent, 
    nav_items, 
    on_navigate, 
    width=70, 
    ui_mode="light",  # <--- NUEVO: Argumento de modo
    variant="primary" # (Opcional) Sobrescribir variante de iconos si se desea
):
    """
    Barra lateral funcional y reactiva al tema.
    """

    # 1. RESOLVER COLORES DEL TEMA
    theme = get_drawer_theme(mode=ui_mode)
    
    def resolve(val):
        return get_app_color(val[0], val[1]) if isinstance(val, (tuple, list)) else val

    bg_color = resolve(theme["bg"])
    border_color = resolve(theme["border"])
    
    # Variante de iconos: Usamos la del argumento o la sugerida por el tema
    icon_variant = variant if variant != "primary" else theme["icon_variant"]

    # 2. ESTRUCTURA
    frame = tk.Frame(parent, width=width, bg=bg_color)
    frame.pack_propagate(False)

    buttons_registry = {}
    state = {"current_id": None}

    # 3. LÓGICA DE SELECCIÓN
    def handle_selection(target_id):
        # Si clica el mismo, no hacemos nada
        if state["current_id"] == target_id:
            return

        # Deseleccionar anterior
        old_id = state["current_id"]
        if old_id and old_id in buttons_registry:
            # Importante: los IconButtons deben tener el método .set_selected expuesto
            if hasattr(buttons_registry[old_id], 'set_selected'):
                buttons_registry[old_id].set_selected(False)

        # Seleccionar nuevo
        if target_id in buttons_registry:
            if hasattr(buttons_registry[target_id], 'set_selected'):
                buttons_registry[target_id].set_selected(True)
            state["current_id"] = target_id

        # Ejecutar callback
        if on_navigate:
            on_navigate(target_id)

    # Espaciador superior
    tk.Frame(frame, height=20, bg=bg_color).pack()

    # 4. GENERACIÓN DE BOTONES
    for item in nav_items:
        item_id = item["id"]
        icon_path = item["icon"]

        # Closure para capturar el ID correcto
        def on_btn_click(uid=item_id):
            handle_selection(uid)

        # Instanciar IconButton con el contexto correcto
        btn_widget = IconButton(
            frame, 
            icon_path=icon_path, 
            on_click=on_btn_click, 
            size=24, 
            variant=icon_variant,
            bg_parent=bg_color, # <--- CLAVE: Para que se funda con el drawer
            ui_mode=ui_mode     # <--- CLAVE: Para que el icono sepa si ser blanco/negro
        )
        btn_widget.pack(pady=8)

        buttons_registry[item_id] = btn_widget

    # 5. BORDE DERECHO (Separador)
    border = tk.Frame(frame, bg=border_color, width=1)
    border.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

    # Exponer método público
    frame.select_item = handle_selection

    return frame