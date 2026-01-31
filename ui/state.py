from ui import styles

def gen_theme_manager(root_window):
    # Lista de tuplas: (widget_instance, update_function)
    subscribers = []
    
    def subscribe(widget, update_fn):
        subscribers.append((widget, update_fn))

    def set_theme(mode):
        new_props = styles.get_theme(mode)
        
        # 1. Actualizar ventana raíz
        root_window.configure(bg=new_props["bg_app"])
        
        # 2. Filtrar widgets muertos y actualizar los vivos
        # Creamos una nueva lista solo con los que siguen existiendo
        alive_subscribers = []
        
        for widget, update_fn in subscribers:
            try:
                # winfo_exists() devuelve 1 si el widget existe en Tcl, 0 si fue destruido
                if widget.winfo_exists():
                    update_fn(widget, new_props)
                    alive_subscribers.append((widget, update_fn))
            except Exception:
                # Si falla la verificación, asumimos que está muerto
                pass
                
        # Reemplazamos la lista global con la lista limpia
        # Esto previene que la lista crezca infinitamente (Memory Leak)
        subscribers[:] = alive_subscribers
            
        return new_props

    return subscribe, set_theme