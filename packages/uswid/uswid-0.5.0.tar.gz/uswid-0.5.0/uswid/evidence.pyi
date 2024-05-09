from .problem import uSwidProblem as uSwidProblem
from _typeshed import Incomplete
from datetime import datetime

class uSwidEvidence:
    date: Incomplete
    device_id: Incomplete
    def __init__(self, date: datetime | None = None, device_id: str | None = None) -> None: ...
    def problems(self) -> list[uSwidProblem]: ...
