import tkinter as tk
from ui import styles
from ui.utils import props_to_obj


def Text_Input(parent, label_text, hooks, **initial_props):
    defaults = styles.get_theme('light')
    props = props_to_obj(initial_props, defaults)
    
    frame = tk.Frame(parent, bg=props.bg_app)
    frame.pack(fill="x", pady=5)
    
    lbl = tk.Label(
        frame,
        text=label_text,
        font=(props.family, props.size_sm, props.weight_normal),
        bg=props.bg_app,
        fg=props.text_main
    )
    lbl.pack(anchor="w")
    entry = tk.Entry(
        frame,
        bg=props.bg_component,
        fg=props.text_main,
        relief="flat",
        font=(props.family, props.size_md)
    )
    entry.pack(fill='x', ipady=3)
    
    def update(widget_frame, new_theme_dict):
        p = props_to_obj(new_theme_dict)
        widget_frame.configure(bg=p.bg_app)
        lbl.configure(bg=p.bg_app, fg=p.text_main)
        entry.configure(bg=p.bg_component, fg=p.text_main, insertbackground=p.text_main)
    hooks['subscribe'](frame, update)
    return frame, entry
    