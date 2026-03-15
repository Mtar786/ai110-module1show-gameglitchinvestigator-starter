# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:**
A number-guessing game where the player picks a difficulty (Easy 1–20, Normal 1–100, Hard 1–200), then guesses the secret number. Each wrong guess deducts 5 points from a starting score of 100 and shows a directional hint (Go HIGHER / Go LOWER). Guessing correctly ends the game with a win screen; running out of attempts ends it with a loss.

**Bugs found:**
1. **Swapped hints** — "Go HIGHER!" appeared when the guess was too high and "Go LOWER!" when it was too low. The `check_guess` return strings were reversed.
2. **Unstable secret number** — The secret was regenerated on every button click because `random.randint()` ran at the top level of the script with no `session_state` guard, so Streamlit's rerun mechanism kept changing it.
3. **Wrong difficulty ranges** — Hard was set to 1–50 (easier than Normal), and the blue info banner always displayed "1 and 100" regardless of the chosen difficulty.
4. **Score rewarded wrong guesses** — An even/odd branch inside `calculate_score` added +5 points on even-numbered wrong guesses instead of always subtracting.
5. **New Game did not reset properly** — The attempts counter initialised at 1 instead of 0, and the New Game button used a hardcoded range instead of respecting the current difficulty.
6. **Type-switching secret** — On even-numbered attempts the secret was cast to a `str`, causing numeric comparisons to silently fail and making the game unwinnable.

**Fixes applied:**
- Swapped the hint strings in `check_guess` inside `logic_utils.py`.
- Guarded `random.randint()` with `if "secret" not in st.session_state:` in `app.py`.
- Corrected all difficulty ranges in `get_range_for_difficulty` and wired the banner text to the same function.
- Removed the even/odd scoring branch; all wrong guesses now deduct 5.
- Unified the attempts initialisation to 0 and passed `low`/`high` to New Game's reset.
- Removed the string-cast of the secret so comparisons are always numeric.
- Refactored all game logic into `logic_utils.py` and updated `app.py` imports.
- Added targeted `pytest` cases for each fix; all 6 tests pass.

## 📸 Demo

![Fixed game winning screen](assets/demo_win.png)

> **Note:** Run `python -m streamlit run app.py`, select a difficulty, and guess the secret number shown in the "Developer Debug Info" expander to reproduce a win locally.

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
