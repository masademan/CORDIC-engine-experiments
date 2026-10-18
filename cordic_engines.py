import math

def get_A(refinements: int, units_of_precision: int) -> tuple[list[float], list[int]]:
    TRUE_A = []
    A = []
    for i in range(refinements - 1):
        a_i = math.atan(1 / 2**i)
        a_i_deg = a_i * 180 / math.pi
        TRUE_A.append(a_i_deg)
        A.append(round(a_i_deg * 10**units_of_precision))

    return TRUE_A, A

def get_K(refinements: int, units_of_precision: int) -> tuple[float, int]:
    TRUE_K = 1
    for i in range(refinements - 1):
        a_i = math.atan(1 / 2**i)
        TRUE_K *= math.cos(a_i)

    K = round(TRUE_K * 10**units_of_precision)

    return TRUE_K, K


def format_deg(degrees: int) -> int:
    temp_deg = abs(degrees) % 360

    if temp_deg > 180:
        temp_deg -= 360

    if degrees < 0:
        return -temp_deg
    return temp_deg


def cordic_rotation(
    degrees: int, refinements: int = 10, units_of_precision: int = 3
) -> tuple[int, int, int]:
    """
    Takes in degrees as an input and outputs x and y when a unit vector is rotated by degrees degrees
    x and y are the answer multiplied by 10^units_of_precision and then made an int
    """

    # CONSTANT VALS
    _, A = get_A(refinements, units_of_precision)
    _, K = get_K(refinements, units_of_precision)

    x = 1 * 10**units_of_precision
    y = 0

    if degrees != 0:
        degrees = format_deg(degrees) * 10**units_of_precision

    if degrees == 0:
        return x, y, 0

    curr_deg = 0

    for i in range(refinements):
        sign = 1
        if curr_deg > degrees:
            sign = -1

        new_x = x - (y >> i) * sign
        new_y = y + (x >> i) * sign
        if i < refinements - 1:
            curr_deg += A[i] * sign

        x = new_x
        y = new_y

    return x * K // 10**units_of_precision, y * K // 10**units_of_precision, curr_deg


def cordic_vectoring(
    x: int, y: int, refinements: int = 10, units_of_precision: int = 3
) -> int:
    """
    Takes in x and y as inputs and outputs the number of degrees that vector was rotated by
    x and y are the coords of the true vector multiplied by 10^units_of_precision and then made an int
    does do x = abs(x) to make the function solvable, so make sure to negate x if necessary before this function
    """

    # CONSTANT VALS
    _, A = get_A(refinements, units_of_precision)

    x = abs(x)

    curr_deg = 0

    for i in range(refinements):
        sign = 1
        if y < 0:
            sign = -1

        new_x = x + (y >> i) * sign
        new_y = y - (x >> i) * sign
        if i < refinements - 1:
            curr_deg += A[i] * sign

        x = new_x
        y = new_y

    return curr_deg
