"""Reaction time game for Casio fx-CG100 MicroPython."""

import random
import time


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


def pause_seconds(seconds):
    sleep_ms = getattr(time, "sleep_ms", None)
    if sleep_ms:
        sleep_ms(int(seconds * 1000))
    else:
        time.sleep(seconds)


def run_round(round_index):
    print("\nRound", round_index)
    print("Get ready... wait for GO, then press Enter.")
    input("Press Enter to arm this round: ")

    wait_time = random.uniform(1.5, 4.5)
    false_start_window = random.uniform(0.2, 0.8)
    print("Do NOT press Enter yet...")
    pause_seconds(false_start_window)
    early = input("False start check (leave blank if waiting): ").strip()
    if early == "":
        pause_seconds(wait_time - false_start_window)
    else:
        print("False start detected! Round disqualified.")
        return None

    print("GO!")
    start = now_ms()
    input("Press Enter now! ")
    result = elapsed_ms(start)
    print("Reaction time:", result, "ms")
    return result


def session_summary(results):
    if not results:
        print("No valid rounds recorded.")
        return
    best = min(results)
    avg = sum(results) / float(len(results))
    print("\nSession results")
    print("Valid rounds:", len(results))
    print("Best:", int(best), "ms")
    print("Average:", int(avg), "ms")


def main():
    print("=== Reaction Time Trainer ===")
    all_results = []
    round_index = 1
    while True:
        result = run_round(round_index)
        if result is not None:
            all_results.append(result)
        again = input("Play another round? (y/n): ").strip().lower()
        if again != "y":
            break
        round_index += 1
    session_summary(all_results)
    print("Goodbye")


if __name__ == "__main__":
    main()
