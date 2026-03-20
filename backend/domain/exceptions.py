
class UnauthorisedOperationError(Exception):
        """Raised when a producer attempts to modify a resource they do not own."""
        pass