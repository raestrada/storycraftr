class DebugState:
    """
    A class to manage the global debug state for the application.

    Attributes:
        debug (bool): Indicates whether debug mode is active.
    """

    def __init__(self):
        """
        Initializes the DebugState instance with debug mode set to False by default.
        """
        self._debug = False

    def set_debug(self, value: bool):
        """
        Sets the debug state to the specified value.

        Args:
            value (bool): True to enable debug mode, False to disable it.
        """
        self._debug = value

    def is_debug(self) -> bool:
        """
        Returns the current debug state.

        Returns:
            bool: True if debug mode is enabled, False otherwise.
        """
        return self._debug


# Singleton to manage global debug state
debug_state = DebugState()
# Test
