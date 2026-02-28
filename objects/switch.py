from objects.base_object import GameObject
from engine.audio_manager import AudioManager


class Switch(GameObject):
    character = "○"  # untriggered
    triggered_char = "◉"  # triggered
    name = "Switch"

    def __init__(self, position=(0, 0), character="○", name=None, dialogue=""):
        super().__init__(
            position,
            character or self.character,
            name or self.name,
            dialogue or "Move a block on top to activate!",
        )
        self.triggered = False
        self.color = "royal_blue1"

    def trigger(self, obj):
        if self.triggered:
            return
        AudioManager.play("trigger")
        if callable(getattr(obj, "can_move", None)) and obj.can_move():
            self.triggered = True
            self.character = self.triggered_char
            self.dialogue = "Activated!"
