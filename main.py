import tkinter as tk
from ui.components.Drawer import DrawerLayout
from ui.components.Tab import Tab
from ui.components.buttons.Button import Button
from ui.components.inputs.Text_Input import Text_Input
from ui.layout.layouts import TabMonitor
from ui.state import gen_theme_manager
import ui.styles as styles

root = tk.Tk()
root.geometry("1100x700") # Un poco más ancho para acomodar el drawer
root.title("LogicMarket Enterprise")

subscribe, set_theme = gen_theme_manager(root)
hooks = {"subscribe": subscribe}

initial_styles = styles.get_theme("light")
root.configure(bg=initial_styles["bg_app"])


rutas_app = {
        "📊  Monitor": TabMonitor,     
    }
# Renderizar Layout Principal
DrawerLayout(root, rutas_app, hooks, **initial_styles)
# ==========================================
#       UI
# ========================================

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
