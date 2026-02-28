from engine.audio_manager import AudioManager
from objects.item import Item


class FinalItem(Item):
    def interact(
        self, player, screen
    ):  # I don't remember why I needed "player here", but the class breaks without it.
        self.color = "red1"

        # Trigger ending
        screen.end_game_sequence()

        # Play sound
        AudioManager.play("end", volume=1)
