import numpy as np
import pandas as pd


def f1(x, y):
    return 2 * x + 3 * y


def g1(x, y):
    return 3 * x + 2 * y


def real_f1(t):
    return np.exp(-t) * 0.5 + np.exp(5 * t) * 0.5


def real_g1(t):
    return -np.exp(-t) * 0.5 + np.exp(5 * t) * 0.5


def f2(x, y):
    return x + 5 * y


def g2(x, y):
    return -x - 3 * y


def real_f2(t):
    return 5 * np.exp(-t) * (np.cos(t) + 6 * np.sin(t))


def real_g2(t):
    return np.exp(-t) * (4 * np.cos(t) - 13 * np.sin(t))


def f3(x, y):
    return x + 3 * y


def g3(x, y, t):
    return x - y + 2 * np.exp(t)


def real_f3(t):
    return -np.exp(-2*t) + 3*np.exp(2*t) - 2*np.exp(t)


def real_g3(t):
    return np.exp(-2*t) + np.exp(2*t)


def B(B, T):
    return B*(10-B-T)


def T(B, T):
    return T*(15-B-3*T)