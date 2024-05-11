from kozmoserver.errors import KozmoServerError
from typing import Optional


class InvalidMLlibFormat(KozmoServerError):
    def __init__(self, name: str, model_uri: Optional[str] = None):
        msg = f"Invalid MLlib format for model {name}"
        if model_uri:
            msg += f" ({model_uri})"

        super().__init__(msg)
