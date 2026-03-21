from domain.product_category import ProductCategory
from domain.perishability_level import PerishabilityLevel
from domain.exceptions import InvalidProductCategoryError
from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
    category: ProductCategory
    perishability: PerishabilityLevel

    def __post_init__(self):
        if not isinstance(self.category, ProductCategory):
            raise InvalidProductCategoryError("Product category does not exist")
    