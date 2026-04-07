
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

class InvalidTemperatureCelciusRange(Exception):
        """Raise when invalid celcius temperature range"""
        pass

class InvalidHumidityRange(Exception):
        """Raise when humidity range is invalid"""
        pass

class InvalidPrecipitationValue(Exception):
        """Raise when precipitation value is less than zero"""
        pass

class InvalidLowTemperature(Exception):
        """Raise when low temperature is greater than high temperature"""
        pass

class InvalidSimilarityScoreRangeError(Exception):
        """Raise when similarity score range is invalid"""
        pass

class EmptyContentError(Exception):
        """Raise when content is empty"""
        pass

class EmptyCountryError(Exception):
        """Raise when country is empty"""
        pass
