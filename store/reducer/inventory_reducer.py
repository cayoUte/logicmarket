def inventory_reducer(state, action):
    tipo, payload = action
    
    # --- ZONA API (Importador) ---
    if tipo == 'API_BUSQUEDA_EXITO':
        # payload: lista de productos crudos de la API
        print(payload, "<- payload en reducer")
        return {**state, "resultados_api": payload, "loading": False}
        
    elif tipo == 'LIMPIAR_BUSQUEDA':
         return {**state, "resultados_api": []}

    # --- ZONA INVENTARIO ---
    elif tipo == 'CARGAR_INICIAL':
        return {**state, "inventario": payload}

    elif tipo == 'IMPORTAR_LOTE':
        """
        AQUÍ ESTÁ LA CLAVE DEL REQUERIMIENTO:
        Recibimos una lista de productos de la API, y un objeto de configuración
        (precio y stock por defecto definidos por el usuario en la UI).
        """
        productos_api, config_lote = payload
        precio_defecto = config_lote.get('precio', 0.0)
        stock_defecto = config_lote.get('stock', 0)
        proveedor_defecto = config_lote.get('proveedor', 'General')

        # HOF: map para transformar datos de API a datos de Inventario en bloque
        nuevos_items = [
            {
                "COD": p.get('code', 'N/A')[-4:], # Últimos 4 dígitos
                "PRODUCTO": p.get('product_name', 'Sin Nombre')[:40],
                "MARCA": p.get('brands', 'Genérico')[:20],
                "CATEGORÍA": p.get('categories', '').split(',')[0][:20],
                "STOCK": stock_defecto,      # Aplicado masivamente
                "PRECIO": precio_defecto,    # Aplicado masivamente
                "PROVEEDOR": proveedor_defecto
            }
            for p in productos_api
        ]
        
        # Concatenamos al inventario existente (Inmutabilidad)
        nuevo_inventario = state["inventario"] + nuevos_items
        
        return {
            **state, 
            "inventario": nuevo_inventario, 
            "resultados_api": [] # Limpiamos la mesa de trabajo
        }

    return state