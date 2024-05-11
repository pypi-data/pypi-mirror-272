from kozmoserver.errors import KozmoServerError

from typing import List, Union


class RemoteInferenceError(KozmoServerError):
    def __init__(self, code: int, reason: str):
        super().__init__(f"Remote inference call failed with {code}, {reason}")


class InvalidExplanationShape(KozmoServerError):
    def __init__(self, shape: Union[List[int], int]):
        super().__init__(
            f"Expected a single element, but multiple were returned {shape}"
        )
