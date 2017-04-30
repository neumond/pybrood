from functools import partial
from .classes import parse_classes
from .objenums import parse_object_enums
from .pureenums import parse_pure_enums
from .cdeclparser import incflines


class HeaderParser:
    def __init__(self, bwapi_include_dir):
        self.bwapi_include_dir = bwapi_include_dir

    @property
    def incflines(self):
        return partial(incflines, self.bwapi_include_dir)

    def get_classes(self):
        return parse_classes(self.incflines)

    def get_objenums(self):
        return parse_object_enums(self.incflines)

    def get_pureenums(self):
        return parse_pure_enums(self.incflines)
