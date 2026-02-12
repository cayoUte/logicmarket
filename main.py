import tkinter as tk

from gui.components.layouts.PersistentDrawer import PersistentDrawer
from gui.pages.InventoryPage import InventoryPage
from gui.pages.ImporterPage import ImporterPage
from gui.pages.HomePage import HomePage
from gui.components.AppBar import AppBar
from gui.theme.fonts import load_custom_fonts

from routes.routes import routes, menu_items
from persistance.inventory import load_inventory_from_file, save_inventory_to_file
from store.store import create_store
from store.utils.combine_reducers import combine_reducers
from store.slices.inventory_slice import inventory_reducer, actions as inventory_actions
from store.slices.theme_slice import theme_reducer
from store.selectors import select_current_colors, select_theme_mode


def main():
    root = tk.Tk()
    root.geometry("1300x800")
    root.title("LogicMarket - Gestión de Inventario")
    load_custom_fonts()

    root_reducer = combine_reducers(
        {"inventory": inventory_reducer, "theme": theme_reducer}
    )

    initial_global_state = {
        "inventory": inventory_reducer(None, None),
        "theme": theme_reducer(None, None),
    }

    dispatch, subscribe, get_state = create_store(root_reducer, initial_global_state)

    def auto_save(state):
        if state and "inventory" in state:
            save_inventory_to_file(state["inventory"]["inventario"])

    subscribe(auto_save)

    datos_disco = load_inventory_from_file()
    dispatch(inventory_actions["setInventory"](datos_disco))

    store_funcs = {"dispatch": dispatch, "subscribe": subscribe, "get_state": get_state}

    sidebar_ref = None
    app_bar_updater = None
    app_bar_theme_updater = None
    current_page_id = "home"

    right_panel = tk.Frame(root)
    right_panel.pack(side="right", fill="both", expand=True)

    user_data = {"avatar_path": "gui/assets/images/avatar.png"}
    app_bar_data = AppBar(right_panel, store_funcs, user_data)
    app_bar_widget = app_bar_data["widget"]
    app_bar_updater = app_bar_data["update_route"]
    app_bar_theme_updater = app_bar_data["update_theme"]

    app_bar_widget.pack(side="top", fill="x")

    content_area = tk.Frame(right_panel)
    content_area.pack(side="bottom", fill="both", expand=True)

    PAGE_TITLES = {
        "home": "Dashboard General",
        "importer": "Importador de Excel",
        "inventory": "Gestión de Inventario",
        "settings": "Configuración",
    }

    def load_page(page_id):
        nonlocal current_page_id
        current_page_id = page_id

        for widget in content_area.winfo_children():
            widget.destroy()

        if app_bar_updater:
            page_title = PAGE_TITLES.get(page_id, "LogicMarket")
            app_bar_updater(page_id, title=page_title)

        page_constructor = routes.get(page_id)
        if page_constructor:
            if page_id == "inventory":
                new_page = InventoryPage(content_area, store_funcs)
            elif page_id == "importer":
                new_page = ImporterPage(content_area, store_funcs)
            elif page_id == "home":
                new_page = HomePage(content_area, on_navigate=load_page)
            else:
                new_page = page_constructor(content_area)

            new_page.pack(fill="both", expand=True)

    def render_sidebar():
        nonlocal sidebar_ref

        state = get_state()
        current_mode = select_theme_mode(state)

        if sidebar_ref:
            sidebar_ref.destroy()

        sidebar_ref = PersistentDrawer(
            root,
            nav_items=menu_items,
            on_navigate=load_page,
            width=80,
            variant="secondary",
            ui_mode=current_mode,
        )
        sidebar_ref.pack(side="left", fill="y", before=right_panel)

        sidebar_ref.select_item(current_page_id)

    last_mode = None

    def on_state_change(state):
        nonlocal last_mode
        current_mode = select_theme_mode(state)
        colors = select_current_colors(state)

        if current_mode != last_mode:
            last_mode = current_mode
            print(f"🎨 Tema cambiado a: {current_mode} - Recargando UI...")

            bg_color = colors["background"]

            root.configure(bg=bg_color)
            right_panel.configure(bg=bg_color)
            content_area.configure(bg=bg_color)

            if app_bar_theme_updater:
                app_bar_theme_updater()

            render_sidebar()

            load_page(current_page_id)

    subscribe(on_state_change)

    on_state_change(get_state())

    root.mainloop()


if __name__ == "__main__":
    main()
