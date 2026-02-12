# gui/components/modals/UpdateModal.py
import tkinter as tk
from gui.components.TextField import TextField
from gui.components.buttons.Button import Pillow_Button
from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font
from gui.theme.dialogs import get_dialog_theme, DIALOG_SPECS


def UpdateModal(parent, current_data, on_confirm, ui_mode="light"):
    THEME = get_dialog_theme(ui_mode)
    bg_color = get_app_color(*THEME["bg"])
    title_color = get_app_color(*THEME["title"])

    modal = tk.Toplevel(parent)
    modal.title("Actualizar Producto")
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
        text="Editar Producto",
        font=get_font("h4"),
        fg=title_color,
        bg=bg_color,
        anchor="w",
    ).pack(fill="x", pady=(0, 16))

    v_name = str(current_data.get("name", ""))
    v_brand = str(current_data.get("brand", ""))
    v_cat = str(current_data.get("category", ""))
    v_price = str(current_data.get("price", ""))
    v_stock = str(current_data.get("stock", ""))
    v_sup = str(current_data.get("supplier", ""))

    inp_name = TextField(
        main,
        label="Nombre *",
        initial_value=v_name,
        width=350,
        ui_mode=ui_mode,
        bg_parent=bg_color,
    )
    inp_name.pack(fill="x", pady=(0, 12))

    row = tk.Frame(main, bg=bg_color)
    row.pack(fill="x", pady=(0, 12))
    inp_brand = TextField(
        row,
        label="Marca",
        initial_value=v_brand,
        width=170,
        ui_mode=ui_mode,
        bg_parent=bg_color,
    )
    inp_brand.pack(side="left", padx=(0, 10))
    inp_cat = TextField(
        row,
        label="Categoría",
        initial_value=v_cat,
        width=170,
        ui_mode=ui_mode,
        bg_parent=bg_color,
    )
    inp_cat.pack(side="left")

    lbl_code = tk.Label(
        main,
        text=f"Código: {current_data.get('code')}",
        bg=bg_color,
        fg=get_app_color(*THEME["body"]),
        anchor="w",
    )
    lbl_code.pack(fill="x", pady=(0, 12))

    inp_price = TextField(
        main,
        label="Precio *",
        initial_value=v_price,
        width=350,
        ui_mode=ui_mode,
        bg_parent=bg_color,
    )
    inp_price.pack(fill="x", pady=(0, 12))
    inp_stock = TextField(
        main,
        label="Stock *",
        initial_value=v_stock,
        width=350,
        ui_mode=ui_mode,
        bg_parent=bg_color,
    )
    inp_stock.pack(fill="x", pady=(0, 12))
    inp_sup = TextField(
        main,
        label="Proveedor *",
        initial_value=v_sup,
        width=350,
        ui_mode=ui_mode,
        bg_parent=bg_color,
    )
    inp_sup.pack(fill="x", pady=(0, 16))

    def handle_update():
        err = False
        name = inp_name.get_value().strip()
        if not name:
            inp_name.set_error("Requerido")
            err = True

        try:
            price = float(inp_price.get_value())
            if price <= 0:
                raise ValueError
        except:
            inp_price.set_error("Inválido")
            err = True
            price = 0

        try:
            stock = int(inp_stock.get_value())
            if stock < 0:
                raise ValueError
        except:
            inp_stock.set_error("Inválido")
            err = True
            stock = 0

        sup = inp_sup.get_value().strip()
        if not sup:
            inp_sup.set_error("Requerido")
            err = True

        if err:
            return

        updated_prod = {
            **current_data,
            "name": name,
            "brand": inp_brand.get_value().strip(),
            "category": inp_cat.get_value().strip(),
            "price": price,
            "stock": stock,
            "supplier": sup,
        }
        on_confirm(updated_prod)
        modal.destroy()

    actions = tk.Frame(main, bg=bg_color)
    actions.pack(fill="x", pady=(16, 0))
    Pillow_Button(
        actions,
        text="GUARDAR",
        on_click=handle_update,
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
