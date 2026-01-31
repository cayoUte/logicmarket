import aiohttp



def search_products_action(query_text):
    async def thunk(dispatch):
        print(f"Buscando productos para: {query_text}")
        dispatch(("SET_LOADING", True))

        url = "https://world.openfoodfacts.net/api/v2/search"
        params = {
            "categories_tags": query_text,
            "fields": "code,product_name,brands,categories", # Agregué categories por si acaso
            "page_size": 10,
            "countries_tags_en": "ecuador",
            "json": "true",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        products = data.get("products", [])
                        
                        # CORRECCIÓN: Enviamos la lista de diccionarios PURA
                        # No convertimos a tuplas todavía
                        print(f"✅ Búsqueda exitosa. Encontrados: {len(products)}")
                        dispatch(("API_BUSQUEDA_EXITO", products)) 
                        
                        # Nota: Asegúrate que el tipo de acción coincida con tu reducer 
                        # (En tu reducer usas 'API_BUSQUEDA_EXITO', en tu servicio tenías 'BUSQUEDA_EXITO')
                    else:
                        print("Error API")
                        dispatch(("SET_LOADING", False))
        except Exception as e:
            print(f"Error: {e}")
            dispatch(("SET_LOADING", False))

    return thunk