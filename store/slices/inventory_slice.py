from store.utils.utils import create_slice


def set_search_params(state, payload):
    return {**state, "search_params": payload}


def search_api_success(state, payload):
    return {**state, "resultados_api": payload, "loading": False, "ui_page": 1}


def create_product(state, payload):
    new_product = payload
    if not new_product.get("code"):
        import time

        new_product["code"] = f"MAN-{int(time.time())}"

    new_list = [new_product] + state["inventario"]

    return {**state, "inventario": new_list}


def change_api_page(state, payload):
    new_page = state["ui_page"] + payload
    if new_page < 1:
        new_page = 1
    return {**state, "ui_page": new_page}


def delete_product(state, payload):
    code_to_delete = payload
    current_list = state["inventario"]
    new_list = [p for p in current_list if p.get("code") != code_to_delete]
    return {**state, "inventario": new_list}


def update_product(state, payload):
    updated_item = payload
    target_code = updated_item.get("code")
    current_list = state["inventario"]
    new_list = [
        updated_item if p.get("code") == target_code else p for p in current_list
    ]
    return {**state, "inventario": new_list}


def import_batch(state, payload):
    existing_codes = {p.get("code") for p in state["inventario"]}
    new_unique_items = [p for p in payload if p.get("code") not in existing_codes]
    return {
        **state,
        "inventario": state["inventario"] + new_unique_items,
        "resultados_api": [],
    }


initial_state = {
    "inventario": [],
    "resultados_api": [],
    "loading": False,
    "search_params": {},
    "ui_page": 1,
    "ui_page_size": 10,
}

inventory_reducer, actions = create_slice(
    name="inventory",
    initial_state=initial_state,
    reducers={
        "setLoading": lambda s, p: {**s, "loading": p},
        "setSearchParams": set_search_params,
        "searchSuccess": search_api_success,
        "changePage": change_api_page,
        "clearSearch": lambda s, _: {**s, "resultados_api": [], "ui_page": 1},
        "setInventory": lambda s, p: {**s, "inventario": p},
        "importBatch": import_batch,
        "createProduct": create_product,
        "deleteProduct": delete_product,
        "updateProduct": update_product,
    },
)
