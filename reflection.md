# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").
  the number was glitched when it said go lower for 4 i went 3 then it said go higher turns out number was 29 so the hints are switched
  also when i switech to easy the blute text never chaned saying only from 1 to 20 still says 1 to 100
  when i try to do new game it is stuck and does not change still says gamve over start new again


---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic's AI assistant) throughout this project to identify, explain, and fix bugs.

**Correct AI suggestion — swapped hint messages:**
The AI correctly identified that `check_guess` was returning "Go HIGHER!" when the guess was too high and "Go LOWER!" when the guess was too low — the exact backwards behavior I noticed when playing. It suggested swapping the two message strings inside the `if guess > secret` branches. I verified this by running `pytest tests/test_game_logic.py::test_too_high_message_says_go_lower` and confirming it passed, then tested manually in the live app by guessing a number I knew was too high and checking that the hint now correctly said "Go LOWER!".

**Incorrect/misleading AI suggestion — the starter test assertions:**
The AI's original starter tests compared the full return value of `check_guess` directly to a plain string like `assert result == "Win"`. This was misleading because `check_guess` returns a tuple `("Win", "🎉 Correct!")`, not just `"Win"`. Running pytest immediately showed all three starter tests failing with `AssertionError: assert ('Win', '...') == 'Win'`. I fixed each test by unpacking the tuple: `outcome, message = check_guess(...)` before asserting. This taught me that AI-generated tests need the same careful review as AI-generated code.

---

## 3. Debugging and testing your fixes

I decided a bug was truly fixed only when both a passing pytest test and a correct live-game interaction confirmed the new behavior.

For the swapped hint bug, I wrote `test_too_high_message_says_go_lower` which calls `check_guess(60, 50)` and asserts `"LOWER" in message`. Before the fix the test failed; after swapping the strings it passed. I ran the full suite with `pytest tests/ -v` and confirmed all 6 tests passed with no regressions.

For the blue-text range bug I verified it manually: switched to Easy in the sidebar and confirmed the banner changed from "1 and 100" to "1 and 20", then switched to Hard and saw "1 and 200". The AI helped design the targeted message-content tests by suggesting checking for the word "LOWER" or "HIGHER" inside the message string rather than comparing the full emoji-string exactly, which made the tests more readable and less brittle.

---

## 4. What did you learn about Streamlit and state?

The secret number kept changing because every time I clicked "Submit", Streamlit reran the entire script from top to bottom, and the original code called `random.randint()` at the top level with no guard. That meant a brand-new random number was picked on every interaction, so the target I was trying to guess literally changed each click.

A Streamlit "rerun" is like the app hitting refresh on itself every single time you interact with it — press a button, move a slider, or change a dropdown and the whole Python file runs again from line one. `st.session_state` is a special dictionary that survives those reruns, like a notepad that stays on the desk even when you flip to a new page. Once you store a value in `session_state`, it is still there the next time the script runs.

The fix was wrapping the `random.randint()` call in `if "secret" not in st.session_state:` so the number is only generated the very first time the app loads. After that, every rerun finds the key already in `session_state` and skips the random call entirely, keeping the secret stable for the whole game.

---

## 5. Looking ahead: your developer habits

One habit I want to keep is writing a pytest test immediately after fixing a bug — before moving on. Having that test act as a "regression guard" meant I could confidently make later changes to the code without worrying I had accidentally broken something that was already working. That test-first mindset is something I want to bring to every future lab.

Next time I work with AI on a coding task, I would read the AI's output line by line before running it instead of running first and debugging after. Several issues — like the tuple vs. string mismatch in the starter tests — would have been caught in a two-second visual review rather than a head-scratching debug session.

This project changed how I see AI-generated code: it is a fast first draft, not a finished answer. The AI is great at spotting patterns and suggesting structure, but it can confidently produce code that looks right and is subtly wrong, so treating every suggestion as "probably correct, needs one more check" is the right default attitude.
