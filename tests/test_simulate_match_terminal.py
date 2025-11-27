from tournament import simulate_match

def test_simulate_match_terminal_returns_bool():
    result = simulate_match("Real Madrid", "Barcelona")
    assert isinstance(result, bool)
