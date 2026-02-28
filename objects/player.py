from objects.base_object import GameObject
from engine.audio_manager import AudioManager


class Player(GameObject):
    def __init__(self, position=(0, 0), character="@", name="Player", color="yellow"):
        super().__init__(
            position=position,
            character=character,
            name=name,
            color=color,
            dialogue="",
        )
        self._speech_played = False

    def interact(self, world):
        for obj in world.get_adjacent_objects(self):
            obj.interact(self, world)

    def get_adjacent_speech(self, world):
        speech = []

        for obj in world.get_adjacent_objects(self):
            if obj.dialogue:
                print_dialogue = obj.dialogue
                if hasattr(obj, "interact"):
                    print_dialogue = obj.dialogue + "\n\n Press TAB to interact"
                speech.append((obj.name, print_dialogue))

                if not self._speech_played:
                    AudioManager.play("speak")
                    self._speech_played = True

        if not speech:
            self._speech_played = False

        return speech

    ARROWS = {
        "UP": "△",
        "DOWN": "▽",
        "LEFT": "◁",
        "RIGHT": "▷",
    }

    def set_facing(self, direction: str):
        self.facing = direction.upper()
        self.character = self.ARROWS.get(self.facing, "@")
