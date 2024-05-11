from kozmoml.errors import KozmoMLError
from typing import Optional


class InvalidMLlibFormat(KozmoMLError):
    def __init__(self, name: str, model_uri: Optional[str] = None):
        msg = f"Invalid MLlib format for model {name}"
        if model_uri:
            msg += f" ({model_uri})"

        super().__init__(msg)
