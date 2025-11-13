class GenericError(Exception):
    """Base class for any kind of error."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message