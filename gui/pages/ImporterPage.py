import tkinter as tk
from gui.components.ImportResultsList import ImportResultsList
from gui.components.TextField import TextField
from gui.components.buttons.Button import Pillow_Button

from gui.components.modals.ImportModal import ImportModal

from gui.theme.fonts import get_font
from store.slices.inventory_slice import actions
from store.selectors import (
    select_current_colors,
    select_paginated_results,
    select_theme_mode,
)
from service.inventory_service import search_products_action


def ImporterPage(parent, store_funcs):
    dispatch = store_funcs["dispatch"]
    subscribe = store_funcs["subscribe"]
    get_state = store_funcs["get_state"]

    state = get_state()
    current_mode = select_theme_mode(state)
    colors = select_current_colors(state)

    bg_color = colors["background"]
    surface_color = colors["surface"]
    text_color = colors["text"]

    frame = tk.Frame(parent, bg=bg_color)

    header_frame = tk.Frame(frame, bg=bg_color)
    header_frame.pack(fill="x", padx=24, pady=(24, 0))

    lbl_title = tk.Label(
        header_frame,
        text="Importador de Productos",
        bg=bg_color,
        fg=text_color,
        font=get_font("h5"),
    )
    lbl_title.pack(side="left")

    filter_frame = tk.Frame(frame, bg=surface_color)
    filter_frame.pack(fill="x", padx=24, pady=16)

    inner_filter = tk.Frame(filter_frame, bg=surface_color, padx=20, pady=20)
    inner_filter.pack(fill="x")

    inp_cat = TextField(
        inner_filter,
        label="Categoría",
        placeholder="Ej: Snacks",
        width=220,
        ui_mode=current_mode,
        bg_parent=surface_color,
    )
    inp_cat.grid(row=0, column=0, padx=(0, 16))

    inp_country = TextField(
        inner_filter,
        label="País",
        placeholder="Ej: Ecuador",
        width=220,
        ui_mode=current_mode,
        bg_parent=surface_color,
    )
    inp_country.grid(row=0, column=1, padx=(0, 16))

    def do_search():
        filters = {
            "categories": inp_cat.get_value(),
            "countries": inp_country.get_value(),
        }
        if any(filters.values()):
            dispatch(search_products_action(filters), ui_ref=frame)

    btn_container = tk.Frame(inner_filter, bg=surface_color, pady=2)
    btn_container.grid(row=0, column=2, sticky="s")

    btn_search = Pillow_Button(
        btn_container,
        text="BUSCAR",
        on_click=do_search,
        variant="primary",
        bg_parent=surface_color,
        ui_mode=current_mode,
        dimensions=(120, 44, 22),
    )
    btn_search.pack()

    def on_modal_confirm(final_item_data):
        print(f"📦 Importando: {final_item_data['name']}")
        dispatch(actions["importBatch"]([final_item_data]))

    def open_import_modal(product_data_from_api):
        ImportModal(
            parent=frame,
            product_data=product_data_from_api,
            on_confirm=on_modal_confirm,
            ui_mode=current_mode,
        )

    list_container = tk.Frame(frame, bg=bg_color)
    list_container.pack(fill="both", expand=True, padx=24)

    results_list = ImportResultsList(
        parent=list_container,
        on_import_click=open_import_modal,
        height=450,
        colors=colors,
    )
    results_list.pack(fill="both", expand=True)

    pagination_frame = tk.Frame(frame, bg=bg_color)
    pagination_frame.pack(fill="x", padx=24, pady=16)

    lbl_page_info = tk.Label(
        pagination_frame, text="...", bg=bg_color, fg=text_color, font=("Segoe UI", 10)
    )
    lbl_page_info.pack(side="left")

    buttons_frame = tk.Frame(pagination_frame, bg=bg_color)
    buttons_frame.pack(side="right")

    btn_prev = Pillow_Button(
        buttons_frame,
        text="<",
        variant="surface",
        bg_parent=bg_color,
        dimensions=(40, 32, 8),
        on_click=lambda: dispatch(actions["changePage"](-1)),
        ui_mode=current_mode,
    )
    btn_prev.pack(side="left", padx=8)

    btn_next = Pillow_Button(
        buttons_frame,
        text=">",
        variant="surface",
        bg_parent=bg_color,
        dimensions=(40, 32, 8),
        on_click=lambda: dispatch(actions["changePage"](1)),
        ui_mode=current_mode,
    )
    btn_next.pack(side="left")

    def update_ui(state):
        if not frame.winfo_exists():
            return

        view_data = select_paginated_results(state)

        if hasattr(results_list, "set_data"):
            results_list.set_data(view_data["rows"])

        info_text = f"Página {view_data['current_page']} de {view_data['total_pages']} ({view_data['total_items']} items)"
        lbl_page_info.config(text=info_text)

    unsubscribe = subscribe(update_ui)
    update_ui(get_state())

    frame.bind("<Destroy>", lambda e: unsubscribe() if e.widget == frame else None)

    return frame
