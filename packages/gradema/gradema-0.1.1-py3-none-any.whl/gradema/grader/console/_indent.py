import io
from typing import TextIO


class IndentTextIOWrapper(io.BytesIO):
    """
    A wrapper around a TextIO object to put indentation before each line.

    This is a little messy because the subprocess package won't let you pass just any TextIO object to the run function,
    so you usually have to pass subprocess.PIPE, and then feed the piped output to this for it to actually do anything.

    TLDR; This would be cool to use, but it's hard to get to work.

    Additionally, putting correct type hints on this is difficult, so we need to figure that out

    Notes for later:
    MYPY_FORCE_COLOR=1
    """

    def __init__(self, stdout: TextIO, indent: str):
        super().__init__()
        self.stdout = stdout
        self.indent = indent
        self.__needs_indent = True

    def write(self, text):  # type: ignore
        for ascii_value in text:
            c = chr(ascii_value)
            if c == "\n":
                self.__needs_indent = True
            elif c != "\r" and self.__needs_indent:
                self.stdout.write(self.indent)
                self.__needs_indent = False
            self.stdout.write(c)

    def flush(self) -> None:
        self.stdout.flush()
