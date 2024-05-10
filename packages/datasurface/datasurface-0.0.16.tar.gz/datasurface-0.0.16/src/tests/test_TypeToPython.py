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

from datasurface.md.Schema import Vector, Binary, Variant, Boolean, NChar, Char, String, VarChar
from datasurface.md.Schema import NVarChar, Interval, Date, Timestamp, Decimal, FP8_E4M3FNUZ


class Test_ColumnCodeGen(unittest.TestCase):

    def test_ColumnCodeGen(self):
        self.assertEqual(str(Vector(10)), "Vector(10)")
        self.assertEqual(str(Binary(10)), "Binary(10)")
        self.assertEqual(str(Variant(10)), "Variant(10)")
        self.assertEqual(str(Variant()), "Variant()")
        self.assertEqual(str(Boolean()), "Boolean()")

        self.assertEqual(str(NChar()), "NChar()")
        self.assertEqual(str(NChar(10)), "NChar(10)")
        self.assertEqual(str(NChar(10, "latin-1")), "NChar(10, 'latin-1')")

        self.assertEqual(str(Char()), "Char()")
        self.assertEqual(str(Char(10)), "Char(10)")
        self.assertEqual(str(Char(10, "latin-1")), "Char(10, 'latin-1')")

        self.assertEqual(str(String()), 'String()')
        self.assertEqual(str(String(10)), 'String(10)')
        self.assertEqual(str(String(10, 'latin-1')), "String(10, 'latin-1')")
        self.assertEqual(str(String(None, 'latin-1')), "String(collationString='latin-1')")

        self.assertEqual(str(VarChar()), 'VarChar()')
        self.assertEqual(str(VarChar(10)), 'VarChar(10)')
        self.assertEqual(str(VarChar(10, 'latin-1')), "VarChar(10, 'latin-1')")
        self.assertEqual(str(VarChar(None, 'latin-1')), "VarChar(collationString='latin-1')")

        self.assertEqual(str(NVarChar()), 'NVarChar()')
        self.assertEqual(str(NVarChar(10)), 'NVarChar(10)')
        self.assertEqual(str(NVarChar(10, 'latin-1')), "NVarChar(10, 'latin-1')")
        self.assertEqual(str(NVarChar(None, 'latin-1')), "NVarChar(collationString='latin-1')")

        self.assertEqual(str(Interval()), 'Interval()')
        self.assertEqual(str(Date()), 'Date()')
        self.assertEqual(str(Timestamp()), 'Timestamp()')

        self.assertEqual(str(Decimal(10, 2)), 'Decimal(10,2)')

        # The other floating types are similar to this
        self.assertEqual(str(FP8_E4M3FNUZ()), 'FP8_E4M3FNUZ()')
