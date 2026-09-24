"""Standalone MicroPython-friendly maths trainer for Casio fx-CG100."""

import math
import random
import time


HIGH_SCORE = 0


def now_ms():
    ticks_ms = getattr(time, "ticks_ms", None)
    if ticks_ms:
        return ticks_ms()
    return int(time.time() * 1000)


def elapsed_ms(start):
    ticks_diff = getattr(time, "ticks_diff", None)
    if ticks_diff:
        return ticks_diff(now_ms(), start)
    return now_ms() - start


def ask_int(prompt, minimum=None, maximum=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print("Must be at least", minimum)
            continue
        if maximum is not None and value > maximum:
            print("Must be at most", maximum)
            continue
        return value


def ask_float(prompt, minimum=None, maximum=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Enter a number.")
            continue
        if minimum is not None and value < minimum:
            print("Must be at least", minimum)
            continue
        if maximum is not None and value > maximum:
            print("Must be at most", maximum)
            continue
        return value


def close_enough(a, b, tolerance=0.05):
    return abs(a - b) <= tolerance * max(1.0, abs(b))


def algebra_question(level):
    a = random.randint(1, 2 + level)
    x = random.randint(-5 - level, 5 + level)
    b = random.randint(-10, 10)
    c = a * x + b
    return "Solve: %dx + %d = %d" % (a, b, c), float(x)


def indices_question(level):
    base = random.randint(2, min(4 + level, 9))
    m = random.randint(1, 2 + level)
    n = random.randint(1, 2 + level)
    return "Evaluate: %d^%d * %d^%d" % (base, m, base, n), float(base ** (m + n))


def surd_question(level):
    n = random.randint(2, 5 + level)
    return "Approximate sqrt(%d) to 2 d.p." % n, round(math.sqrt(n), 2)


def quadratics_question(level):
    r1 = random.randint(-4 - level, 4 + level)
    r2 = random.randint(-4 - level, 4 + level)
    s = r1 + r2
    p = r1 * r2
    return "For x^2 - (%d)x + (%d)=0, give sum of roots" % (s, p), float(s)


def gradient_question(level):
    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)
    x2 = x1
    while x2 == x1:
        x2 = random.randint(-5 - level, 5 + level)
    y2 = random.randint(-8 - level, 8 + level)
    m = (y2 - y1) / float(x2 - x1)
    return "Gradient through (%d,%d) and (%d,%d)" % (x1, y1, x2, y2), m


def complete_square_question(level):
    h = random.randint(-3 - level, 3 + level)
    k = random.randint(-10, 10)
    b = -2 * h
    c = h * h + k
    return "For x^2 + (%d)x + (%d), give completed-square h in (x-h)^2+k" % (b, c), float(h)


def simultaneous_question(level):
    x = random.randint(-5 - level, 5 + level)
    y = random.randint(-5 - level, 5 + level)
    a = random.randint(1, 4 + level)
    b = random.randint(1, 4 + level)
    c = a * x + b * y
    d = random.randint(1, 4 + level)
    e = random.randint(1, 4 + level)
    f = d * x + e * y
    return "Solve for x: %dx+%dy=%d and %dx+%dy=%d" % (a, b, c, d, e, f), float(x)


def probability_question(level):
    red = random.randint(2, 5 + level)
    blue = random.randint(2, 5 + level)
    total = red + blue
    return "P(red) from bag with %d red, %d blue" % (red, blue), red / float(total)


def calculus_question(level):
    a = random.randint(1, 4 + level)
    n = random.randint(2, 4 + level)
    x = random.randint(1, 3 + level)
    deriv = a * n * (x ** (n - 1))
    return "d/dx of %dx^%d at x=%d" % (a, n, x), float(deriv)


def linear_algebra_question(level):
    a = random.randint(-3 - level, 3 + level)
    b = random.randint(-3 - level, 3 + level)
    c = random.randint(-3 - level, 3 + level)
    d = random.randint(-3 - level, 3 + level)
    return "Determinant of [[%d,%d],[%d,%d]]" % (a, b, c, d), float(a * d - b * c)


def make_question(level):
    generators = [
        algebra_question,
        indices_question,
        surd_question,
        quadratics_question,
        gradient_question,
        complete_square_question,
        simultaneous_question,
        probability_question,
        calculus_question,
        linear_algebra_question,
    ]
    fn = random.choice(generators)
    return fn(level)


def mental_maths_mode():
    global HIGH_SCORE
    level = ask_int("Difficulty 1-3: ", 1, 3)
    rounds = ask_int("Rounds (3-20): ", 3, 20)
    limit = ask_int("Time per question in seconds (5-60): ", 5, 60)
    score = 0
    streak = 0
    print("\nMental maths starts. Enter q to quit round early.")
    for i in range(rounds):
        question, answer = make_question(level)
        print("\nQ%d/%d:" % (i + 1, rounds), question)
        start = now_ms()
        raw = input("Answer: ").strip()
        elapsed = elapsed_ms(start)
        if raw.lower() == "q":
            break
        if elapsed > limit * 1000:
            streak = 0
            print("Too slow (%.2fs). Correct answer:" % (elapsed / 1000.0), answer)
            continue
        try:
            guess = float(raw)
        except ValueError:
            streak = 0
            print("Invalid number. Correct answer:", answer)
            continue
        if close_enough(guess, answer):
            streak += 1
            gained = 1 + min(streak, 5)
            score += gained
            print("Correct! +%d points. Streak %d" % (gained, streak))
        else:
            streak = 0
            print("Incorrect. Correct answer:", answer)
    print("\nRound score:", score)
    if score > HIGH_SCORE:
        HIGH_SCORE = score
        print("New high score!", HIGH_SCORE)
    else:
        print("Session high score:", HIGH_SCORE)


def guess_graph_mode():
    scenarios = [
        {
            "desc": "f(x)=x^2-4x+3",
            "q": "How many real roots?",
            "a": 2,
        },
        {
            "desc": "f(x)=1/(x-2)",
            "q": "Vertical asymptote x=?",
            "a": 2,
        },
        {
            "desc": "f(x)=-x^2+6x-5",
            "q": "x-coordinate of turning point?",
            "a": 3,
        },
        {
            "desc": "f(x)=2x+1",
            "q": "y-intercept?",
            "a": 1,
        },
        {
            "desc": "f(x)=x^3",
            "q": "Increasing for x>0? (1 yes / 0 no)",
            "a": 1,
        },
    ]
    random.shuffle(scenarios)
    score = 0
    for item in scenarios:
        print("\nGraph clue:", item["desc"])
        guess = ask_float(item["q"] + " ")
        if close_enough(guess, float(item["a"])):
            score += 1
            print("Correct")
        else:
            print("Expected:", item["a"])
    print("Guess-the-graph score:", score, "/", len(scenarios))


def graph_to_function_mode():
    print("\nGraph-to-function mode")
    presets = [
        {"points": [(-1, 1), (0, 0), (1, 1)], "func": "x^2"},
        {"points": [(-1, -2), (0, 1), (1, 4)], "func": "3x+1"},
        {"points": [(-2, 0), (0, -2), (2, 0)], "func": "0.5x^2-2"},
        {"points": [(-2, -0.5), (0, 0), (2, 0.5)], "func": "x/4"},
    ]
    sample = random.choice(presets)
    print("Sample points:")
    for x, y in sample["points"]:
        print("(", x, ",", y, ")", sep="")
    guess = input("Best matching function? ").strip().lower().replace(" ", "")
    expected = sample["func"].lower().replace(" ", "")
    if guess == expected:
        print("Nice! exact match.")
    else:
        print("Suggested function:", sample["func"])


def main():
    while True:
        print("\n=== CG100 Maths Trainer ===")
        print("1) Mental maths")
        print("2) Guess-the-graph")
        print("3) Graph-to-function")
        print("4) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            mental_maths_mode()
        elif choice == "2":
            guess_graph_mode()
        elif choice == "3":
            graph_to_function_mode()
        elif choice == "4":
            print("Goodbye")
            return
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
