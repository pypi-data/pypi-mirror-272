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

from typing import Optional
import unittest

from datasurface.md.Governance import InfrastructureLocation, InfrastructureVendor


class Test_VendorLocation(unittest.TestCase):
    def test_VendorLocation(self):
        vendor: InfrastructureVendor = InfrastructureVendor(
            "AWS",
            InfrastructureLocation(
                "USA",
                InfrastructureLocation("us-east-1"),
                InfrastructureLocation("us-west-1")
                ),
            InfrastructureLocation(
                "EU",
                InfrastructureLocation("eu-west-1"),
                InfrastructureLocation("eu-west-2"))
            )

        east: Optional[InfrastructureLocation] = vendor.findLocationUsingKey(["USA", "us-east-1"])
        self.assertIsNotNone(east)

        west: Optional[InfrastructureLocation] = vendor.findLocationUsingKey(["USA", "us-west-1"])
        self.assertIsNotNone(west)

        unknown: Optional[InfrastructureLocation] = vendor.findLocationUsingKey(["USA", "us-west-2"])
        self.assertIsNone(unknown)

        usa: Optional[InfrastructureLocation] = vendor.findLocationUsingKey(["USA"])
        self.assertIsNotNone(usa)

        eu: Optional[InfrastructureLocation] = vendor.findLocationUsingKey(["EU"])
        self.assertIsNotNone(eu)

        if (eu is not None and usa is not None and east is not None and west is not None):
            self.assertTrue(usa.containsLocation(east))
            self.assertTrue(usa.containsLocation(west))
            self.assertTrue(usa.containsLocation(usa))
            self.assertTrue(eu.containsLocation(eu))
            self.assertFalse(usa.containsLocation(eu))
            self.assertFalse(eu.containsLocation(usa))
