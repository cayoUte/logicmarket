def inventory_reducer(state, action):
    tipo, payload = action

    if tipo == "API_BUSQUEDA_EXITO":
        print(payload, "<- payload en reducer")
        return {**state, "resultados_api": payload, "loading": False}

    elif tipo == "LIMPIAR_BUSQUEDA":
        return {**state, "resultados_api": []}

    elif tipo == "CARGAR_INICIAL":
        return {**state, "inventario": payload}

    elif tipo == "IMPORTAR_LOTE":
        productos_api, config_lote = payload
        precio_defecto = config_lote.get("precio", 0.0)
        stock_defecto = config_lote.get("stock", 0)
        proveedor_defecto = config_lote.get("proveedor", "General")

        nuevos_items = [
            {
                "COD": p.get("code", "N/A")[-4:],
                "PRODUCTO": p.get("product_name", "Sin Nombre")[:40],
                "MARCA": p.get("brands", "Genérico")[:20],
                "CATEGORÍA": p.get("categories", "").split(",")[0][:20],
                "STOCK": stock_defecto,
                "PRECIO": precio_defecto,
                "PROVEEDOR": proveedor_defecto,
            }
            for p in productos_api
        ]

        nuevo_inventario = state["inventario"] + nuevos_items

        return {**state, "inventario": nuevo_inventario, "resultados_api": []}

    return state
