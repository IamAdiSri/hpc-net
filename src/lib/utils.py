# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
from contextlib import redirect_stdout

def xtos(x):
    """
    Convert 6-byte hex address to string

    Args:
        x: Hexadecimal number

    Returns:
        str: MAC address delimited by ':'
    """

    return ":".join("{0:012x}".format(x)[i : i + 2] for i in range(0, 12, 2))


def capture_stdout(func):
    def wrapper(*args, **kwargs):
        f = io.StringIO()
        with redirect_stdout(f):
            func(*args, **kwargs)
        return f.getvalue()
    return wrapper