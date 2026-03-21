from domain.product import Product
from domain.product_category import ProductCategory
from domain.perishability_level import PerishabilityLevel
from domain.exceptions import InvalidProductCategoryError
import pytest

class TestProduct:

    def test_product_creation_success(self):
        product = Product(ProductCategory.CROP, PerishabilityLevel.CRITICAL)
    
    def test_invalid_category_raises_error(self):
        with pytest.raises(InvalidProductCategoryError):
            product = Product("INVALID", PerishabilityLevel.CRITICAL)
