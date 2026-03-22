
class UnauthorisedOperationError(Exception):
        """Raised when a producer attempts to modify a resource they do not own."""
        pass

class InvalidProductCategoryError(Exception):
        """Raised when there is incorrect product category"""
        pass

class NoProducerTypeError(Exception):
        """Raised when there is no producer type"""
        pass
        
class InvalidProducerTypeError(Exception):
        """Raised when there is invlaid producer type"""
        pass

class ProductAlreadyExistsError(Exception):
        """Raised when product already exists when adding product for producer profile"""
        pass
