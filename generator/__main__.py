from . import skel
from .parser import HeaderParser
from .config import BWAPI_INCLUDE_DIR, GEN_OUTPUT_DIR, VCXProjectConfig


skel.main(
    HeaderParser(BWAPI_INCLUDE_DIR),
    GEN_OUTPUT_DIR,
    VCXProjectConfig,
)
