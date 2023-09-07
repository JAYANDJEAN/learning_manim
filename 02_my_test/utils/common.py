import numpy as np

a = 5.0
b = 3.0
c = 4.0
time_gap = 2


def get_slope_out(k_i, k_n):
    return (2 * k_n - k_i + k_i * np.square(k_n)) / (1 + 2 * k_n * k_i - np.square(k_n))


# ellipse
def get_ellipse_y(x):
    return np.sqrt((1 - np.square(x) / np.square(a)) * np.square(b))


def get_ellipse_slope_n(x, y):
    return y * np.square(a) / x / np.square(b)


def get_ellipse_another_point(x0, y0, k):
    A = (np.square(k) / np.square(b) + 1 / np.square(a))
    B = (2 * k * y0 - 2 * np.square(k) * x0) / np.square(b)
    C = (k * x0 - y0) * (k * x0 - y0) / np.square(b) - 1
    x1 = (-B - np.sqrt(np.square(B) - 4 * A * C)) / 2 / A
    x2 = (-B + np.sqrt(np.square(B) - 4 * A * C)) / 2 / A
    x_p = x2 if np.abs(x1 - x0) < np.abs(x2 - x0) else x1
    y_p = y0 + k * (x_p - x0)
    return x_p, y_p


def get_ellipse_reflection_line(x0, y0, x1, y1):
    k_i = (y1 - y0) / (x1 - x0)
    k_n = get_ellipse_slope_n(x1, y1)
    k_o = get_slope_out(k_i, k_n)
    x2, y2 = get_ellipse_another_point(x1, y1, k_o)
    return x2, y2



