# gui/components/modals/ImportModal.py
import tkinter as tk
from gui.components.TextField import TextField
from gui.components.buttons.Button import Pillow_Button
from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font
from gui.theme.dialogs import get_dialog_theme, DIALOG_SPECS


def ImportModal(parent, product_data, on_confirm, ui_mode="light"):
    """
    MODAL DE IMPORTACIÓN:
    Muestra datos traídos de la API (Solo Lectura) y pide datos de inventario.
    """
    THEME = get_dialog_theme(ui_mode)
    bg_color = get_app_color(*THEME["bg"])
    card_bg = get_app_color(*THEME["card_bg"])
    title_color = get_app_color(*THEME["title"])
    body_color = get_app_color(*THEME["body"])

    modal = tk.Toplevel(parent)
    modal.title("Importar Producto")
    modal.configure(bg=bg_color)
    modal.transient(parent)
    modal.grab_set()

    main = tk.Frame(
        modal,
        bg=bg_color,
        padx=DIALOG_SPECS["padding_outer"],
        pady=DIALOG_SPECS["padding_outer"],
    )
    main.pack(fill="both", expand=True)

    tk.Label(
        main,
        text="Importar al Inventario",
        font=get_font("h4"),
        fg=title_color,
        bg=bg_color,
        anchor="w",
    ).pack(fill="x", pady=(0, 16))

    card = tk.Frame(main, bg=card_bg, padx=16, pady=16)
    card.pack(fill="x", pady=(0, 24))

    tk.Label(
        card,
        text=product_data.get("name", "Sin Nombre"),
        font=("Segoe UI", 11, "bold"),
        fg=title_color,
        bg=card_bg,
        wraplength=320,
        anchor="w",
        justify="left",
    ).pack(fill="x")

    meta = f"{product_data.get('brand', 'N/A')} • {product_data.get('code', 'N/A')}"
    tk.Label(
        card, text=meta, font=("Segoe UI", 9), fg=body_color, bg=card_bg, anchor="w"
    ).pack(fill="x", pady=(4, 0))

    inp_price = TextField(
        main, label="Precio Venta ($) *", width=350, ui_mode=ui_mode, bg_parent=bg_color
    )
    inp_price.pack(fill="x", pady=(0, 12))

    inp_stock = TextField(
        main, label="Stock Inicial *", width=350, ui_mode=ui_mode, bg_parent=bg_color
    )
    inp_stock.pack(fill="x", pady=(0, 12))

    inp_sup = TextField(
        main, label="Proveedor *", width=350, ui_mode=ui_mode, bg_parent=bg_color
    )
    inp_sup.pack(fill="x", pady=(0, 16))

    def handle_save():
        try:
            p = float(inp_price.get_value())
            s = int(inp_stock.get_value())
            sup = inp_sup.get_value().strip()
            if p <= 0 or s < 0 or not sup:
                raise ValueError

            final_item = {**product_data, "price": p, "stock": s, "supplier": sup}
            on_confirm(final_item)
            modal.destroy()
        except:
            inp_price.set_error("Verifica los datos (obligatorios)")

    actions = tk.Frame(main, bg=bg_color)
    actions.pack(fill="x", pady=(16, 0))
    Pillow_Button(
        actions,
        text="IMPORTAR",
        on_click=handle_save,
        variant="primary",
        bg_parent=bg_color,
        ui_mode=ui_mode,
        dimensions=(110, 40, 20),
    ).pack(side="right")
    tk.Frame(actions, width=8, bg=bg_color).pack(side="right")
    Pillow_Button(
        actions,
        text="Cancelar",
        on_click=modal.destroy,
        variant="surface",
        bg_parent=bg_color,
        ui_mode=ui_mode,
        dimensions=(100, 40, 20),
    ).pack(side="right")

    _center_modal(modal, parent)
    return modal


def _center_modal(modal, parent):
    modal.withdraw()
    modal.update_idletasks()
    w, h = max(modal.winfo_reqwidth(), 400), modal.winfo_reqheight()
    x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (w // 2)
    y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (h // 2)
    modal.geometry(f"+{x}+{y}")
    modal.minsize(w, h)
    modal.deiconify()
