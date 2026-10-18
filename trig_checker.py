import math
from cordic_sin import cordic_sin, cordic_arcsin
from cordic_cos import cordic_cos, cordic_arccos
from cordic_engines import format_deg, get_A, get_K
from cordic_tan import cordic_tan, cordic_arctan, cordic_arctan2
from typing import Callable


def string_format_num_list(list: list[float | int], do_decimals: bool = True) -> None:
    stringed_items = []

    for item in list:
        if do_decimals:
            stringed_items.append(f"{item:.5f}")
        else:
            stringed_items.append(str(item))

    return f"[{", ".join(stringed_items)}]"


def test_trig_funcs(
    cordic_funcs: list[Callable],
    real_funcs: list[Callable],
    max_error: float = 0.005,
    refinements: int = 17,
    units_of_precision: int = 3,
    print_test_status: bool = True,
) -> None:
    deg_tests = [
        -360,
        -315,
        -270,
        -225,
        -180,
        -135,
        -90,
        -60,
        -45,
        -30,
        0,
        30,
        45,
        60,
        90,
        135,
        180,
        225,
        270,
        315,
        360,
    ]

    all_func_passed_tests = 0
    tests_skipped = 0

    for cordic_func, real_func in zip(cordic_funcs, real_funcs):
        if print_test_status:
            print(f"Testing {cordic_func.__name__}:")

        max_func_error = 0
        max_deg_error = 0
        passed_tests = 0
        for deg_test in deg_tests:
            is_tan_func = "tan" in cordic_func.__name__.lower()
            if is_tan_func:
                if abs(deg_test) in {90, 270}:
                    tests_skipped += 1
                    continue

            cordic_func_result = cordic_func(deg_test, refinements, units_of_precision)
            if is_tan_func:
                approximate_val = cordic_func_result / 10**units_of_precision
            else:
                approximate_val = cordic_func_result[0] / 10**units_of_precision
            true_val = real_func(deg_test * math.pi / 180)
            func_error = abs(true_val - approximate_val)
            max_func_error = max(max_func_error, func_error)
            if not is_tan_func:
                deg_error = (
                    abs(cordic_func_result[1] - format_deg(deg_test) * 10**units_of_precision) // 10**units_of_precision
                ) % 360
                max_deg_error = max(deg_error, max_deg_error)
            if func_error <= max_error:
                passed_tests += 1

            if print_test_status:
                print(
                    f"   {"PASS" if func_error <= max_error else "FAIL"}  {cordic_func.__name__}({deg_test:4d}) = {approximate_val:.5f}   {" " if approximate_val >= 0 else ""}"
                    f"{real_func.__name__}({deg_test:4d}) = {true_val:.5f}   {" " if true_val >= 0 else ""}func error: {func_error:.5f}     "
                    f"{f"deg reached: {cordic_func_result[1]//10**units_of_precision:4d}     deg error: {deg_error}" if not is_tan_func else ""}"
                )

        all_func_passed_tests += passed_tests
        print(
            f"{cordic_func.__name__} testing complete. Passed {passed_tests}/{len(deg_tests) - tests_skipped}. Max {cordic_func.__name__} error of {max_func_error:.5f}, max error allowed {max_error}."
            f" {f"Max deg error: {max_deg_error}" if not is_tan_func else ""}"
        )
        if print_test_status:
            print()

    if not print_test_status:
        print()

    num_tests = len(deg_tests) * len(cordic_funcs) - tests_skipped
    if all_func_passed_tests == num_tests:
        print(f"All {num_tests} tests passed! These functions have good settings and are implemented correctly")
    else:
        print(
            f"In total, {all_func_passed_tests} out of {num_tests} test passed. Either the implementation is wrong, or some parameters need to be adjusted"
        )
    print()

    print("CONSTANTS USED:")
    true_k, k = get_K(refinements, units_of_precision)
    true_a, a = get_A(refinements, units_of_precision)
    print(f"TRUE_K = {true_k:.5f}")
    print(f"K = {k}")
    print(f"TRUE_A = {string_format_num_list(true_a)}")
    print(f"A = {string_format_num_list(a, False)}")


def test_arc_trig_funcs(
    single_in_cordic_funcs: list,
    single_in_real_funcs: list,
    dual_in_cordic_funcs: list,
    dual_in_real_funcs: list,
    max_error: float = 0.005,
    refinements: int = 17,
    units_of_precision: int = 3,
    print_test_status: bool = True,
) -> None:
    y_tests = [
        -1,
        -0.75,
        -0.8660254038,
        -0.7071067812,
        -0.5,
        -0.25,
        0,
        0.25,
        0.5,
        0.7071067812,
        0.8660254038,
        0.75,
        1,
    ]

    all_func_passed_tests = 0
    tests_skipped = 0
    for cordic_func, real_func in zip(single_in_cordic_funcs, single_in_real_funcs):
        if print_test_status:
            print(f"Testing {cordic_func.__name__}:")
        max_deg_error = 0
        passed_tests = 0
        for y_test in y_tests:
            cordic_func_result = cordic_func(int(y_test * 10**units_of_precision), refinements, units_of_precision)

            approximate_val = cordic_func_result / 10**units_of_precision
            true_val = real_func(y_test) * 180 / math.pi
            deg_error = abs(true_val - approximate_val)
            max_deg_error = max(max_deg_error, deg_error)
            if deg_error <= max_error:
                passed_tests += 1

            if print_test_status:
                print(
                    f"   {"PASS" if deg_error <= max_error else "FAIL"}  {cordic_func.__name__}({y_test:8.5f}) = {approximate_val:10.5f}    "
                    f"{real_func.__name__}({y_test:8.5f}) = {true_val:10.5f}    deg error: {deg_error:.5f}"
                )
        all_func_passed_tests += passed_tests
        print(
            f"{cordic_func.__name__} testing complete. Passed {passed_tests}/{len(y_tests)}. Max {cordic_func.__name__} error of {max_deg_error:.5f}, max error allowed {max_error}."
        )
        if print_test_status:
            print()

    xy_tests = [
        *list((x, y) for x in range(-5, 6) for y in range(-5, 6)),
        (0.8660254, 0.5),
        (0.5, 0.8660254),
        (100, 489),
        (978, 1.2),
    ]
    for cordic_func, real_func in zip(dual_in_cordic_funcs, dual_in_real_funcs):
        if print_test_status:
            print(f"Testing {cordic_func.__name__}:")
        max_deg_error = 0
        passed_tests = 0
        for x_test, y_test in xy_tests:
            cordic_func_result = cordic_func(
                int(y_test * 10**units_of_precision), int(x_test * 10**units_of_precision), refinements, units_of_precision
            )

            approximate_val = cordic_func_result / 10**units_of_precision
            true_val = real_func(y_test, x_test) * 180 / math.pi
            deg_error = abs(true_val - approximate_val)
            max_deg_error = max(max_deg_error, deg_error)
            if deg_error <= max_error:
                passed_tests += 1

            if print_test_status:
                print(
                    f"   {"PASS" if deg_error <= max_error else "FAIL"}  {cordic_func.__name__}({y_test:8.5f}, {x_test:8.5f}) = {approximate_val:10.5f}    "
                    f"{real_func.__name__}({y_test:8.5f}, {x_test:8.5f}) = {true_val:10.5f}    deg error: {deg_error:.5f}"
                )
        all_func_passed_tests += passed_tests
        print(
            f"{cordic_func.__name__} testing complete. Passed {passed_tests}/{len(xy_tests)}. Max {cordic_func.__name__} error of {max_deg_error:.5f}, max error allowed {max_error}."
        )
        if print_test_status:
            print()

    if not print_test_status:
        print()

    num_tests = len(y_tests) * len(single_in_cordic_funcs) + len(xy_tests) * len(dual_in_cordic_funcs) - tests_skipped
    if all_func_passed_tests == num_tests:
        print(f"All {num_tests} tests passed! These functions have good settings and are implemented correctly")
    else:
        print(
            f"In total, {all_func_passed_tests} out of {num_tests} test passed. Either the implementation is wrong, or some parameters need to be adjusted"
        )
    print()

    print("CONSTANTS USED:")
    true_a, a = get_A(refinements, units_of_precision)
    print(f"TRUE_A = {string_format_num_list(true_a)}")
    print(f"A = {string_format_num_list(a, False)}")


if __name__ == "__main__":
    # max_error = 0.001
    max_error = 0.01
    print_test_status = False

    refinements = 15              # max_err = 0.01
    units_of_precision = 5        # max_err = 0.01
    # refinements = 28              # max_err = 0.001
    # units_of_precision = 6        # max_err = 0.001

    refinements_trig = refinements
    units_of_precision_trig = units_of_precision
    # refinements_trig = 9                # min for trig (max_err = 0.01)
    # units_of_precision_trig = 3          # min for trig (max_err = 0.01)
    # refinements_trig = 21                # min for trig (max_err = 0.001)
    # units_of_precision_trig = 4          # min for trig (max_err = 0.001)

    test_trig_funcs(
        [
            cordic_sin,
            cordic_cos,
            cordic_tan,
        ],
        [
            math.sin,
            math.cos,
            math.tan,
        ],
        max_error=max_error,
        refinements=refinements_trig,
        units_of_precision=units_of_precision_trig,
        print_test_status=print_test_status,
    )

    print()

    refinements_arctrig = refinements
    units_of_precision_arctrig = units_of_precision
    # refinements_arctrig = 15              # min for arctrig (max_err = 0.01)
    # units_of_precision_arctrig = 5        # min for arctrig (max_err = 0.01)
    # refinements_arctrig = 28              # min for arctrig (max_err = 0.001)
    # units_of_precision_arctrig = 6        # min for arctrig (max_err = 0.001)

    test_arc_trig_funcs(
        [
            cordic_arcsin,
            cordic_arccos,
            cordic_arctan,
        ],
        [
            math.asin,
            math.acos,
            math.atan,
        ],
        [
            cordic_arctan2,
        ],
        [
            math.atan2,
        ],
        max_error=max_error,
        refinements=refinements_arctrig,
        units_of_precision=units_of_precision_arctrig,
        print_test_status=print_test_status,
    )
