import pytest
from backend.app.game_logic import Game

@pytest.fixture
def game():
    g = Game(["Alice", "Bob"])
    g.start()
    return g

def test_income(game):
    first = game.current_player()
    coins_before = first.coins
    game.income()
    assert first.coins == coins_before + 1

def test_coup(game):
    game.current_player().coins = 7
    game.coup(1)
    assert not game.players[1].alive