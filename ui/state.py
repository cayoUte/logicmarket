from ui import styles


def gen_theme_manager(root_window):
    subscribers = []
    
    def subscribe(widget, update_fn):
        subscribers.append((widget, update_fn))
    
    def set_theme(mode):
        new_props=styles.get_theme(mode)
        root_window.configure(bg=new_props['bg_app'])
        
        for widget, update_fn in subscribers:
            update_fn(widget, new_props)
        return new_props            
    return subscribe, set_theme