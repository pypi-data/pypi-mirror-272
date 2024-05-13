# Copyright (c) 2024 Santosh Philip
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================

"""easy functions for conversions"""

from epconversions import epconversions

f2c = lambda f: epconversions.convert2si(f, "F", unitstr=False)
c2f = lambda c: epconversions.convert2ip(c, "C", unitstr=False)
