from enum import IntEnum
from uswid import NotSupportedError as NotSupportedError, uSwidComponent as uSwidComponent, uSwidContainer as uSwidContainer, uSwidEntity as uSwidEntity, uSwidEntityRole as uSwidEntityRole, uSwidPayloadCompression as uSwidPayloadCompression, uSwidProblem as uSwidProblem, uSwidVersionScheme as uSwidVersionScheme
from uswid.format_coswid import uSwidFormatCoswid as uSwidFormatCoswid
from uswid.format_cyclonedx import uSwidFormatCycloneDX as uSwidFormatCycloneDX
from uswid.format_goswid import uSwidFormatGoswid as uSwidFormatGoswid
from uswid.format_ini import uSwidFormatIni as uSwidFormatIni
from uswid.format_pkgconfig import uSwidFormatPkgconfig as uSwidFormatPkgconfig
from uswid.format_spdx import uSwidFormatSpdx as uSwidFormatSpdx
from uswid.format_swid import uSwidFormatSwid as uSwidFormatSwid
from uswid.format_uswid import uSwidFormatUswid as uSwidFormatUswid
from uswid.vex_document import uSwidVexDocument as uSwidVexDocument

class SwidFormat(IntEnum):
    UNKNOWN: int
    INI: int
    XML: int
    USWID: int
    PE: int
    JSON: int
    PKG_CONFIG: int
    COSWID: int
    CYCLONE_DX: int
    SPDX: int
    VEX: int

def main() -> None: ...
