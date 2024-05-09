from .component import uSwidComponent as uSwidComponent
from .container import uSwidContainer as uSwidContainer
from .entity import uSwidEntityRole as uSwidEntityRole
from .format import uSwidFormatBase as uSwidFormatBase
from _typeshed import Incomplete

class uSwidFormatPkgconfig(uSwidFormatBase):
    filepath: Incomplete
    def __init__(self, filepath: str | None = None) -> None: ...
    def load(self, blob: bytes, path: str | None = None) -> uSwidContainer: ...
