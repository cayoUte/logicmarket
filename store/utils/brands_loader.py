import json
import os


def load_brands_list(json_path="brands.json"):
    """
    Lee el brands.json de OpenFoodFacts y devuelve una lista plana de nombres.
    Ej: ["Nestlé", "Coca-Cola", "Milka", ...]
    """
    if not os.path.exists(json_path):
        print(f"⚠️ Advertencia: No se encontró {json_path}")
        return []

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        brands = []
        for key, value in data.items():
            try:
                name_obj = value.get("name", {})
                brand_name = name_obj.get("xx") or name_obj.get("en")

                if not brand_name and name_obj:
                    brand_name = list(name_obj.values())[0]

                if brand_name:
                    brands.append(brand_name)
            except:
                continue

        return sorted(list(set(brands)))

    except Exception as e:
        print(f"❌ Error leyendo brands.json: {e}")
        return []
