# debug_state.py


class DebugState:
    def __init__(self):
        self.debug = False

    def set_debug(self, value: bool):
        self.debug = value

    def is_debug(self) -> bool:
        return self.debug


# Singleton para almacenar el estado global
debug_state = DebugState()
