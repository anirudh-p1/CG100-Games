"""Matrix and vector visualiser with text-mode fallback for CG100 MicroPython."""

import math


def ask_float(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def ask_int(prompt, minimum=None, maximum=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print("Minimum is", minimum)
            continue
        if maximum is not None and value > maximum:
            print("Maximum is", maximum)
            continue
        return value


def read_matrix(rows, cols, name):
    print("Enter matrix", name)
    matrix = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(ask_float("%s[%d,%d]: " % (name, r + 1, c + 1)))
        matrix.append(row)
    return matrix


def show_matrix(matrix, name="Result"):
    print(name + ":")
    for row in matrix:
        print(" ".join("%8.3f" % value for value in row))


def add_matrices():
    rows = ask_int("Rows (2-3): ", 2, 3)
    cols = ask_int("Cols (2-3): ", 2, 3)
    a = read_matrix(rows, cols, "A")
    b = read_matrix(rows, cols, "B")
    result = [[a[r][c] + b[r][c] for c in range(cols)] for r in range(rows)]
    show_matrix(result)


def multiply_matrices():
    r1 = ask_int("Rows in A (2-3): ", 2, 3)
    c1 = ask_int("Cols in A (2-3): ", 2, 3)
    r2 = c1
    print("Rows in B fixed at", r2, "for multiplication")
    c2 = ask_int("Cols in B (2-3): ", 2, 3)
    a = read_matrix(r1, c1, "A")
    b = read_matrix(r2, c2, "B")
    result = []
    for r in range(r1):
        row = []
        for c in range(c2):
            total = 0.0
            for k in range(c1):
                total += a[r][k] * b[k][c]
            row.append(total)
        result.append(row)
    show_matrix(result)


def determinant_2x2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def determinant_3x3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def determinant_menu():
    size = ask_int("Determinant size (2 or 3): ", 2, 3)
    m = read_matrix(size, size, "M")
    if size == 2:
        det = determinant_2x2(m)
    else:
        det = determinant_3x3(m)
    print("det(M) =", det)


def solve_2x2_simultaneous():
    print("Solve ax + by = e and cx + dy = f")
    a = ask_float("a: ")
    b = ask_float("b: ")
    c = ask_float("c: ")
    d = ask_float("d: ")
    e = ask_float("e: ")
    f = ask_float("f: ")
    det = a * d - b * c
    if abs(det) < 1e-9:
        print("No unique solution (determinant is 0).")
        return
    x = (e * d - b * f) / det
    y = (a * f - e * c) / det
    print("x =", x)
    print("y =", y)


def read_vector(size, name="v"):
    vec = []
    for i in range(size):
        vec.append(ask_float("%s[%d]: " % (name, i + 1)))
    return vec


def show_vector(vec, name="Result"):
    print(name + ":", "(" + ", ".join("%.3f" % x for x in vec) + ")")


def vector_2d_ops():
    v = read_vector(2, "v")
    w = read_vector(2, "w")
    show_vector([v[0] + w[0], v[1] + w[1]], "v+w")
    show_vector([v[0] - w[0], v[1] - w[1]], "v-w")
    dot = v[0] * w[0] + v[1] * w[1]
    mag_v = math.sqrt(v[0] ** 2 + v[1] ** 2)
    print("v·w =", dot)
    print("|v| =", mag_v)


def transform_2d():
    v = read_vector(2, "v")
    print("1) Rotate   2) Reflect x-axis   3) Reflect y-axis   4) Stretch")
    choice = input("Select transform: ").strip()
    if choice == "1":
        degrees = ask_float("Angle degrees: ")
        radians = degrees * math.pi / 180.0
        c = math.cos(radians)
        s = math.sin(radians)
        out = [v[0] * c - v[1] * s, v[0] * s + v[1] * c]
        show_vector(out, "Rotated")
    elif choice == "2":
        show_vector([v[0], -v[1]], "Reflected")
    elif choice == "3":
        show_vector([-v[0], v[1]], "Reflected")
    elif choice == "4":
        sx = ask_float("Stretch x scale: ")
        sy = ask_float("Stretch y scale: ")
        show_vector([v[0] * sx, v[1] * sy], "Stretched")
    else:
        print("Invalid selection")


def vector_3d_ops():
    v = read_vector(3, "v")
    w = read_vector(3, "w")
    dot = v[0] * w[0] + v[1] * w[1] + v[2] * w[2]
    cross = [
        v[1] * w[2] - v[2] * w[1],
        v[2] * w[0] - v[0] * w[2],
        v[0] * w[1] - v[1] * w[0],
    ]
    show_vector([v[0] + w[0], v[1] + w[1], v[2] + w[2]], "v+w")
    print("v·w =", dot)
    show_vector(cross, "v×w")


def ascii_plane_hint():
    print("\nSimple 2D text plane")
    print("  y")
    print("  ^")
    print("  |   .")
    print("--+--------> x")
    print("  |")


def main():
    while True:
        print("\n=== Matrix & Vector Visualiser ===")
        print("1) Matrix addition")
        print("2) Matrix multiplication")
        print("3) Determinant (2x2/3x3)")
        print("4) Solve 2x2 simultaneous equations")
        print("5) 2D vector operations")
        print("6) 2D transforms")
        print("7) 3D vector operations")
        print("8) Show ASCII graphics fallback")
        print("9) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_matrices()
        elif choice == "2":
            multiply_matrices()
        elif choice == "3":
            determinant_menu()
        elif choice == "4":
            solve_2x2_simultaneous()
        elif choice == "5":
            vector_2d_ops()
        elif choice == "6":
            transform_2d()
        elif choice == "7":
            vector_3d_ops()
        elif choice == "8":
            ascii_plane_hint()
        elif choice == "9":
            print("Goodbye")
            return
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
