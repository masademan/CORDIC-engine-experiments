from cordic_engines import cordic_rotation, cordic_vectoring, format_deg


def cordic_cos(
    degrees: int, refinements: int = 10, units_of_precision: int = 3
) -> tuple[int, int]:
    sign = 1
    new_deg = format_deg(degrees)
    if new_deg > 90:
        new_deg = 180 - new_deg
        sign = -1
    elif new_deg < -90:
        new_deg = -180 - new_deg
        sign = -1

    cos_result = cordic_rotation(new_deg, refinements, units_of_precision)

    return cos_result[0] * sign, cos_result[2]


def cordic_arccos(x: int, refinements: int = 10, units_of_precision: int = 3) -> int:
    arccos_deg = cordic_vectoring(x, int((10 ** (2 * units_of_precision) - x**2) ** 0.5), refinements, units_of_precision)
    if x < 0:
        arccos_deg = 180 * 10**units_of_precision - arccos_deg

    return arccos_deg
