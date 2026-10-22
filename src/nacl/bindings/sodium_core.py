# Copyright 2013 Donald Stufft and individual contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, division, print_function

from nacl import exceptions as exc
from nacl._sodium import ffi, lib
from nacl.exceptions import ensure


# A point on the curve but outside the main subgroup: its L-multiple has
# X == 0 but Y != Z. libsodium before the 2025-12-31 1.0.20-stable build
# accepts it as valid (CVE-2025-69277).
_NOT_MAIN_SUBGROUP_P = b'\x95' + 31 * b'\x99'


def _check_main_subgroup_validation(is_valid_point):
    """
    Refuse a libsodium whose ed25519 point validation accepts a point
    outside the main subgroup (CVE-2025-69277). The version string cannot
    tell a vulnerable 1.0.20 from the fixed 1.0.20-stable, so test the
    behaviour instead.
    """
    ensure(is_valid_point(_NOT_MAIN_SUBGROUP_P) == 0,
           "The libsodium PyNaCl is linked against accepts ed25519 points "
           "outside the main subgroup (CVE-2025-69277). Rebuild or run "
           "against libsodium 1.0.20-stable (2025-12-31) or later.",
           raising=exc.RuntimeError)


def _sodium_init():
    ensure(lib.sodium_init() != -1,
           "Could not initialize sodium",
           raising=exc.RuntimeError)
    # minimal builds of libsodium don't provide the ed25519 core functions,
    # so nothing in PyNaCl can reach the flawed check there
    if lib.PYNACL_HAS_CRYPTO_CORE_ED25519:
        _check_main_subgroup_validation(
            lib.crypto_core_ed25519_is_valid_point)


def sodium_init():
    """
    Initializes sodium, picking the best implementations available for this
    machine.
    """
    ffi.init_once(_sodium_init, "libsodium")
