"""
Copyright (C) 2024 William Newport

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import unittest
from datasurface.md.Documentation import PlainTextDocumentation

from datasurface.md.Policy import AllowDisallowPolicy


class Test_Policy(unittest.TestCase):
    def test_allow_disallow_policy(self):
        # Test case 1: Object is explicitly allowed
        allowed_values = {1, 2, 3}
        policy = AllowDisallowPolicy("Test Policy", PlainTextDocumentation("Test"), allowed=allowed_values)
        self.assertTrue(policy.isCompatible(2))

        # Test case 2: Object is explicitly forbidden
        not_allowed_values = {4, 5, 6}
        policy = AllowDisallowPolicy("Test Policy", PlainTextDocumentation("Test"), notAllowed=not_allowed_values)
        self.assertFalse(policy.isCompatible(4))

        # Test case 3: Object is neither explicitly allowed nor forbidden
        allowed_values = {1, 2, 3}
        not_allowed_values = {4, 5, 6}
        policy = AllowDisallowPolicy("Test Policy", PlainTextDocumentation("Test"), allowed=allowed_values, notAllowed=not_allowed_values)
        self.assertFalse(policy.isCompatible(7))

        # Test case 4: Object is both explicitly allowed and forbidden
        allowed_values = {1, 2, 3}
        not_allowed_values = {3, 4, 5}
        try:
            policy = AllowDisallowPolicy("Test Policy", PlainTextDocumentation("Test"), allowed=allowed_values, notAllowed=not_allowed_values)
            self.fail("Exception not thrown for overlapping allow/disallow sets")
        except Exception:
            # Test is succesful
            pass
