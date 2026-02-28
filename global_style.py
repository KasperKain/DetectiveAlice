from rich import box

BORDER_STYLES = [
    box.ROUNDED,
    box.HORIZONTALS,
    box.MARKDOWN,
    box.ASCII,
    box.DOUBLE,
    box.SIMPLE,
]
_current_index = 0


def get_border():
    return BORDER_STYLES[_current_index]


def cycle_border():
    global _current_index
    _current_index = (_current_index + 1) % len(BORDER_STYLES)
