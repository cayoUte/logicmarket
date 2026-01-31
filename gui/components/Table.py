import tkinter as tk
from tkinter import ttk
from gui.theme.app_pallete import get_app_color

def Table(parent, columns, data, variant="primary", height=10):
    """
    A themed Treeview table func component.
    
    Args:
        columns: List of dicts [{"id": "name", "text": "Name", "width": 150}, ...]
        data: List of tuples/lists matching the column order.
        variant: Palette key used for the SELECTION highlight color.
    """

    # --- 1. RESOLUCIÓN DE COLORES ---
    def resolve(cat, shade):
        return get_app_color(cat, shade)

    bg_body = resolve("neutral", 0)       # Blanco / Fondo
    bg_header = resolve("neutral", 50)    # Gris muy claro
    text_main = resolve("neutral", 900)   # Casi negro
    text_header = resolve("neutral", 800) # Gris oscuro

    highlight_bg = resolve(variant, "Basic") # Color primario (ej. Azul)
    highlight_fg = resolve("neutral", 0)     # Texto blanco al seleccionar

    # --- 2. CONFIGURACIÓN DE ESTILOS (Theming) ---
    style = ttk.Style()
    
    # Aseguramos un tema base que soporte personalización (clam es el mejor para esto)
    if style.theme_use() != "clam":
        style.theme_use("clam")

    # Creamos un nombre único para este estilo basado en la variante
    style_name = f"{variant}.Treeview"

    # Estilo del cuerpo de la tabla
    style.configure(
        style_name,
        background=bg_body,
        foreground=text_main,
        fieldbackground=bg_body,
        rowheight=30,
        borderwidth=0,
        font=("Segoe UI", 10),
    )

    # Estilo de la cabecera
    style.configure(
        f"{style_name}.Heading",
        background=bg_header,
        foreground=text_header,
        relief="flat",
        font=("Segoe UI", 10, "bold"),
    )

    # Mapa de colores para estados (seleccionado, etc.)
    style.map(
        style_name,
        background=[("selected", highlight_bg)],
        foreground=[("selected", highlight_fg)],
    )

    # --- 3. CONSTRUCCIÓN DE WIDGETS ---
    container = tk.Frame(parent, bg=bg_body)
    
    # NOTA: Comentamos esto para que la tabla se expanda y llene el ImporterPage
    # container.pack_propagate(False) 

    scrollbar = ttk.Scrollbar(container, orient="vertical")

    tree = ttk.Treeview(
        container,
        columns=[c["id"] for c in columns],
        show="headings",
        style=style_name,
        height=height,
        yscrollcommand=scrollbar.set,
        selectmode="browse" # Selección simple
    )

    scrollbar.config(command=tree.yview)

    # Configurar columnas
    for col in columns:
        col_id = col["id"]
        col_text = col["text"]
        col_width = col.get("width", 100)
        col_anchor = col.get("anchor", "w") # Alineación (w=izq, center=centro, e=der)

        tree.heading(col_id, text=col_text)
        tree.column(col_id, width=col_width, anchor=col_anchor)

    # --- 4. LÓGICA DE ACTUALIZACIÓN (CLOSURES) ---
    
    def set_data(new_rows):
        """Borra todo y repuebla la tabla."""
        # Limpiar
        for item in tree.get_children():
            tree.delete(item)

        # Insertar nuevos
        # Nota: 'values' espera una tupla o lista: (col1, col2, col3)
        for row in new_rows:
            tree.insert("", "end", values=row)

    def get_selected_item():
        """Retorna los valores de la fila seleccionada o None."""
        selected_id = tree.selection()
        if selected_id:
            return tree.item(selected_id[0])["values"]
        return None

    # Llenado inicial
    set_data(data)

    # Layout
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # --- 5. EXPOSICIÓN DE MÉTODOS (Monkey Patching) ---
    # Adjuntamos las funciones al objeto Frame para poder llamarlas desde fuera
    container.set_data = set_data         # <--- ESTO ES LO QUE BUSCA TU UI
    container.update_rows = set_data      # Alias por compatibilidad
    container.get_selected = get_selected_item
    container.tree = tree                 # Acceso directo al treeview por si acaso

    return container