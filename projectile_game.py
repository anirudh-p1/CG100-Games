"""Projectile challenge game for Casio fx-CG100 MicroPython."""

import math
import random


G = 9.81


def ask_float(prompt, minimum=None):
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
        return value


def configure_target():
    mode = input("Random target? (y/n): ").strip().lower()
    if mode == "n":
        tx = ask_float("Target x (m): ", 1.0)
        ty = ask_float("Target y (m): ", 0.0)
        return tx, ty
    tx = random.uniform(20.0, 80.0)
    ty = random.uniform(0.0, 25.0)
    print("Target generated at x=%.1fm, y=%.1fm" % (tx, ty))
    return tx, ty


def sample_trajectory(speed, angle_deg, start_h, steps=120):
    angle = angle_deg * math.pi / 180.0
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)
    samples = []
    if vx <= 0:
        return samples
    t_max = max(0.5, (vy + math.sqrt(max(vy * vy + 2 * G * start_h, 0.0))) / G)
    for i in range(steps + 1):
        t = t_max * i / float(steps)
        x = vx * t
        y = start_h + vy * t - 0.5 * G * t * t
        samples.append((x, y))
        if y < 0 and i > 0:
            break
    return samples


def closest_approach(samples, tx, ty):
    best_d = None
    best_point = (0.0, 0.0)
    for x, y in samples:
        d = math.sqrt((x - tx) ** 2 + (y - ty) ** 2)
        if best_d is None or d < best_d:
            best_d = d
            best_point = (x, y)
    return best_d, best_point


def render_ascii(samples, tx, ty, width=50, height=14):
    max_x = max([tx] + [p[0] for p in samples] + [1.0])
    max_y = max([ty] + [p[1] for p in samples] + [1.0])
    grid = [[" " for _ in range(width)] for _ in range(height)]

    def to_grid(x, y):
        gx = int((x / max_x) * (width - 1))
        gy = height - 1 - int((y / max_y) * (height - 1))
        return gx, gy

    for x, y in samples:
        if y < 0:
            continue
        gx, gy = to_grid(x, y)
        if 0 <= gx < width and 0 <= gy < height:
            grid[gy][gx] = "*"

    tgx, tgy = to_grid(tx, ty)
    if 0 <= tgx < width and 0 <= tgy < height:
        grid[tgy][tgx] = "T"

    print("\nASCII trajectory (* = path, T = target)")
    for row in grid:
        print("".join(row))


def run_round():
    print("\n=== Projectile Round ===")
    speed = ask_float("Launch speed m/s (>=1): ", 1.0)
    angle = ask_float("Launch angle degrees (1-89): ", 1.0)
    if angle >= 89:
        angle = 89.0
    start_h = ask_float("Starting height m (>=0): ", 0.0)
    tx, ty = configure_target()

    samples = sample_trajectory(speed, angle, start_h)
    if not samples:
        print("Invalid launch settings for trajectory.")
        return

    miss_distance, point = closest_approach(samples, tx, ty)
    hit = miss_distance <= 2.0
    print("Target:", (round(tx, 2), round(ty, 2)))
    print("Closest approach point:", (round(point[0], 2), round(point[1], 2)))
    print("Closest distance: %.2f m" % miss_distance)
    if hit:
        print("HIT! Great shot.")
    else:
        print("MISS. Adjust speed/angle and try again.")

    render_ascii(samples, tx, ty)


def main():
    while True:
        run_round()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye")
            break


if __name__ == "__main__":
    main()
