from enum import IntEnum

class uSwidGlobalMap(IntEnum):
    TAG_ID: int
    SOFTWARE_NAME: int
    ENTITY: int
    EVIDENCE: int
    LINK: int
    SOFTWARE_META: int
    PAYLOAD: int
    HASH: int
    CORPUS: int
    PATCH: int
    MEDIA: int
    SUPPLEMENTAL: int
    TAG_VERSION: int
    SOFTWARE_VERSION: int
    VERSION_SCHEME: int
    LANG: int
    DIRECTORY: int
    FILE: int
    PROCESS: int
    RESOURCE: int
    SIZE: int
    FILE_VERSION: int
    KEY: int
    LOCATION: int
    FS_NAME: int
    ROOT: int
    PATH_ELEMENTS: int
    PROCESS_NAME: int
    PID: int
    TYPE: int
    ENTITY_NAME: int
    REG_ID: int
    ROLE: int
    THUMBPRINT: int
    DATE: int
    DEVICE_ID: int
    ARTIFACT: int
    HREF: int
    OWNERSHIP: int
    REL: int
    MEDIA_TYPE: int
    USE: int
    ACTIVATION_STATUS: int
    CHANNEL_TYPE: int
    COLLOQUIAL_VERSION: int
    DESCRIPTION: int
    EDITION: int
    ENTITLEMENT_DATA_REQUIRED: int
    ENTITLEMENT_KEY: int
    GENERATOR: int
    PERSISTENT_ID: int
    PRODUCT: int
    PRODUCT_FAMILY: int
    REVISION: int
    SUMMARY: int
    UNSPSC_CODE: int
    UNSPSC_VERSION: int

class uSwidVersionScheme(IntEnum):
    MULTIPARTNUMERIC: int
    MULTIPARTNUMERIC_SUFFIX: int
    ALPHANUMERIC: int
    DECIMAL: int
    SEMVER: int

USWID_HEADER_MAGIC: bytes
USWID_HEADER_FLAG_COMPRESSED: int

class uSwidHeaderFlags(IntEnum):
    NONE: int
    COMPRESSED: int

class uSwidPayloadCompression(IntEnum):
    NONE: int
    ZLIB: int
    LZMA: int
    @staticmethod
    def argparse(s): ...
