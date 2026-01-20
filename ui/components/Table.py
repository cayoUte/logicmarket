import tkinter as tk
from tkinter import ttk
from ui import utils

def Table(parent, columns, data, hooks, **initial_props):
    """
    A reactive Treeview table that respects the app's theme
    instead of the OS system theme.
    """
    props = utils.props_to_obj(initial_props, initial_props) # Ensure we have an object
    
    # --- 1. THEME ENGINE CONFIGURATION ---
    # We need a unique style name to avoid conflicts if you have multiple tables
    style_name = "Inventory.Treeview"
    
    style = ttk.Style()
    # 'clam' is the most customizable engine across OSs (Mac/Windows/Linux)
    style.theme_use("clam") 

    def apply_styles(current_props):
        """Helper to apply colors to the ttk Style"""
        p = utils.props_to_obj(current_props, current_props)
        
        # Configure the Body (Rows)
        style.configure(
            style_name,
            background=p.bg_component,      # White in light mode
            foreground=p.text_main,         # Black text
            fieldbackground=p.bg_component, # Background of empty area
            rowheight=30,
            borderwidth=0,
            font=(p.family[0], 10)
        )
        
        # Configure the Header
        style.configure(
            f"{style_name}.Heading",
            background=p.bg_app,            # Light gray header
            foreground=p.text_main,
            relief="flat",
            font=(p.family[0], 10, "bold")
        )
        
        # Configure Selection Colors (Highlight)
        style.map(
            style_name,
            background=[('selected', p.primary)], # Violet when selected
            foreground=[('selected', 'white')]    # White text when selected
        )

    # Apply initial styles
    apply_styles(initial_props)

    # --- 2. WIDGET SETUP ---
    # Container frame to hold table + scrollbar
    frame = tk.Frame(parent, bg=props.bg_app)
    frame.pack(expand=True, fill='both', padx=20, pady=10)

    # The Treeview Widget
    tree = ttk.Treeview(
        frame, 
        columns=[c["id"] for c in columns], 
        show="headings",
        style=style_name # Apply our custom style
    )
    
    # Define Columns
    for col in columns:
        tree.heading(col["id"], text=col["text"])
        
        # Calculate width dynamically or use fixed
        width = col.get("width", 100)
        tree.column(col["id"], width=width, anchor="w")

    # Insert Data
    for item in data:
        tree.insert("", "end", values=item)

    # Scrollbar (Modern Look)
    # Note: Tkinter scrollbars are hard to style heavily, 
    # but we can match the bg at least.
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Layout
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- 3. REACTIVITY ---
    def update_table_theme(widget_frame, new_props):
        # 1. Update the Frame background
        p = utils.props_to_obj(new_props, new_props)
        widget_frame.configure(bg=p.bg_app)
        
        # 2. Re-apply the global ttk styles
        # Note: This updates ALL tables sharing this style name
        apply_styles(new_props)

    hooks['subscribe'](frame, update_table_theme)

    # Hook to allow external data updates (e.g. from the Filter button)
    def update_data(new_rows):
        tree.delete(*tree.get_children())
        for row in new_rows:
            tree.insert("", "end", values=row)
            
    # Register this table's update function in hooks
    # You can call hooks['inventory_table'](new_data) later
    hooks['inventory_table'] = update_data

    return tree