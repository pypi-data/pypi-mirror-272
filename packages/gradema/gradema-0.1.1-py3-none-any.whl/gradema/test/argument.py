__all__ = ["OUTPUT_FILE", "Argument", "ResolvedArgumentInfo", "OutputFile"]

from pathlib import Path
from typing import Union


class OutputFile:
    pass


OUTPUT_FILE = OutputFile()


Argument = str | OutputFile
ResolvedArgumentInfo = Union[None, Path]
