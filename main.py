import tkinter as tk

# --- GUI IMPORTS ---
from gui.components.layouts.PersistentDrawer import PersistentDrawer
from gui.pages.ImporterPage import ImporterPage
from gui.pages.HomePage import HomePage
from gui.components.AppBar import AppBar
from gui.theme.fonts import load_custom_fonts

# --- LOGIC & STORE IMPORTS ---
from routes.routes import routes, menu_items
from persistance.inventory import load_inventory_from_file, save_inventory_to_file
from store.store import create_store
from store.utils.combine_reducers import combine_reducers
from store.slices.inventory_slice import inventory_reducer, actions as inventory_actions
from store.slices.theme_slice import theme_reducer
from store.selectors import select_current_colors, select_theme_mode

def main():
    # 1. SETUP INICIAL
    root = tk.Tk()
    root.geometry("1300x800")
    root.title("LogicMarket - Gestión de Inventario")    
    load_custom_fonts()

    # 2. STORE REDUX
    root_reducer = combine_reducers({
        "inventory": inventory_reducer,
        "theme": theme_reducer
    })
    
    initial_global_state = {
        "inventory": inventory_reducer(None, None),
        "theme": theme_reducer(None, None)
    }

    dispatch, subscribe, get_state = create_store(root_reducer, initial_global_state)

    def auto_save(state):
        if state and "inventory" in state:
            save_inventory_to_file(state["inventory"]["inventario"])
    subscribe(auto_save)

    datos_disco = load_inventory_from_file()
    dispatch(inventory_actions["setInventory"](datos_disco))

    store_funcs = {
        "dispatch": dispatch, 
        "subscribe": subscribe, 
        "get_state": get_state
    }

    # 3. REFERENCIAS GLOBALES DE UI
    # Necesitamos guardarlas para poder destruirlas después
    sidebar_ref = None
    app_bar_updater = None 
    app_bar_theme_updater = None
    current_page_id = "home" # Página por defecto

    # --- ESTRUCTURA BASE ---
    # Panel Derecho (Contenedor del contenido y AppBar)
    # Lo creamos una vez, solo le cambiaremos el color de fondo.
    right_panel = tk.Frame(root) 
    right_panel.pack(side="right", fill="both", expand=True)

    # AppBar (Ya tiene su propia lógica interna de actualización, no hace falta destruirla)
    user_data = {"avatar_path": "gui/assets/images/avatar.png"}
    app_bar_data = AppBar(right_panel, store_funcs, user_data)
    app_bar_widget = app_bar_data["widget"]
    app_bar_updater = app_bar_data["update_route"]
    app_bar_theme_updater = app_bar_data["update_theme"]
    
    app_bar_widget.pack(side="top", fill="x")

    # Área de Contenido (Donde se montan las páginas)
    content_area = tk.Frame(right_panel)
    content_area.pack(side="bottom", fill="both", expand=True)

    # 4. GESTORES DE RENDERIZADO
    
    PAGE_TITLES = {
        "home": "Dashboard General",
        "importer": "Importador de Excel",
        "inventory": "Gestión de Inventario",
        "settings": "Configuración"
    }

    def load_page(page_id):
        nonlocal current_page_id
        current_page_id = page_id # Guardamos estado para recargar si cambia el tema
        
        # A. Limpiar contenido anterior
        for widget in content_area.winfo_children():
            widget.destroy()

        # B. Actualizar título AppBar
        if app_bar_updater:
            page_title = PAGE_TITLES.get(page_id, "LogicMarket")
            app_bar_updater(page_id, title=page_title)

        # C. Instanciar Página Nueva
        # IMPORTANTE: Al ejecutarse el constructor AHORA, leerá el color actual del store
        page_constructor = routes.get(page_id)
        if page_constructor:
            # Factory pattern según la página
            if page_id == "importer":
                new_page = ImporterPage(content_area, store_funcs)
            elif page_id == "home":
                new_page = HomePage(content_area, on_navigate=load_page)
            else:
                new_page = page_constructor(content_area)
            
            new_page.pack(fill="both", expand=True)

    def render_sidebar():
        nonlocal sidebar_ref
        
        # Obtener modo actual para pasarlo al drawer
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
            ui_mode=current_mode # <--- ¡AQUÍ ESTÁ LA MAGIA!
        )
        sidebar_ref.pack(side="left", fill="y", before=right_panel)
        
        sidebar_ref.select_item(current_page_id)

    # 5. LISTENER DE CAMBIOS DE TEMA
    last_mode = None

    def on_state_change(state):
        nonlocal last_mode
        current_mode = select_theme_mode(state)
        colors = select_current_colors(state)
        
        # Solo actuamos si el modo cambió (Light <-> Dark)
        if current_mode != last_mode:
            last_mode = current_mode
            print(f"🎨 Tema cambiado a: {current_mode} - Recargando UI...")

            bg_color = colors["background"]
            
            # A. Actualizar fondos de contenedores base
            root.configure(bg=bg_color)
            right_panel.configure(bg=bg_color)
            content_area.configure(bg=bg_color)
            
            # B. Actualizar AppBar (usando su método optimizado)
            if app_bar_theme_updater:
                app_bar_theme_updater()
            
            # C. Recrear Sidebar (Full refresh)
            render_sidebar()
            
            # D. Recargar la página actual (Full refresh)
            # Esto destruirá la página vieja (blanca) y creará la nueva (oscura)
            load_page(current_page_id)

    subscribe(on_state_change)

    # 6. INICIO
    # Forzar primer pintado con colores correctos
    on_state_change(get_state())
    
    root.mainloop()

if __name__ == "__main__":
    main()