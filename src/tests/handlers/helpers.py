
from unittest import mock

from todolist.states import UserInputStates


def assert_state_entrypoint(state: mock.Mock):
    state.clear.assert_called_once()
    state.set_state.assert_called_once()

def assert_state_endpoint(state: mock.Mock):
    state.clear.assert_called_once()

def assert_register_handled(state: mock.Mock, answer_to: mock.Mock):
    state.set_state.assert_called_once_with(UserInputStates.name)
    answer_to.assert_called_once_with("Send me your name:")
