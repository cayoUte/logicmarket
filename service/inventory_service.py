import aiohttp
from store.slices.inventory_slice import actions
from service.adapters import open_food_facts_adapter


def search_products_action(filters):
    """
    filters: dict { 'brands': '...', 'categories': '...', 'countries': '...' }
    """

    async def thunk(dispatch):
        print(f"🔍 Filtros recibidos de UI: {filters}")

        dispatch(actions["setLoading"](True))
        dispatch(actions["setSearchParams"](filters))

        url = "https://world.openfoodfacts.net/api/v2/search"

        params = {
            "fields": "code,product_name,brands,categories,countries",
            "page_size": "500",
            "sort_by": "product_name",
            "json": "true",
        }

        if filters.get("brands"):
            params["brands_tags"] = str(filters["brands"])

        if filters.get("categories"):
            params["categories_tags"] = str(filters["categories"])

        if filters.get("countries"):
            params["countries_tags_en"] = str(filters["countries"])

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:

                    if resp.status == 200:
                        data = await resp.json()
                        raw_products = data.get("products", [])

                        clean_products = [
                            open_food_facts_adapter(p) for p in raw_products
                        ]

                        print(f"✅ Éxito: {len(clean_products)} productos encontrados.")
                        dispatch(actions["searchSuccess"](clean_products))
                    else:
                        print(f"❌ Error API: {resp.status}")
                        dispatch(actions["setLoading"](False))

        except Exception as e:
            print(f"❌ Excepción Crítica en Service: {type(e).__name__}: {e}")
            dispatch(actions["setLoading"](False))

    return thunk
