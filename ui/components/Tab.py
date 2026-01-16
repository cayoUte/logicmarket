from tkinter import ttk
import tkinter as tk
from ui.utils import props_to_obj


def Tab(parent, tab_config, hooks, **initial_props):
    props = props_to_obj(initial_props)
    notebook = ttk.Notebook(parent)
    notebook.pack(expand=True, fill='both', padx=5, pady=5)
    
    for title, render_fn in tab_config.items():
        frame = tk.Frame(notebook, bg=props.bg_app)
        notebook.add(frame, text=title)
        
        render_fn(frame, hooks, **initial_props)
        hooks['subscribe'](frame, lambda w, p: w.configure(bg=p['bg_app']))
    
    return notebook