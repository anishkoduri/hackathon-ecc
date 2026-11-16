"""Scratch fixture for the /test-coverage Steps 1-2 exercise (dry-run #40 Leg 5)."""

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        raise ValueError("divide by zero")
    return a / b

def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x

def untested_helper(x):
    # deliberately untested: exercises the below-80% listing
    if x > 100:
        return "big"
    elif x < 0:
        return "neg"
    return "mid"
