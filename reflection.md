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

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
