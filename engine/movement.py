# engine/movement.py


# Maybe could have been part of the player class, but I figured more things would end up using this in the future. Oh well!

from engine.game_state import GameState


DIR_DELTAS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


def attempt_move(world, obj, direction: str) -> bool:
    direction = direction.upper()
    if direction not in DIR_DELTAS:
        return False

    if hasattr(obj, "set_facing"):
        obj.set_facing(direction)

    dr, dc = DIR_DELTAS[direction]
    r, c = obj.position
    new_pos = (r + dr, c + dc)

    world.move_object(obj, new_pos)
    return True
