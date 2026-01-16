import tkinter as tk
from ui.utils import props_to_obj


def Console(parent, hooks, **initial_props):
    props = props_to_obj
    
    lbl = tk.Label(
        parent,
        text="Esperando Acción...",
        bg=props.bg_component,
        fg=props.text_main,
        font=(props.family, props.size_sm, props.weight_bold),
        padx=10, pady=10,
        relief='flat'
    )
    lbl.pack(fill='x', pady=10)
    
    def set_state(type, message):
        #idealmente se leeria de un estado global TODO
        
        color_map = {
            "success": getattr(props, "success", '#4CAF50'),
            "error": getattr(props, "error", '#f4368b'),
            "neutral": getattr(props, "bg_component", '#ffffff'),
        }
        bg_final = color_map.get(type, props.bg_component)
        fg_final = '#ffffff' if type in ["success", "error"] else props.text_main
        lbl.configure(
            text=message,
            bg=bg_final,
            fg=fg_final
        )
    hooks['logic_console'] = set_state
    
    return lbl