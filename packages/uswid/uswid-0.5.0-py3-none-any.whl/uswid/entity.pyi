from .problem import uSwidProblem as uSwidProblem
from _typeshed import Incomplete
from enum import IntEnum

class uSwidEntityRole(IntEnum):
    TAG_CREATOR: int
    SOFTWARE_CREATOR: int
    AGGREGATOR: int
    DISTRIBUTOR: int
    LICENSOR: int
    MAINTAINER: int

class uSwidEntity:
    name: Incomplete
    regid: Incomplete
    roles: Incomplete
    def __init__(self, name: str | None = None, regid: str | None = None, roles: list[uSwidEntityRole] | None = None) -> None: ...
    def problems(self) -> list[uSwidProblem]: ...
