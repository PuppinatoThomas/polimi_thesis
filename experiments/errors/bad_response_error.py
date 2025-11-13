from experiments.errors.generic_error import GenericError

class BadResponseError(GenericError):
    """Raised when an evaluator LLM answered with something invalid."""
    def __init__(self, response: str) -> None:
        message = f"The following response is invalid: {response}."
        super().__init__(message)