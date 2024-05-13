# Copyright (c) 2024 Santosh Philip
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================

import pytest
from epconversions import ec


def almostequal(first, second, places=7, printit=True):
    """docstring for almostequal
    # taken from python's unit test
    # may be covered by Python's license

    """
    if round(abs(second - first), places) != 0:
        if printit:
            print(round(abs(second - first), places))
            print("notalmost: %s != %s" % (first, second))
        return False
    else:
        return True


@pytest.mark.parametrize(
    "fht, expected",
    [
        (75, 23.8888888889),  # fht, expected
    ],
)
def test_f2c(fht, expected):
    result = ec.f2c(fht)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "cls, expected",
    [
        (25, 77),  # cls, expected
    ],
)
def test_c2f(cls, expected):
    result = ec.c2f(cls)
    assert result == expected
