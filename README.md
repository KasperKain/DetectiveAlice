# Untitled Text Game

A surreal, text-based puzzle game where progression is driven by interaction, exploration, and quiet observation.
The game is rendered entirely using text characters and symbols. Dialogue, environments, and mechanics are intentionally minimalist and abstract.

---

## Features

- Explore multiple text-rendered areas
- Interact with characters through dialogue
- Solve block-based spatial puzzles
- Unlock new areas by completing objectives
- Collect items that advance progression

---

## Controls
When viewing the overworld, input is handled through typed commands.

north / n

south / s

east / e

west / w

enter – Enter the selected region

help – Show the help screen

style – Cycle visual border styles

quit – Exit the game

Commands are visible on the help screen at any time.


When viewing the localworld (region), input is handled through keybinds.

Arrow Keys – Move

TAB – Interact with nearby objects

ESC – Return to the overworld
---

## Requirements

If running from source, the following Python packages are required:

- `pygame` (used for audio)
- `rich`
- `readchar`

These are listed in `requirements.txt`.

---

## Running From Source

1. Ensure Python 3.10+ is installed
2. Create and activate a virtual environment (optional but recommended)
3. Install dependencies:
   ```bash
   pip install -r requirements.txt