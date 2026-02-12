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

    def resolve(cat, shade):
        return get_app_color(cat, shade)

    bg_body = resolve("neutral", 0)
    bg_header = resolve("neutral", 50)
    text_main = resolve("neutral", 900)
    text_header = resolve("neutral", 800)

    highlight_bg = resolve(variant, "Basic")
    highlight_fg = resolve("neutral", 0)

    style = ttk.Style()

    if style.theme_use() != "clam":
        style.theme_use("clam")

    style_name = f"{variant}.Treeview"

    style.configure(
        style_name,
        background=bg_body,
        foreground=text_main,
        fieldbackground=bg_body,
        rowheight=30,
        borderwidth=0,
        font=("Segoe UI", 10),
    )

    style.configure(
        f"{style_name}.Heading",
        background=bg_header,
        foreground=text_header,
        relief="flat",
        font=("Segoe UI", 10, "bold"),
    )

    style.map(
        style_name,
        background=[("selected", highlight_bg)],
        foreground=[("selected", highlight_fg)],
    )

    container = tk.Frame(parent, bg=bg_body)

    scrollbar = ttk.Scrollbar(container, orient="vertical")

    tree = ttk.Treeview(
        container,
        columns=[c["id"] for c in columns],
        show="headings",
        style=style_name,
        height=height,
        yscrollcommand=scrollbar.set,
        selectmode="browse",
    )

    scrollbar.config(command=tree.yview)

    for col in columns:
        col_id = col["id"]
        col_text = col["text"]
        col_width = col.get("width", 100)
        col_anchor = col.get("anchor", "w")

        tree.heading(col_id, text=col_text)
        tree.column(col_id, width=col_width, anchor=col_anchor)

    def set_data(new_rows):
        for item in tree.get_children():
            tree.delete(item)

        for row in new_rows:
            tree.insert("", "end", values=row)

    def get_selected_item():
        selected_id = tree.selection()
        if selected_id:
            return tree.item(selected_id[0])["values"]
        return None

    set_data(data)

    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    container.set_data = set_data
    container.update_rows = set_data
    container.get_selected = get_selected_item
    container.tree = tree

    return container
