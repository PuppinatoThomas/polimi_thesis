from experiments.errors.generic_error import GenericError

class CheckItemError(GenericError):
    """Raised when you try to check an item you aren't supposed to check."""
    def __init__(self, item_id: str, reason: str) -> None:
        message = f"You cannot check the {item_id} item because {reason}."
        super().__init__(message)