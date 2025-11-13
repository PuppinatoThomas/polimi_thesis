from experiments.errors.generic_error import GenericError

class DisableItemError(GenericError):
    """Raised when you try to disable an item you aren't supposed to disable."""
    def __init__(self, item_id: str, reason: str) -> None:
        message = f"You cannot disable the {item_id} item because {reason}."
        super().__init__(message)