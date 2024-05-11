#!/usr/bin/env python3

from pathlib import Path
import sys
import re

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from eevalue import EEValue as EEV  # noqa E402


def test_E_series():
    # These are hand-picked from the actual E series values, according to the selected mode
    series_values = {
        "round": [2.2, 3.3, 3.3, 3.0, 3.16, 3.09, 3.09],
        "floor": [2.2, 2.2, 2.7, 3.0, 3.01, 3.09, 3.09],
        "ceil": [4.7, 3.3, 3.3, 3.3, 3.16, 3.16, 3.12]
    }

    for idx, series in enumerate([3, 6, 12, 24, 48, 96, 192]):
        assert float(EEV(3.1, 2).E(series, 'round')) == series_values["round"][idx]
        assert float(EEV(3.1, 2).E(series, 'floor')) == series_values["floor"][idx]
        assert float(EEV(3.1, 2).E(series, 'ceil')) == series_values["ceil"][idx]


def test_si_prefixes():
    Si_prefixes = ('y', 'z', 'a', 'f', 'p', 'n', 'µ', 'm', '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')

    for factor in range(-24, 24 + 3, 3):
        assert str(EEV(3.1 * 10**factor, 2)) == "{:.2f} {}".format(3.1, Si_prefixes[factor // 3 + 8])

    assert str(EEV(3.1 * 10**-28, 5)) == "0.00031 y"
    assert str(EEV(3.1 * 10**28, 5)) == "31000.00000 Y"


def test_instance_corruption():
    A = EEV(10)
    B = EEV(30E-3)
    C = EEV(0.1)

    foo = B / C
    x = str(foo)
    10E-6 / A
    y = str(foo)

    assert x == y


def test_no_clamping():
    assert str(EEV('14y').E(24)) == '15.00 y'
    assert str(EEV('14y').E(96)) == '14.00 y'
    assert str(EEV('14Y').E(24)) == '13.00 Y'
    assert str(EEV('14Y').E(96)) == '14.00 Y'


def test_instanciation():
    values = []
    for i in range(-10, 10):
        values.append(EEV(i/2))


def test_precision():
    re_pattern = re.compile(r'\.(\d*)')
    precision = 5

    strings = [
        [
            precision, [
                str(EEV(0.12345, precision)),
                str(EEV(0.12345, precision) ** 2),
                str(EEV(0.12345, precision) * 2),
                str(EEV(0.12345, precision) / 2),
                str(EEV(0.12345, precision) + 2),
                str(EEV(0.12345, precision) - 2),
            ]
        ],

        [
            precision + 1, [
                str(EEV(0.12345, precision+1)),
                str(EEV(0.12345, precision) ** EEV(2, precision + 1)),
                str(EEV(0.12345, precision) * EEV(2, precision + 1)),
                str(EEV(0.12345, precision) / EEV(2, precision + 1)),
                str(EEV(0.12345, precision) + EEV(2, precision + 1)),
                str(EEV(0.12345, precision) - EEV(2, precision + 1))
            ]
        ]
    ]

    for precision in strings:
        for string in precision[1]:
            result = re.search(re_pattern, string)
            assert len(result.group(1)) == precision[0]


def test_str_notation():
    strs = [
        ['2k7', 2700],
        ['47k', 47E3],
        ['82K', 82E3],
        ['4.7k', 4700],
        ['2700', 2700],
        ['2.7', 2.7],
        ['2R7', 2.7],
        ['2r7', 2.7]
    ]

    for teststr in strs:
        assert EEV(teststr[0]) == EEV(teststr[1])
