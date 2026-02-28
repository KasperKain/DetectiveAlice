class BaseScreen:

    accept_commands = False
    accept_arrows = False
    accept_any = False

    def __init__(self):
        self.command_buffer = ""
        self.should_quit = False

    def update(self):
        pass

    def update_objects(self):
        pass

    def render(self):
        raise NotImplementedError

    def handle_command(self, cmd: str):
        pass

    def handle_arrow(self, direction: str):
        pass

    def handle_any_key(self, key):
        pass

    # need this to store inputs
    def add_char_to_buffer(self, ch: str):
        pass
