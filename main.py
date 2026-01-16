import tkinter as tk
from ui.components.Tab import Tab
from ui.components.buttons.Button import Button
from ui.components.inputs.Text_Input import Text_Input
from ui.layout.layouts import TabMonitor
from ui.state import gen_theme_manager
import ui.styles as styles

root = tk.Tk()
root.geometry("400x300")
root.title("LogicMarket")

subscribe, set_theme = gen_theme_manager(root)
hooks = {"subscribe": subscribe}

initial_styles = styles.get_theme("light")
root.configure(bg=initial_styles["bg_app"])

# ==========================================
#       UI
# ========================================

tab_config = {"Monitor de Inventario": TabMonitor}
Tab(root, tab_config, hooks, **initial_styles)
lbl_title = tk.Label(
    root,
    text=f"Logig Market",
    bg=initial_styles["bg_app"],
    fg=initial_styles["text_main"],
    font=(
        initial_styles["family"],
        initial_styles["size_lg"],
        initial_styles["weight_bold"],
    ),
)

lbl_title.pack(pady=15)

subscribe(
    lbl_title, lambda w, props: w.configure(bg=props["bg_app"], fg=props["text_main"])
)

Text_Input(root, "Tu Nombre", hooks, **initial_styles)

Text_Input(root, "Tu Correo", hooks, **initial_styles)

local_state = ["light"]


def toggle_theme():
    new_mode = "dark" if local_state[0] == "light" else "light"
    local_state[0] = new_mode
    set_theme(new_mode)


theme_btn = Button(
    root,
    f"Cambiar Tema a {'dark' if local_state[0] == 'light' else 'light'}",
    toggle_theme,
    hooks,
    type="primary",
    **initial_styles,
)
theme_btn.pack(pady=5)
root.mainloop()
