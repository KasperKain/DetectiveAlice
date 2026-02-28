from engine.audio_manager import AudioManager
from objects.base_object import GameObject


class Door(GameObject):
    OFFSCREEN = (-1, -1)

    def __init__(
        self,
        position=(0, 0),
        character="▒",
    ):
        super().__init__(
            position,
            character,
            name="Door",
            dialogue="Closed",
            color="hot_pink2",
        )
        self.opened = False

    def open(self, world, should_play_sound=True):
        if self.opened:
            return
        self.opened = True

        world._pos_lookup.pop(self.position, None)

        self.position = self.OFFSCREEN
        if should_play_sound:
            AudioManager.play("open")
