def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Hard was returning 1,50 which is easier than Normal (1,100). AI identified
        # the ranges were backwards; changed to 1,200 so Hard is genuinely harder.
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        # FIX: Original messages were swapped — "Go HIGHER!" appeared when guess was too high.
        # AI flagged the bug in check_guess; fixed by swapping the hint strings.
        return "Too High", "📉 Go LOWER!"
    else:
        # FIX: Same swap bug — "Go LOWER!" appeared when guess was too low.
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIX: Original code added +5 points on even attempts for wrong guesses.
        # AI caught the even/odd branch rewarding incorrect guesses; removed it so
        # Too High always deducts 5, same as Too Low.
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
