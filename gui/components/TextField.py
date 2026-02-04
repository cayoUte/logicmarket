import tkinter as tk
from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font
from gui.theme.inputs import get_textfield_theme # <--- IMPORTANTE
from gui.components.buttons.IconButton import IconButton

def TextField(
    parent, 
    label="Label", 
    placeholder="", 
    width=250, 
    leading_icon=None, 
    trailing_icon=None, 
    on_trailing_click=None,
    supporting_text=None,
    is_password=False,
    validator=None,
    initial_value="",
    ui_mode="light",   # <--- NUEVO: Argumento para el tema
    bg_parent=None     # <--- NUEVO: Para que el wrapper se funda con el fondo
):
    
    # --- 1. RESOLUCIÓN DE COLORES ---
    # Obtenemos la configuración cruda del tema
    theme_config = get_textfield_theme(mode=ui_mode)
    
    # Helper para convertir tuplas ("primary", 500) a Hex
    def resolve(val):
        if isinstance(val, (tuple, list)) and len(val) == 2:
            return get_app_color(val[0], val[1])
        return val

    # Diccionario COLORS final con valores Hex
    COLORS = {k: resolve(v) for k, v in theme_config.items()}
    
    # Detectar fondo del padre si no se pasa explícitamente
    if not bg_parent:
        try:
            bg_parent = parent.cget("bg")
        except:
            bg_parent = "#FFFFFF"

    state = {
        "focused": False,
        "error": False,
        "hover": False
    }

    # --- 2. ESTRUCTURA WRAPPER ---
    # Usamos bg_parent para que el wrapper sea invisible
    wrapper = tk.Frame(parent, bg=bg_parent, highlightthickness=0) 

    # Contenedor Visual (Caja Filled)
    container = tk.Frame(wrapper, bg=COLORS["bg_idle"], width=width, height=56, cursor="xterm")
    container.pack_propagate(False)
    container.pack(fill="x", anchor="n")

    # Indicador Inferior
    indicator = tk.Frame(container, bg=COLORS["indicator_idle"], height=1)
    indicator.place(relx=0, rely=1.0, relwidth=1.0, anchor="sw")

    # --- 3. ELEMENTOS INTERNOS ---
    padding_left = 16 if not leading_icon else 48
    padding_right = 16 if not trailing_icon else 48

    # Iconos (Leading / Trailing)
    # Importante: Pasar ui_mode a los IconButtons internos
    if leading_icon:
        icon_lead = IconButton(
            container, icon_path=leading_icon, on_click=lambda: entry.focus_set(), 
            size=24, bg_parent=COLORS["bg_idle"], variant="neutral", ui_mode=ui_mode
        )
        icon_lead.place(x=12, rely=0.5, anchor="w")

    if trailing_icon:
        icon_trail = IconButton(
            container, icon_path=trailing_icon, on_click=on_trailing_click,
            size=24, bg_parent=COLORS["bg_idle"], variant="neutral", ui_mode=ui_mode
        )
        icon_trail.place(relx=1.0, x=-12, rely=0.5, anchor="e")

    # Entry (Campo de Texto)
    entry = tk.Entry(
        container,
        bg=COLORS["bg_idle"],
        fg=COLORS["text"],
        insertbackground=COLORS["caret"], # Color del cursor
        font=get_font("body"), 
        relief="flat",
        highlightthickness=0,
        show="*" if is_password else ""
    )
    entry.place(
        x=padding_left, 
        y=24, 
        width=width - padding_left - padding_right, 
        height=24
    )
    
    # Label Flotante
    lbl_widget = tk.Label(
        container,
        text=label,
        bg=COLORS["bg_idle"],
        fg=COLORS["label_idle"],
        font=get_font("body"),
        anchor="w"
    )

    # Supporting Text (Error msg)
    # bg debe ser bg_parent para que se vea sobre el fondo de la app, no dentro del input
    lbl_support = tk.Label(
        wrapper,
        text="",
        bg=bg_parent, 
        fg=COLORS["supporting"],
        font=get_font("input"),
        anchor="w",
        justify="left",
        wraplength=width
    )

    if initial_value:
        entry.insert(0, initial_value)

    # --- 4. LÓGICA DE ACTUALIZACIÓN ---
    
    def update_visuals(force_idle=False):
        has_content = len(entry.get()) > 0
        is_active = state["focused"] or has_content

        # A. Determinar Colores
        if state["error"]:
            lbl_color = COLORS["label_error"]
            ind_color = COLORS["indicator_error"]
            ind_height = 2
            support_color = COLORS["supporting_error"]
        elif state["focused"]:
            lbl_color = COLORS["label_focus"]
            ind_color = COLORS["indicator_focus"]
            ind_height = 2
            support_color = COLORS["supporting"]
        else:
            lbl_color = COLORS["label_idle"]
            ind_color = COLORS["indicator_idle"]
            ind_height = 1
            support_color = COLORS["supporting"]

        # Color de fondo (Hover vs Idle)
        bg_current = COLORS["bg_hover"] if state["hover"] else COLORS["bg_idle"]
        
        # Aplicar colores
        container.configure(bg=bg_current)
        entry.configure(bg=bg_current, fg=COLORS["text"], insertbackground=COLORS["caret"])
        lbl_widget.configure(bg=bg_current, fg=lbl_color)
        indicator.configure(bg=ind_color, height=ind_height)
        lbl_support.configure(fg=support_color, bg=bg_parent)

        # B. Animación del Label
        if is_active and not force_idle:
            # Flotante (Arriba)
            lbl_widget.place(x=padding_left, y=8, anchor="nw")
            lbl_widget.configure(font=get_font("input")) # Texto pequeño
            lbl_widget.lift()
        else:
            # Reposo (Centro)
            lbl_widget.place(x=padding_left, y=28, anchor="w")
            lbl_widget.configure(font=get_font("body")) # Texto normal

        # C. Supporting Text Visibility
        if state["error"] or (supporting_text and supporting_text.strip()):
            lbl_support.pack(fill="x", padx=16, pady=(4,0))
        else:
            lbl_support.pack_forget()

    # --- 5. EVENTOS ---
    def on_focus_in(e):
        state["focused"] = True
        update_visuals()

    def on_focus_out(e):
        state["focused"] = False
        if validator:
            val = entry.get()
            is_valid, err_msg = validator(val)
            if not is_valid:
                set_error(err_msg)
            else:
                clear_error()
        update_visuals()

    def on_hover(e, is_hovering):
        state["hover"] = is_hovering
        if not state["focused"]: 
            update_visuals()

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    container.bind("<Enter>", lambda e: on_hover(e, True))
    container.bind("<Leave>", lambda e: on_hover(e, False))
    lbl_widget.bind("<Button-1>", lambda e: entry.focus_set())

    # --- API ---
    def get_value(): return entry.get()
    
    def set_value(text):
        entry.delete(0, tk.END)
        entry.insert(0, text)
        update_visuals() 
    
    def set_error(message):
        state["error"] = True
        lbl_support.configure(text=message)
        update_visuals()

    def clear_error():
        state["error"] = False
        lbl_support.configure(text=supporting_text if supporting_text else "")
        update_visuals()

    wrapper.get_value = get_value
    wrapper.set_value = set_value
    wrapper.set_error = set_error
    wrapper.clear_error = clear_error

    # Estado inicial
    update_visuals()
    
    return wrapper