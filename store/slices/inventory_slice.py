from store.utils.utils import create_slice

# --- MINI REDUCERS ---

def set_search_params(state, payload):
    # Guardamos qué buscó el usuario para poder "cargar más" después si quisiéramos
    return {**state, "search_params": payload}

def search_success(state, payload):
    # payload: lista de 50-100 productos
    # Al buscar de nuevo, reseteamos la pagina a la 1
    return {
        **state, 
        "resultados_api": payload, 
        "loading": False,
        "ui_page": 1 
    }

def change_page(state, payload):
    # payload: +1 (siguiente) o -1 (anterior)
    new_page = state["ui_page"] + payload
    # Evitamos ir a página 0
    if new_page < 1: new_page = 1
    
    # (Opcional) Podríamos validar max_page aquí si tuviéramos el total
    return {**state, "ui_page": new_page}

# --- INITIAL STATE MEJORADO ---
initial_state = {
    "inventario": [],
    "resultados_api": [], # Aquí viven los 100 productos cacheados
    "loading": False,
    "search_params": {},
    "ui_page": 1,         # Página actual de la TABLA
    "ui_page_size": 10    # Filas por página en la TABLA
}

inventory_reducer, actions = create_slice(
    name="inventory",
    initial_state=initial_state,
    reducers={
        "setLoading": lambda s, p: {**s, "loading": p},
        "searchSuccess": search_success,
        "setSearchParams": set_search_params,
        "changePage": change_page,
        "clearSearch": lambda s, _: {**s, "resultados_api": [], "ui_page": 1},
        "setInventory": lambda s, p: {**s, "inventario": p},                
        "importBatch": lambda s, p: { 
            **s, 
            "inventario": s["inventario"] + p, 
            "resultados_api": [] # Limpiamos la búsqueda al importar
        } 
    }
)