from rich.text import Text
from rich.style import Style
from render.effects_manager import full_map_glitch

CHAR_STYLES = {
    "▓": Style(color="bright_blue"),
    "▒": Style(color="blue"),
    "^": Style(color="green", strike=True),
    "#": Style(conceal=True, bgcolor="cyan"),
    "!": Style(conceal=True),
    ",": Style(color="dark_green", dim=True, italic=True),
    "|": Style(color="pale_turquoise1", strike=True),
    "@": Style(color="yellow", bold=True),
}


def render_world(world, player):
    output = Text()

    for r in range(world.height):
        row_text = Text()

        for c in range(world.width):
            pos = (r, c)

            char = world.base_grid[r][c]
            style = CHAR_STYLES.get(char, None)

            obj = world.get_object_at(pos)
            if obj:
                char = obj.character

                if hasattr(obj, "get_style"):
                    style = obj.get_style()

            char, style = world.effects_manager.apply(pos, char, style, player, world)

            if style:
                row_text.append(char, style=style)
            else:
                row_text.append(char)

        # What is output? I don't remember.
        output.append(row_text)
        output.append("\n")

    return output


def render_overworld(grid, highlight_region, grid_rows, grid_cols):
    text = Text()
    cell_height = len(grid) // grid_rows
    cell_width = len(grid[0]) // grid_cols
    row_idx, col_idx = highlight_region
    top = row_idx * cell_height
    left = col_idx * cell_width
    bottom = min(top + cell_height, len(grid))
    right = min(left + cell_width, len(grid[0]))

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            char = grid[r][c]
            # Draw red border on map to see selected region. Doesn't work how I'd like it to... but it works so I'll leave it as is.
            if (r == top or r == bottom - 1) and left <= c < right:
                text.append("▒", style=Style(color="green", bold=True))
                continue
            if (c == left or c == right - 1) and top <= r < bottom:
                text.append("▒", style=Style(color="green", bold=True))
                continue

            text.append(char, style=CHAR_STYLES.get(char, Style()))
        text.append("\n")
    return text


def render_intro(frame_grid):
    text = Text()

    # Ewww
    if isinstance(frame_grid, str):
        lines = frame_grid.splitlines()
        frame_grid = [list(line) for line in lines]
    elif isinstance(frame_grid, list) and isinstance(frame_grid[0], str):
        frame_grid = [list(line) for line in frame_grid]

    for row in frame_grid:
        for ch in row:
            style = CHAR_STYLES.get(ch, Style())
            text.append(ch, style)
        text.append("\n")

    return text
