
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

class InvalidPriceError(Exception):
        """Raised when sell mode price is <= 0"""
        pass

class InvalidListingModeError(Exception):
        """Raised when listing mode is invlaid"""
        pass

class InvalidPhotoUrlError(Exception):
        """Raise when photo url is invalid"""
        pass

class ListingNotFoundError(Exception):
        """Raise when listing is not present"""
        pass
