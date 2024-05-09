from _typeshed import Incomplete
from enum import IntEnum

class uSwidHashAlg(IntEnum):
    UNKNOWN: int
    SHA256: int
    SHA384: int
    SHA512: int
    @classmethod
    def from_string(cls, alg_id: str) -> uSwidHashAlg: ...

class uSwidHash:
    alg_id: Incomplete
    def __init__(self, alg_id: uSwidHashAlg | None = None, value: str | None = None) -> None: ...
    @property
    def alg_id_for_display(self) -> str | None: ...
    @property
    def value(self) -> str | None: ...
    @value.setter
    def value(self, value: str | None) -> None: ...
