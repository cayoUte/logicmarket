import tkinter as tk
from gui.components.buttons.Button import Pillow_Button
from gui.theme.app_pallete import get_app_color
from gui.theme.dialogs import get_dialog_theme


def ConfirmDialog(
    parent, title, message, on_confirm=None, ui_mode="light", is_error=False
):
    theme = get_dialog_theme(ui_mode)
    bg_color = get_app_color(*theme["bg"])
    text_color = get_app_color(*theme["title"])

    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.configure(bg=bg_color)
    dialog.transient(parent)
    dialog.grab_set()

    container = tk.Frame(dialog, bg=bg_color, padx=24, pady=24)
    container.pack()

    icon_char = "⚠️" if is_error else "❓"
    tk.Label(
        container,
        text=icon_char,
        font=("Segoe UI Emoji", 24),
        bg=bg_color,
        fg=text_color,
    ).pack(pady=(0, 10))

    tk.Label(
        container, text=title, font=("Segoe UI", 14, "bold"), bg=bg_color, fg=text_color
    ).pack(fill="x")
    tk.Label(
        container,
        text=message,
        font=("Segoe UI", 10),
        bg=bg_color,
        fg=get_app_color(*theme["body"]),
        wraplength=300,
    ).pack(pady=(10, 20))

    btns = tk.Frame(container, bg=bg_color)
    btns.pack(fill="x")

    if not is_error:
        Pillow_Button(
            btns,
            text="Confirmar",
            variant="primary",
            ui_mode=ui_mode,
            bg_parent=bg_color,
            dimensions=(100, 36, 18),
            on_click=lambda: [on_confirm(), dialog.destroy()],
        ).pack(side="right")

        tk.Frame(btns, width=10, bg=bg_color).pack(side="right")

        Pillow_Button(
            btns,
            text="Cancelar",
            variant="surface",
            ui_mode=ui_mode,
            bg_parent=bg_color,
            dimensions=(90, 36, 18),
            on_click=dialog.destroy,
        ).pack(side="right")
    else:
        Pillow_Button(
            btns,
            text="Entendido",
            variant="surface",
            ui_mode=ui_mode,
            bg_parent=bg_color,
            dimensions=(100, 36, 18),
            on_click=dialog.destroy,
        ).pack(side="right")

    dialog.update_idletasks()
    w, h = dialog.winfo_reqwidth(), dialog.winfo_reqheight()
    x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (w // 2)
    y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (h // 2)
    dialog.geometry(f"+{x}+{y}")
