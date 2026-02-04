import tkinter as tk
from gui.components.TextField import TextField
from gui.components.buttons.Button import Pillow_Button
from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font
from gui.theme.dialogs import get_dialog_theme, DIALOG_SPECS # <--- Usar función dinámica

def ImportModal(parent, product_data, on_confirm, ui_mode="light"):
    """
    Modal de importación estilo MD3.
    """
    
    # 1. Configuración de Tema
    THEME = get_dialog_theme(ui_mode)
    
    # Helper para resolver colores
    def resolve(val):
        return get_app_color(val[0], val[1]) if isinstance(val, (tuple, list)) else val

    bg_color = resolve(THEME["bg"])
    title_color = resolve(THEME["title"])
    body_color = resolve(THEME["body"])
    card_bg = resolve(THEME["card_bg"])

    # 2. Configuración de Ventana
    modal = tk.Toplevel(parent)
    modal.title("Importar Producto")
    modal.configure(bg=bg_color)
    modal.transient(parent)
    modal.grab_set()

    # ==========================================
    # ANATOMÍA MATERIAL DESIGN 3
    # ==========================================

    # 1. CONTENEDOR PRINCIPAL
    main_container = tk.Frame(
        modal, 
        bg=bg_color, 
        padx=DIALOG_SPECS["padding_outer"], 
        pady=DIALOG_SPECS["padding_outer"]
    )
    main_container.pack(fill="both", expand=True)

    # 2. HEADLINE (Título)
    tk.Label(
        main_container, 
        text="Importar al Inventario", 
        font=get_font("h4"), 
        fg=title_color, 
        bg=bg_color,
        anchor="w"
    ).pack(fill="x", pady=(0, DIALOG_SPECS["padding_title"]))

    # 3. CARD DE RESUMEN (Producto Detectado)
    product_card = tk.Frame(main_container, bg=card_bg, padx=16, pady=16)
    product_card.pack(fill="x", pady=(0, 24)) # Espacio visual claro antes del form

    # Nombre del producto
    tk.Label(
        product_card, 
        text=product_data.get('name', 'Sin Nombre'), 
        font=("Segoe UI", 11, "bold"), 
        fg=title_color,
        bg=card_bg,
        wraplength=320,
        anchor="w",
        justify="left"
    ).pack(fill="x")

    # Metadatos
    meta_text = f"{product_data.get('brand', 'N/A')} • {product_data.get('code', 'N/A')}"
    tk.Label(
        product_card, 
        text=meta_text, 
        font=("Segoe UI", 9), 
        fg=body_color,
        bg=card_bg,
        anchor="w"
    ).pack(fill="x", pady=(4, 0))

    # 4. FORMULARIO
    # Helper para inputs consistentes
    def create_input(label, placeholder, validator=None):
        inp = TextField(
            parent=main_container,
            label=label,
            width=350, # Ancho fijo cómodo para el modal
            initial_value="",
            supporting_text=placeholder, # Usamos supporting text como hint
            validator=validator,
            ui_mode=ui_mode,      # <--- PASAR MODO
            bg_parent=bg_color    # <--- PASAR FONDO DEL MODAL
        )
        inp.pack(fill="x", pady=(0, 16)) # Espaciado vertical MD3 estándar
        return inp

    # Validadores
    def validate_number(val):
        if not val: return True, "" # Permitir vacío inicial
        # Validación simple de float
        try:
            float(val)
            return True, ""
        except ValueError:
            return False, "Debe ser un número válido"

    # Inputs
    inp_price = create_input("Precio Venta ($)", "Precio unitario sugerido", validate_number)
    inp_stock = create_input("Stock Inicial", "Cantidad física disponible", validate_number)
    
    # Input Proveedor (Ejemplo con icono opcional)
    inp_supplier = TextField(
        main_container,
        label="Proveedor",
        width=350,
        # leading_icon="store.svg", # Si tienes el icono, descomenta
        supporting_text="Distribuidor oficial",
        ui_mode=ui_mode,
        bg_parent=bg_color
    )
    inp_supplier.pack(fill="x", pady=(0, 16))

    # Espaciador flexible
    tk.Frame(main_container, bg=bg_color).pack(fill="y", expand=True)

    # 5. ACTIONS (Botones)
    actions_frame = tk.Frame(main_container, bg=bg_color)
    actions_frame.pack(fill="x", pady=(DIALOG_SPECS["padding_actions"], 0))

    def handle_save():
        try:
            val_price = inp_price.get_value()
            val_stock = inp_stock.get_value()
            val_supplier = inp_supplier.get_value()

            final_item = {
                **product_data,
                "price": float(val_price) if val_price else 0.0,
                "stock": int(val_stock) if val_stock else 0,
                "supplier": val_supplier if val_supplier else "Genérico"
            }
            on_confirm(final_item)
            modal.destroy()
        except ValueError:
            inp_price.set_error("Verifica los datos")

    # Botones alineados a la derecha
    # Botón Confirmar
    btn_confirm = Pillow_Button(
        actions_frame, 
        text="IMPORTAR", 
        on_click=handle_save, 
        variant="primary",   # Color principal de la marca
        bg_parent=bg_color,
        ui_mode=ui_mode,
        dimensions=(110, 40, 20)
    )
    btn_confirm.pack(side="right")

    # Espaciador
    tk.Frame(actions_frame, bg=bg_color, width=DIALOG_SPECS["gap_actions"]).pack(side="right")

    # Botón Cancelar
    btn_cancel = Pillow_Button(
        actions_frame, 
        text="Cancelar", 
        on_click=modal.destroy, 
        variant="surface",    # Botón plano/texto
        bg_parent=bg_color,
        ui_mode=ui_mode,
        dimensions=(100, 40, 20)
    )
    btn_cancel.pack(side="right")

    # ==========================================
    # CÁLCULO DE POSICIÓN
    # ==========================================
    modal.withdraw()
    modal.update_idletasks()
    
    req_width = modal.winfo_reqwidth()
    req_height = modal.winfo_reqheight()
    
    final_width = max(req_width, DIALOG_SPECS["min_width"]) 

    x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (final_width // 2)
    y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (req_height // 2)

    modal.geometry(f"+{x}+{y}")
    modal.minsize(final_width, req_height)
    modal.deiconify()

    return modal