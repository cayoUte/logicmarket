from typing import Protocol, TypedDict, Dict, Any

# 1. DEFINICIÓN DE TU ESTÁNDAR (Como quieres que sea tu objeto interno)
class ProductoNormalizado(TypedDict):
    code: str
    name: str
    brand: str
    category: str
    country: str
    # Campos que la API no da, pero tu sistema necesita (Defaults)
    price: float
    stock: int
    supplier: str
    image_url: str
# 2. EL PROTOCOLO (La firma de la función adaptadora)
class AdapterProtocol(Protocol):
    def __call__(self, raw_data: Dict[str, Any]) -> ProductoNormalizado: ...

# 3. LA IMPLEMENTACIÓN CONCRETA (Open Food Facts)
def open_food_facts_adapter(raw_product: Dict[str, Any]) -> ProductoNormalizado:
    # Extraemos con seguridad (usando .get para evitar crashes)
    return {
        "code": raw_product.get("code", "S/N"),
        "name": raw_product.get("product_name", "Sin Nombre"),
        "brand": raw_product.get("brands", "Genérico"),
        # La API a veces devuelve listas o strings, aquí limpiamos
        "category": raw_product.get("categories", "").split(',')[0], 
        "country": raw_product.get("countries", "").split(',')[0],
        # Valores por defecto de negocio
        "price": 0.00,
        "stock": 0,
        "supplier": "Genérico",
        "image_url": raw_product.get("image_front_small_url", "")
    }