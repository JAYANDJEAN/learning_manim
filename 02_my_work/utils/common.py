import numpy as np

a = 5
b = 3
c = 4
r = 3
time_gap = 2


def get_slope_out(k_i, k_n):
    return (2 * k_n - k_i + k_i * np.square(k_n)) / (1 + 2 * k_n * k_i - np.square(k_n))


# ellipse
def get_y(x, long, short):
    return np.sqrt((1 - np.square(x) / np.square(long)) * np.square(short))


def get_slope_normal(x, y, long, short):
    return y * np.square(long) / x / np.square(short)


def get_dual_point(x0, y0, k, long, short):
    A = (np.square(k) / np.square(short) + 1 / np.square(long))
    B = (2 * k * y0 - 2 * np.square(k) * x0) / np.square(short)
    C = (k * x0 - y0) * (k * x0 - y0) / np.square(short) - 1
    discriminant = np.square(B) - 4 * A * C
    x1 = (-B - np.sqrt(discriminant)) / 2 / A
    x2 = (-B + np.sqrt(discriminant)) / 2 / A
    x_p = x2 if np.abs(x1 - x0) < np.abs(x2 - x0) else x1
    y_p = y0 + k * (x_p - x0)
    return x_p, y_p


def get_reflection_line(x0, y0, x1, y1, long, short):
    k_i = (y1 - y0) / (x1 - x0)
    k_n = get_slope_normal(x1, y1, long, short)
    k_o = get_slope_out(k_i, k_n)
    x2, y2 = get_dual_point(x1, y1, k_o, long, short)
    return x2, y2
