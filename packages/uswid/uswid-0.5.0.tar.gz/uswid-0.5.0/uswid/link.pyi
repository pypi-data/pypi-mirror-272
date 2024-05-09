from .component import uSwidComponent as uSwidComponent
from .problem import uSwidProblem as uSwidProblem
from _typeshed import Incomplete
from enum import IntEnum

class uSwidLinkRel(IntEnum):
    LICENSE: int
    COMPILER: int
    ANCESTOR: int
    COMPONENT: int
    FEATURE: int
    INSTALLATIONMEDIA: int
    PACKAGEINSTALLER: int
    PARENT: int
    PATCHES: int
    REQUIRES: int
    SEE_ALSO: int
    SUPERSEDES: int
    SUPPLEMENTAL: int

class uSwidLink:
    component: Incomplete
    def __init__(self, href: str | None = None, rel: str | None = None) -> None: ...
    @property
    def rel(self) -> str | None: ...
    @rel.setter
    def rel(self, rel: str | None) -> None: ...
    @property
    def href(self) -> str | None: ...
    @href.setter
    def href(self, href: str | None) -> None: ...
    @property
    def href_for_display(self) -> str | None: ...
    def problems(self) -> list[uSwidProblem]: ...
