from .entity import uSwidEntity as uSwidEntity
from .vex_document import uSwidVexDocument as uSwidVexDocument
from .vex_product import uSwidVexProduct as uSwidVexProduct
from _typeshed import Incomplete
from enum import Enum

class uSwidVexStatementStatus(Enum):
    UNKNOWN: str
    NOT_AFFECTED: str
    AFFECTED: str
    FIXED: str
    UNDER_INVESTIGATION: str
    @classmethod
    def from_string(cls, status: str) -> uSwidVexStatementStatus: ...

class uSwidVexStatementJustification(Enum):
    UNKNOWN: str
    COMPONENT_NOT_PRESENT: str
    VULNERABLE_CODE_NOT_PRESENT: str
    VULNERABLE_CODE_NOT_IN_EXECUTE_PATH: str
    VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY: str
    INLINE_MITIGATIONS_ALREADY_EXIST: str
    @classmethod
    def from_string(cls, status: str) -> uSwidVexStatementJustification: ...

class uSwidVexStatement:
    vulnerability_name: Incomplete
    status: Incomplete
    justification: Incomplete
    impact_statement: Incomplete
    products: Incomplete
    def __init__(self) -> None: ...
    @property
    def trusted_entity(self) -> uSwidEntity | None: ...
