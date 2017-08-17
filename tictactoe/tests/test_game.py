from pytest import fixture
from tictactoe.game import TicTacToe

# TODO: Write all of the tests...


@fixture
def create_game():
    return TicTacToe()


@fixture
def create_player():
    return TicTacToe.Player('x')


def test_TicTacToe_game_status(create_game, create_player):
    assert create_game.game_status(create_player) == 0  # there are moves left
