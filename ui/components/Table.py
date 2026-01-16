import tkinter as tk
from tkinter import ttk
from ui.utils import props_to_obj


def Table(parent, cols, initial_data, hooks, **initial_props):
    props = props_to_obj(initial_props)

    table_frame = tk.Frame(parent, bg=props.bg_app)
    table_frame.pack(expand=True, fill="both", padx=10, pady=5)

    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    col_ids = [c["id"] for c in cols]
    tree = ttk.Treeview(
        table_frame, columns=col_ids, 
        show="headings", 
        yscrollcommand=scrollbar.set
    )
    
    for col in cols:
        tree.heading(col['id'], text=col['text'])
        tree.column(col['id'], width=col.get('width', 100))
        scrollbar.config(command=tree.yview)
        tree.pack(side="left", fill='both', expand=True)

    def populate(data):
        for item in tree.get_children():
            tree.delete(item)
        
        for row in data:
            tree.insert("", "end", values=row)
    
    populate(initial_data)
    
    def update_data(new_data):
        populate(new_data)
    
    key_id = initial_props.get("component_id", "main_table")
    hooks[key_id] = update_data
    
    return tree
        
