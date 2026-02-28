from objects.base_object import GameObject
from engine.audio_manager import AudioManager


class Item(GameObject):
    def __init__(self, position=(0, 0), character="♥", name="Item", dialogue=""):
        super().__init__(
            position,
            character,
            name=name,
            dialogue=dialogue,
            color="red1",
        )

    def interact(self, actor, screen):
        AudioManager.play("collect", volume=0.4)

        # Screen handles scene transition

        screen.end_level(self.name)
