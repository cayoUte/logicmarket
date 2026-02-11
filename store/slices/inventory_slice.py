from store.utils.utils import create_slice

# ==========================================
# 1. MINI REDUCERS (Lógica Pura)
# ==========================================

def set_search_params(state, payload):
    """
    Actualiza el texto del buscador global (AppBar).
    InventoryPage usa esto para filtrar la tabla localmente.
    payload: {"query": "texto"}
    """
    return {**state, "search_params": payload}

def search_api_success(state, payload):
    """
    Guarda los resultados de OpenFoodFacts (ImporterPage).
    payload: Lista de productos de la API.
    """
    return {
        **state, 
        "resultados_api": payload, 
        "loading": False,
        "ui_page": 1  # Reseteamos paginación de la API
    }
def create_product(state, payload):
    """
    Crea un producto manualmente y lo agrega al inicio.
    payload: Diccionario del producto nuevo.
    """
    new_product = payload
    # Generar un ID temporal si no tiene código (opcional)
    if not new_product.get("code"):
        import time
        new_product["code"] = f"MAN-{int(time.time())}"
        
    # Insertar al inicio de la lista
    new_list = [new_product] + state["inventario"]
    
    return {**state, "inventario": new_list}

def change_api_page(state, payload):
    """
    Cambia la página de resultados de la API (ImporterPage).
    payload: +1 o -1
    """
    new_page = state["ui_page"] + payload
    if new_page < 1: new_page = 1
    return {**state, "ui_page": new_page}

# --- NUEVAS ACCIONES CRUD ---

def delete_product(state, payload):
    """
    Elimina un producto del inventario local.
    payload: 'code' (str) del producto a borrar.
    """
    code_to_delete = payload
    current_list = state["inventario"]
    
    # Filtramos la lista excluyendo el código recibido
    new_list = [p for p in current_list if p.get("code") != code_to_delete]
    
    return {**state, "inventario": new_list}

def update_product(state, payload):
    """
    Actualiza un producto existente.
    payload: Diccionario completo del producto modificado.
    """
    updated_item = payload
    target_code = updated_item.get("code")
    current_list = state["inventario"]
    
    # Recorremos y reemplazamos solo el que coincida
    new_list = [
        updated_item if p.get("code") == target_code else p
        for p in current_list
    ]
    
    return {**state, "inventario": new_list}

def import_batch(state, payload):
    """
    Agrega nuevos productos desde el importador.
    payload: Lista de productos nuevos.
    """
    # Evitar duplicados (opcional, pero recomendado)
    existing_codes = {p.get("code") for p in state["inventario"]}
    new_unique_items = [p for p in payload if p.get("code") not in existing_codes]
    
    return { 
        **state, 
        "inventario": state["inventario"] + new_unique_items, 
        "resultados_api": [] # Limpiamos la búsqueda API al importar para dar feedback visual
    }

# ==========================================
# 2. INITIAL STATE
# ==========================================
initial_state = {
    "inventario": [],       # Tu base de datos local (se guarda en disco)
    "resultados_api": [],   # Caché temporal de OpenFoodFacts
    "loading": False,
    "search_params": {},    # Estado del buscador del AppBar
    "ui_page": 1,           # Paginación actual del Importador
    "ui_page_size": 10 
}

# ==========================================
# 3. SLICE CREATION
# ==========================================
inventory_reducer, actions = create_slice(
    name="inventory",
    initial_state=initial_state,
    reducers={
        # Utilidades UI
        "setLoading": lambda s, p: {**s, "loading": p},
        "setSearchParams": set_search_params,
        
        # Lógica API (Importer)
        "searchSuccess": search_api_success,
        "changePage": change_api_page,
        "clearSearch": lambda s, _: {**s, "resultados_api": [], "ui_page": 1},
        
        # Lógica CRUD (Inventory)
        "setInventory": lambda s, p: {**s, "inventario": p}, # Carga inicial desde disco
        "importBatch": import_batch,
        "createProduct": create_product,
        "deleteProduct": delete_product,  # <--- NUEVO
        "updateProduct": update_product   # <--- NUEVO
    }
)