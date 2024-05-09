from .entity import uSwidEntity as uSwidEntity
from .vex_statement import uSwidVexStatement as uSwidVexStatement
from _typeshed import Incomplete
from typing import Any

class uSwidVexDocument:
    id: Incomplete
    author: Incomplete
    date: Incomplete
    version: Incomplete
    trusted_entity: Incomplete
    def __init__(self, data: dict[str, Any] | None = None) -> None: ...
    @property
    def statements(self) -> list[uSwidVexStatement]: ...
    def add_statement(self, statement: uSwidVexStatement) -> None: ...
    def load(self, data: dict[str, Any]) -> None: ...
