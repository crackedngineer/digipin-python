import unittest

from digipin.model import Coordinates, DigipinBounds


class TestCoordinates(unittest.TestCase):
    def test_coordinates_instantiation(self):
        """Test instantiation of Coordinates dataclass."""
        coords = Coordinates(latitude=10.0, longitude=20.0)
        self.assertEqual(coords.latitude, 10.0)
        self.assertEqual(coords.longitude, 20.0)

    def test_coordinates_equality(self):
        """Test equality comparison for Coordinates dataclass."""
        coords1 = Coordinates(latitude=10.0, longitude=20.0)
        coords2 = Coordinates(latitude=10.0, longitude=20.0)
        coords3 = Coordinates(latitude=15.0, longitude=20.0)
        self.assertEqual(coords1, coords2)
        self.assertNotEqual(coords1, coords3)
        self.assertNotEqual(coords1, "not a coordinate")

    def test_coordinates_repr(self):
        """Test string representation of Coordinates dataclass."""
        coords = Coordinates(latitude=10.0, longitude=20.0)
        self.assertEqual(repr(coords), "Coordinates(latitude=10.0, longitude=20.0)")

    def test_coordinates_immutability(self):
        """Test immutability of Coordinates dataclass (frozen=True)."""
        coords = Coordinates(latitude=10.0, longitude=20.0)
        with self.assertRaises(AttributeError):
            # Attempting to modify a frozen dataclass attribute should raise AttributeError
            coords.latitude = 12.0  # type: ignore


class TestDigipinBounds(unittest.TestCase):
    def test_digipin_bounds_instantiation(self):
        """Test instantiation of DigipinBounds dataclass."""
        bounds = DigipinBounds(min_lat=0.0, max_lat=90.0, min_lon=-180.0, max_lon=180.0)
        self.assertEqual(bounds.min_lat, 0.0)
        self.assertEqual(bounds.max_lat, 90.0)
        self.assertEqual(bounds.min_lon, -180.0)
        self.assertEqual(bounds.max_lon, 180.0)

    def test_digipin_bounds_equality(self):
        """Test equality comparison for DigipinBounds dataclass."""
        bounds1 = DigipinBounds(min_lat=0.0, max_lat=90.0, min_lon=-180.0, max_lon=180.0)
        bounds2 = DigipinBounds(min_lat=0.0, max_lat=90.0, min_lon=-180.0, max_lon=180.0)
        bounds3 = DigipinBounds(min_lat=1.0, max_lat=90.0, min_lon=-180.0, max_lon=180.0)
        self.assertEqual(bounds1, bounds2)
        self.assertNotEqual(bounds1, bounds3)
        self.assertNotEqual(bounds1, "not bounds")

    def test_digipin_bounds_repr(self):
        """Test string representation of DigipinBounds dataclass."""
        bounds = DigipinBounds(min_lat=0.0, max_lat=90.0, min_lon=-180.0, max_lon=180.0)
        self.assertEqual(
            repr(bounds),
            "DigipinBounds(min_lat=0.0, max_lat=90.0, min_lon=-180.0, max_lon=180.0)",
        )

    def test_digipin_bounds_immutability(self):
        """Test immutability of DigipinBounds dataclass (frozen=True)."""
        bounds = DigipinBounds(min_lat=0.0, max_lat=90.0, min_lon=-180.0, max_lon=180.0)
        with self.assertRaises(AttributeError):
            # Attempting to modify a frozen dataclass attribute should raise AttributeError
            bounds.min_lat = 1.0  # type: ignore
