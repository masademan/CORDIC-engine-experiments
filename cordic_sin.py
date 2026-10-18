from cordic_engines import cordic_rotation, cordic_vectoring, format_deg


def cordic_sin(degrees: int, refinements: int = 10, units_of_precision: int = 3) -> tuple[int, int]:
    new_deg = format_deg(degrees)
    if new_deg > 90:
        new_deg = 180 - new_deg
    elif new_deg < -90:
        new_deg = -180 - new_deg

    sin_result = cordic_rotation(new_deg, refinements, units_of_precision)

    return sin_result[1], sin_result[2]


def cordic_arcsin(y: int, refinements: int = 10, units_of_precision: int = 3) -> int:
    return cordic_vectoring(int((10 ** (2 * units_of_precision) - y**2) ** 0.5), y, refinements, units_of_precision)
