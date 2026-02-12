def select_inventory_state(state):
    return state["inventory"]


def select_paginated_results(state):
    inventory_slice = select_inventory_state(state)

    all_results = inventory_slice.get("resultados_api", [])
    page = inventory_slice.get("ui_page", 1)
    size = inventory_slice.get("ui_page_size", 10)

    start_index = (page - 1) * size
    end_index = start_index + size
    visible_items = all_results[start_index:end_index]

    total_items = len(all_results)
    total_pages = (total_items + size - 1) // size

    return {
        "rows": visible_items,
        "current_page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


from gui.theme.app_pallete import APP_PALETTE


def select_theme_mode(state):
    return state["theme"]["mode"]


def select_current_colors(state):
    mode = state["theme"]["mode"]

    if mode == "dark":
        dark_palette = APP_PALETTE.get("dark", APP_PALETTE["primary"])

        return {
            "background": dark_palette["Basic"],
            "surface": dark_palette[800],
            "text": "#E6E1E5",
            "input_bg": dark_palette[700],
        }
    else:
        return {
            "background": "#f5f9f4",
            "surface": "#ffffff",
            "text": "#1A1C1E",
            "input_bg": "#EEF2F6",
        }
