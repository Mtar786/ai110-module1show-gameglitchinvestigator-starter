from logic_utils import check_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Tests targeting the two bugs fixed in Phase 2 ---

def test_too_high_message_says_go_lower():
    # Bug 2 fix: when guess is too high, message must say Go LOWER, not Go HIGHER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message but got: {message}"


def test_too_low_message_says_go_higher():
    # Bug 2 fix: when guess is too low, message must say Go HIGHER, not Go LOWER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message but got: {message}"


def test_integer_secret_always_comparable():
    # Bug 3 fix: check_guess with an integer secret never raises TypeError
    # and always returns the correct outcome regardless of attempt number
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

    outcome, _ = check_guess(51, 50)
    assert outcome == "Too High"

    outcome, _ = check_guess(49, 50)
    assert outcome == "Too Low"
