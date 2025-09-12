# SPDX-FileCopyrightText: 2025 pydot contributors
#
# SPDX-License-Identifier: MIT
"""Helper script that does nothing but fail."""

import sys

if __name__ == "__main__":
    print("I'm a failure.", file=sys.stderr)
    sys.exit(1)
