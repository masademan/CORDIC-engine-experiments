from cordic_sin import cordic_sin
from cordic_cos import cordic_cos
from cordic_engines import cordic_vectoring


def cordic_tan(degrees: int, refinements: int = 10, units_of_precision: int = 3) -> int:
    sin_result = cordic_sin(degrees=degrees, refinements=refinements, units_of_precision=units_of_precision)
    cos_result = cordic_cos(degrees=degrees, refinements=refinements, units_of_precision=units_of_precision)
    return int(sin_result[0] * 10**units_of_precision / cos_result[0])


def cordic_arctan(yx: int, refinements: int = 10, units_of_precision: int = 3) -> int:
    return cordic_vectoring(10**units_of_precision, yx, refinements, units_of_precision)


def cordic_arctan2(y: int, x: int, refinements: int = 10, units_of_precision: int = 3) -> int:
    if x == 0 and y == 0:
        return 0

    if y == 0:
        if x < 0:
            return 180 * 10**units_of_precision
        else:
            return 0

    offset = 0
    offset_sign = -1
    if y > 0:
        offset_sign = 1

    if x < 0:
        offset = 180
        y = -y

    return cordic_vectoring(x, y, refinements, units_of_precision) + offset * 10**units_of_precision * offset_sign
