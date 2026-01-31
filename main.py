import tkinter as tk
from gui.components.layouts.PersistentDrawer import PersistentDrawer
from gui.pages.CRUD import ImporterPage
from gui.pages.HomePage import HomePage
from persistance.inventory import load_inventory_from_file, save_inventory_to_file
from routes.routes import routes, menu_items
from gui.theme.fonts import load_custom_fonts
from store.reducer.inventory_reducer import inventory_reducer
from store.store import create_store



def main():
    root = tk.Tk()
    root.geometry("1024x768")

    bg_app = "#f5f9f4"
    root.configure(bg=bg_app)

    content_area = tk.Frame(root, bg=bg_app)
    content_area.pack(side="right", fill="both", expand=True)
    load_custom_fonts()
    
    
    # 1. Estado Inicial
    initial_state = {
        "inventario": load_inventory_from_file(),
        "resultados_api": [],
        "loading": False
    }
    
    # 2. CREACIÓN DEL STORE (Estilo Funcional)
    # Desempaquetamos las funciones que devuelve el closure
    dispatch, subscribe, get_state = create_store(
        inventory_reducer, 
        initial_state
    )
    
    # 3. Persistencia (Side Effect controlado)
    def auto_save(state):
        save_inventory_to_file(state["inventario"])
        
    subscribe(auto_save)

    # 4. Inyección de dependencias
    # Pasamos una tupla o un diccionario con las funciones que la página necesita
    store_funcs = {
        "dispatch": dispatch, 
        "subscribe": subscribe, 
        "get_state": get_state
    }
    
    

    def load_page(page_id):

        for widget in content_area.winfo_children():
            widget.destroy()

        page_constructor = routes.get(page_id)

        if page_constructor:
            print(f"Routing to: {page_id}")
            if page_id == "importer":
                new_page = ImporterPage(content_area, store_funcs)
            elif page_id == "home":
                new_page = HomePage(content_area, on_navigate=load_page)
            else:
                new_page = page_constructor(content_area)
            new_page.pack(fill="both", expand=True)
        else:
            print(f"Error: 404 Page not found for id '{page_id}'")

    sidebar = PersistentDrawer(
        root,
        nav_items=menu_items,
        on_navigate=load_page,
        width=80,
        variant="primary",
    )
    sidebar.pack(side="left", fill="y")

    sidebar.select_item("home")

    root.mainloop()


if __name__ == "__main__":
    main()
