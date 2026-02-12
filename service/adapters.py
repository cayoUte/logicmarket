from typing import Protocol, TypedDict, Dict, Any


class ProductoNormalizado(TypedDict):
    code: str
    name: str
    brand: str
    category: str
    country: str
    price: float
    stock: int
    supplier: str
    image_url: str


class AdapterProtocol(Protocol):
    def __call__(self, raw_data: Dict[str, Any]) -> ProductoNormalizado: ...


def open_food_facts_adapter(raw_product: Dict[str, Any]) -> ProductoNormalizado:
    return {
        "code": raw_product.get("code", "S/N"),
        "name": raw_product.get("product_name", "Sin Nombre"),
        "brand": raw_product.get("brands", "Genérico"),
        "category": raw_product.get("categories", "").split(",")[0],
        "country": raw_product.get("countries", "").split(",")[0],
        "price": 0.00,
        "stock": 0,
        "supplier": "Genérico",
        "image_url": raw_product.get("image_front_small_url", ""),
    }
