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

from datasurface.platforms.azure.Azure import SQLServerNamingMapper
from datasurface.md.Governance import DataContainerNamingMapper


class Test_DataContainerMapper(unittest.TestCase):
    def test_IdentifierTruncation(self):
        mapper: DataContainerNamingMapper = SQLServerNamingMapper()
        self.assertEqual(mapper.truncateIdentifier("this_is_a_test", 64), "this_is_a_test")
        self.assertEqual(mapper.truncateIdentifier("this_is_a_test", 8), "this_505")
        self.assertEqual(mapper.truncateIdentifier("this_is_a_different_test", 8), "this_3f7")
        self.assertEqual(mapper.truncateIdentifier("this_is_aanother_different_test", 8), "this_ed8")
