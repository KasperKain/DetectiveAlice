from rich.style import Style

OFFSCREEN_POSITION = (-9999, -9999)  # Force objects waaayyy off screen


class GameObject:
    def __init__(
        self, position=(0, 0), character="?", name="", dialogue="", color="black"
    ):
        self.position = tuple(position)
        self.character = character
        self.name = name
        self.dialogue = dialogue
        self.color = color  # MUST store color. Prevents errors.

    def move_to(self, world, new_position):
        """Request a position change; world enforces rules."""
        world.move_object(self, new_position)

    def update(self, world):
        pass

    # Force objects off screen and deactivate, somewhat like object pooling in game design.
    def remove_from_world(self):
        self.position = OFFSCREEN_POSITION

    def get_style(self):
        if self.color:
            return Style(color=self.color)
        return Style()
