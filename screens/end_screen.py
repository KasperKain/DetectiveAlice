from rich.text import Text
from rich.style import Style
from engine.audio_manager import AudioManager
from render.window import RowLayoutBuilder, WindowPanel
from screens.base_screen import BaseScreen
from utils.paths import resource_path


class EndingScreen(BaseScreen):
    accept_commands = True
    accept_arrows = False

    def __init__(self):
        super().__init__()
        AudioManager.play_music(
            resource_path("audio/end_music.wav"), volume=0.8, loops=-1
        )

    def _ending_text(self):
        txt = Text()

        txt.append(
            "CASE CLOSED\n\n",
            Style(color="bright_white", bold=True),
        )

        txt.append(
            "Detective Alice is dead.\n\n",
            Style(color="white"),
        )

        txt.append(
            "You have known this from the beginning.\n\n",
            Style(color="white"),
        )

        txt.append(
            "The investigation was never meant to change the outcome. "
            "There was no suspect to confront, no mistake to correct, "
            "and no version of events where the conclusion differed.\n\n",
            Style(color="white"),
        )

        txt.append(
            "What remained was procedure.\n\n",
            Style(color="bright_white"),
        )

        txt.append(
            "A detective does not stop working because the answer is painful. "
            "She stops when the facts are complete, the evidence accounted for, "
            "and nothing meaningful remains unresolved.\n\n",
            Style(color="white"),
        )

        txt.append(
            "Each place you visited, each object you examined, served that purpose. "
            "They were not clues leading forward, but confirmations, "
            "a careful reconstruction of something already finished.\n\n",
            Style(color="white"),
        )

        txt.append(
            "The case was yours.\n\n",
            Style(color="white"),
        )

        txt.append(
            "And now, it has been properly closed.\n\n",
            Style(color="bright_white", bold=True),
        )

        txt.append(
            "With the work complete, there is no need to continue searching.\n"
            "You accept the conclusion, as you were trained to do.\n\n",
            Style(color="white"),
        )

        txt.append(
            "Press ESC to return.",
            Style(color="yellow", italic=True),
        )

        return txt

    def render(self):
        panel = WindowPanel(
            "[ CASE CLOSED ]",
            self._ending_text,
            border_style="bright_white",
        )
        row = RowLayoutBuilder([panel], ratios=[1])
        return row.build()
