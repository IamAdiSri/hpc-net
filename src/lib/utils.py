# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# convert 6-byte hex address to string
xtos = lambda x: ":".join("{0:012x}".format(x)[i : i + 2] for i in range(0, 12, 2))
