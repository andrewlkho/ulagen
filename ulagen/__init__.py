#!/usr/bin/env python

# Import the "public" functions.
from .ulagen import gen_prefix, gen_subnet

# Silence warnings from pyflakes as these aren't referenced in this script.
assert gen_prefix
assert gen_subnet
