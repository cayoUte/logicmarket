import tkinter as tk


# Import Raw Components
from components.buttons.IconButton import IconButton
from reactive import connect_theme
from state_manager import create_store
import styles

root = tk.Tk()
root.geometry("800x600")

# 1. Initialize Store
initial_theme = styles.get_theme("light")
get_state, dispatch, _ = create_store(initial_theme)

# 2. Create the HOF (Decorator) tied to this store
# This creates a specific "connector" for our app's theme
with_theme = connect_theme((get_state, dispatch, _))

# 3. Create "Connected" Versions of your components
# This creates a new function that auto-subscribes whatever it creates
ReactiveIconButton = with_theme(IconButton)

# --- UI COMPOSITION ---
root.configure(bg=initial_theme["bg_app"])

# Toolbar
toolbar = tk.Frame(root, bg=initial_theme["bg_app"])
toolbar.pack(pady=50)

# Render Connected Components
# Notice we don't pass 'hooks' anymore. The HOF handles it.
btn1 = ReactiveIconButton(
    toolbar, icon_path="filter_alt.svg", on_click=lambda: print("Filter"), size=32
)
btn1.pack(side="left", padx=10)

btn2 = ReactiveIconButton(
    toolbar, icon_path="sync.svg", on_click=lambda: print("Sync"), size=32
)
btn2.pack(side="left", padx=10)


# --- THEME TOGGLE LOGIC ---
def toggle_theme():
    current_mode = "dark" if get_state()["bg_app"] == "#f0f2f5" else "light"
    new_theme = styles.get_theme(current_mode)

    # Dispatch updates ALL connected components automatically
    # Safe from crashes thanks to WeakKeyDictionary in store
    dispatch(new_theme)

    root.configure(bg=new_theme["bg_app"])
    toolbar.configure(bg=new_theme["bg_app"])


tk.Button(root, text="Toggle Theme", command=toggle_theme).pack(pady=20)

root.mainloop()
