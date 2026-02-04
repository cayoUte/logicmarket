import aiohttp
from store.slices.inventory_slice import actions
from service.adapters import open_food_facts_adapter

def search_products_action(filters):
    """
    filters: dict { 'brands': '...', 'categories': '...', 'countries': '...' }
    """
    async def thunk(dispatch):
        print(f"🔍 Filtros recibidos de UI: {filters}") # Debug vital
        
        dispatch(actions["setLoading"](True))
        dispatch(actions["setSearchParams"](filters))

        url = "https://world.openfoodfacts.net/api/v2/search"
        
        # 1. PARAMETROS BASE (Convertidos a string explícitamente)
        # aiohttp a veces falla con enteros (500), mejor usar "500"
        params = {
            "fields": "code,product_name,brands,categories,countries",
            "page_size": "500", 
            "sort_by": "product_name",
            "json": "true"
        }
        
        # 2. INYECCIÓN SEGURA DE FILTROS
        # Nos aseguramos de que si entra algo, lo convertimos a str()
        if filters.get("brands"): 
            params["brands_tags"] = str(filters["brands"])
            
        if filters.get("categories"): 
            params["categories_tags"] = str(filters["categories"])
            
        if filters.get("countries"): 
            params["countries_tags_en"] = str(filters["countries"])

        try:
            async with aiohttp.ClientSession() as session:
                # Aquí es donde ocurría el error
                async with session.get(url, params=params) as resp:
                    
                    if resp.status == 200:
                        data = await resp.json()
                        raw_products = data.get("products", [])
                        
                        # Pasamos por el adaptador
                        clean_products = [
                            open_food_facts_adapter(p) for p in raw_products
                        ]
                        
                        print(f"✅ Éxito: {len(clean_products)} productos encontrados.")
                        dispatch(actions["searchSuccess"](clean_products))
                    else:
                        print(f"❌ Error API: {resp.status}")
                        dispatch(actions["setLoading"](False))
                        
        except Exception as e:
            # Imprimimos el tipo de error para saber qué pasó
            print(f"❌ Excepción Crítica en Service: {type(e).__name__}: {e}")
            dispatch(actions["setLoading"](False))

    return thunk