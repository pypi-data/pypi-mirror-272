def indentation(depth: int) -> str:
    return "  " * depth


def indent_text(depth: int, text: str) -> str:
    needs_indent = True
    indent = indentation(depth)
    r = ""
    for c in text:
        if c == "\n":
            needs_indent = True
        elif c != "\r" and needs_indent:
            r += indent
            needs_indent = False
        r += c
    return r


def arrow(depth: int) -> str:
    return "--" * (depth - 1) + "> " * (1 if depth else 0)


def header(depth: int, width: int) -> str:
    if depth == 0 or depth == 1:
        return "=" * width
    elif depth == 1:
        return "-" * width
    elif depth == 2:
        return "-" * width
    elif depth == 3:
        return '"' * width
    else:
        return "~" * width
