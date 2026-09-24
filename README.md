# CG100-Games

MicroPython programs for the Casio fx-CG100.

## Files in this repository

- `maths_trainer.py`
  - Menu-driven maths revision tool.
  - Includes mental maths rounds (difficulty levels, per-question time limit, streak scoring, session high score).
  - Includes guess-the-graph prompts (roots, asymptotes, intercepts, turning points, monotonic behaviour).
  - Includes graph-to-function matching from sample points (text fallback representation).

- `matrix_vector_visualiser.py`
  - Matrix addition and matrix multiplication.
  - Determinants for 2x2 and 3x3 matrices.
  - Solver for 2x2 simultaneous linear equations.
  - 2D vector operations (addition, subtraction, dot product, magnitude).
  - 2D transforms (rotation, reflections, stretches).
  - 3D vector operations (addition, dot product, cross product).
  - Includes an ASCII/text graphics fallback hint.

- `reaction_time.py`
  - Reaction-time game with random delay before "GO".
  - False-start detection.
  - Reaction measurement in milliseconds.
  - Tracks best and average valid times over the session.
  - Supports repeat rounds and clean exit.

- `projectile_game.py`
  - Projectile simulation with configurable speed, angle and start height.
  - Supports random target generation or manual target entry.
  - Computes trajectory using constant gravity.
  - Reports hit/miss and closest approach.
  - Includes replay loop and ASCII trajectory fallback.

## Running on a Casio fx-CG100

1. Connect the calculator to your computer via USB.
2. Open storage mode on the calculator.
3. Copy one or more `.py` files from this repository onto the calculator storage.
4. Open the calculator MicroPython app.
5. Select the program file and run it.

Each script is standalone and can be run independently.

## Controls and interaction style

- Input is text-based through `input()` prompts.
- Most menus use numbered choices.
- Enter numeric values when requested; defensive validation is included.
- Type `y` / `n` when prompted for replay/continuation.

## MicroPython assumptions

- Uses conservative standard-library features expected in MicroPython.
- Uses `time.ticks_ms` / `time.ticks_diff` when available, with desktop-compatible fallback.
- Avoids external packages and desktop-only GUI APIs.

## Graphics fallback and limitations

- Programs are designed to run in text mode.
- Where visual output is helpful, simple ASCII fallback is used.
- This is intentionally calculator-friendly, so plotting is approximate and not a full graphing engine.
- Randomly generated practice content is broad but not exhaustive for every syllabus variant.
