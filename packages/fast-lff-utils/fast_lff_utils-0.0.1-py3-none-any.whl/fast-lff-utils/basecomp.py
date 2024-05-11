from enum import unique, IntEnum
import logging
import os


class StateChangeError(Exception):
    """ Error for recognizing an illegal state change"""
    pass


@unique
class State(IntEnum):
    """ Defines several states.
    """

    STOPPED = 0
    SETUP = 1
    RUNNING = 2
    ERROR = 3


class BaseComponent:
    """ Defines the structure for a basic component with a state machine.

    :param name: Name of component. This is used for the identification in logging
    :type name: str

    """

    def __init__(self, name: str, shm: dict, logger: logging.Logger):
        """ Constructor method
        """

        self.__name: str = name
        self.__state: State = State.STOPPED
        self.logger: logging.Logger = logger


    def setup(self) -> None:
        """ Represents a dummy method for setting up a Component.

        """
        pass

    def run(self) -> None:
        """ Represents a dummy method for running a Component.
        """
        pass

    def start(self) -> None:
        """ Defines start-up routine based on `setup()` and `run()` methods.

        :return: None
        :rtype: None

        """
        try:
            self.state = State.BOOT
            self.setup()
            self.run()

        except StateChangeError:
            self.set_error()

    def stop(self) -> None:
        """ Defines a stop routine for the Component

        :return: None
        :rtype: None

        """
        self.state = State.STOPPED

    @property
    def state(self) -> State:
        """ Returns the current State of the Component.

        :return: current State
        :rtype: State

        """

        return self.__state

    @state.setter
    def state(self, state: State) -> None:
        """ Applies the given State `state` if permitted.

        :param state: State that should be set
        :type state: State

        :return: None
        :rtype: None
        :raise StateChangeError: State change is not permitted

        """

        old_state: State = self.state

        if self.state == state:
            return

        elif state == State.ERROR:
            self.set_error()

        elif self.is_state_change_valid(state):
            self.__state = state

            self.logger.debug(f"State change from '{old_state.name}' to '{self.state.name}'")

        else:
            msg = (f"State change from {self.state.name} to {state.name} is not permitted.")
            self.logger.error(msg)
            raise StateChangeError(msg)

    def set_error(self, msg: str = ""):
        """ Changes the current state to State.ERROR

        :return: None
        :rtype: None

        """

        if self.state == State.ERROR:
            self.logger.warning("set_error() was already called")
            return

        self.__state = State.ERROR
        self.logger.critical(f"{msg}")

    @property
    def name(self) -> str:
        """ Returns the name of the Component

        :return: Name of the Component
        :rtype: str

        """
        return self.__name

    def is_state_change_valid(self, state: State) -> bool:
        """ Returns `True` if the requested state change is valid, otherwise `False`.

        This methods checks if the requested State `state` can be applied to the :class:`Component`.

        :return: `True` if the request is valid, otherwise `False`
        :rtype: bool
        """

        is_state_change_valid = (
            (self.state == State.STOPPED and state == State.SETUP)
            or (self.state == State.SETUP and state == State.RUNNING)
            or (self.state == State.RUNNING and state == State.SETUP)
            or (self.state == State.ERROR and state == State.STOPPED)
        )
    
        return True if is_state_change_valid is True else False
