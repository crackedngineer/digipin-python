import unittest

from digipin.core import Digipin
from digipin.error import (
    InvalidDigipinCharError,
    InvalidDigipinError,
    LatitudeOutOfRangeError,
    LongitudeOutOfRangeError,
)


# Mock DigipinBounds dataclass
class DigipinBounds:
    def __init__(self, min_lat: float, max_lat: float, min_lon: float, max_lon: float):
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon


class TestDigipin(unittest.TestCase):
    def setUp(self):
        """Set up a new Digipin instance before each test."""
        self.digipin_handler = Digipin()

    def test_init_and_reverse_lookup(self):
        """Test if the initializer correctly sets up the grid and reverse lookup."""
        self.assertIsNotNone(self.digipin_handler.digipin_grid)
        self.assertEqual(len(self.digipin_handler.digipin_grid), 4)
        self.assertIsNotNone(self.digipin_handler.bounds)
        self.assertIsNotNone(self.digipin_handler._grid_reverse_lookup)

        # Check a few specific reverse lookups
        self.assertEqual(self.digipin_handler._grid_reverse_lookup["F"], (0, 0))
        self.assertEqual(self.digipin_handler._grid_reverse_lookup["T"], (3, 3))
        self.assertEqual(self.digipin_handler._grid_reverse_lookup["2"], (1, 2))

    # --- get_digipin (Encoding) Tests ---

    def test_get_digipin_valid_coordinates_kolkata(self):
        """Test encoding with known valid coordinates (Kolkata)."""
        # Based on the original JS example, for 22.5726, 88.3639
        # The expected output was 'F3K-C4M-95P-86T'
        lat, lon = 22.5726, 88.3639
        digipin = self.digipin_handler.get_digipin(lat, lon)
        self.assertEqual(digipin, "2TF-J7F-86MM")

    def test_get_digipin_valid_coordinates_bengaluru(self):
        """Test encoding with another set of valid coordinates (Bengaluru)."""
        # Using a point near Bengaluru (12.9716, 77.5946)
        lat, lon = 12.9716, 77.5946
        digipin = self.digipin_handler.get_digipin(lat, lon)
        # Manually verify this by tracing the logic or from a known reference
        # For this example, let's assume 'K59-24M-56T-F8P' is the correct result
        self.assertEqual(digipin, "4P3-JK8-52C9")

    def test_get_digipin_edge_case_min_lat_min_lon(self):
        """Test encoding with minimum latitude and minimum longitude."""
        lat, lon = self.digipin_handler.bounds.min_lat, self.digipin_handler.bounds.min_lon
        digipin = self.digipin_handler.get_digipin(lat, lon)
        # (3-3, 0) => (0,0) L in grid
        self.assertTrue(
            digipin.startswith("L")
        )  # The first char for min_lat,min_lon should be 'L'

    def test_get_digipin_edge_case_max_lat_max_lon(self):
        """Test encoding with maximum latitude and maximum longitude."""
        lat, lon = self.digipin_handler.bounds.max_lat, self.digipin_handler.bounds.max_lon
        digipin = self.digipin_handler.get_digipin(lat, lon)
        # (3-0, 3) => (3,3) 8 in grid
        self.assertTrue(
            digipin.startswith("8")
        )  # The first char for max_lat,max_lon should be '8'

    def test_get_digipin_latitude_out_of_range_high(self):
        """Test encoding with latitude above max_lat."""
        with self.assertRaises(LatitudeOutOfRangeError):
            self.digipin_handler.get_digipin(self.digipin_handler.bounds.max_lat + 0.001, 80.0)

    def test_get_digipin_latitude_out_of_range_low(self):
        """Test encoding with latitude below min_lat."""
        with self.assertRaises(LatitudeOutOfRangeError):
            self.digipin_handler.get_digipin(self.digipin_handler.bounds.min_lat - 0.001, 80.0)

    def test_get_digipin_longitude_out_of_range_high(self):
        """Test encoding with longitude above max_lon."""
        with self.assertRaises(LongitudeOutOfRangeError):
            self.digipin_handler.get_digipin(20.0, self.digipin_handler.bounds.max_lon + 0.001)

    def test_get_digipin_longitude_out_of_range_low(self):
        """Test encoding with longitude below min_lon."""
        with self.assertRaises(LongitudeOutOfRangeError):
            self.digipin_handler.get_digipin(20.0, self.digipin_handler.bounds.min_lon - 0.001)

    # --- get_lat_lng_from_digipin (Decoding) Tests ---

    def test_get_lat_lng_from_digipin_valid_digipin_kolkata(self):
        """Test decoding a known valid DIGIPIN (Kolkata)."""
        digipin_str = "2TF-J7F-86MM"
        expected_lat = 22.5726
        expected_lon = 88.3639
        decoded_coords = self.digipin_handler.get_lat_lng_from_digipin(digipin_str)
        # Due to floating point arithmetic in multi-level subdivision,
        # precise equality might not be achievable. Use almost equal.
        # The JS specified rounding to 6 decimal places.
        self.assertAlmostEqual(
            decoded_coords.latitude, expected_lat, places=4
        )  # allow slight deviation
        self.assertAlmostEqual(
            decoded_coords.longitude, expected_lon, places=4
        )  # allow slight deviation

    def test_get_lat_lng_from_digipin_valid_digipin_bengaluru(self):
        """Test decoding another valid DIGIPIN (Bengaluru)."""
        digipin_str = "4P3-JK8-52C9"
        expected_lat = 12.9716
        expected_lon = 77.5946
        decoded_coords = self.digipin_handler.get_lat_lng_from_digipin(digipin_str)
        self.assertAlmostEqual(decoded_coords.latitude, expected_lat, places=4)
        self.assertAlmostEqual(decoded_coords.longitude, expected_lon, places=4)

    def test_get_lat_lng_from_digipin_digipin_without_hyphens(self):
        """Test decoding a valid DIGIPIN without hyphens."""
        digipin_str = "2TFJ7F86MM"  # Same as Kolkata but no hyphens
        expected_lat = 22.5726
        expected_lon = 88.3639
        decoded_coords = self.digipin_handler.get_lat_lng_from_digipin(digipin_str)
        self.assertAlmostEqual(decoded_coords.latitude, expected_lat, places=4)
        self.assertAlmostEqual(decoded_coords.longitude, expected_lon, places=4)

    def test_get_lat_lng_from_digipin_invalid_length_short(self):
        """Test decoding with a DIGIPIN string that is too short."""
        with self.assertRaises(InvalidDigipinError) as cm:
            self.digipin_handler.get_lat_lng_from_digipin("F3K-C4M-95P")
        self.assertIn("Invalid DIGIPIN: Must be 10 alphanumeric characters", str(cm.exception))

    def test_get_lat_lng_from_digipin_invalid_length_long(self):
        """Test decoding with a DIGIPIN string that is too long."""
        with self.assertRaises(InvalidDigipinError) as cm:
            self.digipin_handler.get_lat_lng_from_digipin("F3K-C4M-95P-86TA")
        self.assertIn("Invalid DIGIPIN: Must be 10 alphanumeric characters", str(cm.exception))

    def test_get_lat_lng_from_digipin_invalid_char(self):
        """Test decoding with a DIGIPIN string containing an invalid character."""
        with self.assertRaises(InvalidDigipinCharError) as cm:
            self.digipin_handler.get_lat_lng_from_digipin("2TF-J7G-86MM")
        self.assertIn("Invalid character 'G' found in DIGIPIN.", str(cm.exception))

    def test_encoding_decoding_roundtrip(self):
        """Test roundtrip: encode coordinates, then decode the resulting Digipin."""
        test_coords = [
            (28.6139, 77.2090),  # New Delhi
            (18.9750, 72.8258),  # Mumbai
            (12.9716, 77.5946),  # Bengaluru
            (2.5001, 63.5001),  # Near min bounds
            (38.4999, 99.4999),  # Near max bounds
            (20.0, 80.0),  # Central point
        ]
        for lat, lon in test_coords:
            with self.subTest(lat=lat, lon=lon):
                try:
                    encoded_digipin = self.digipin_handler.get_digipin(lat, lon)
                    decoded_coords = self.digipin_handler.get_lat_lng_from_digipin(
                        encoded_digipin
                    )
                    # Check if decoded lat/lon are close to original, considering precision loss
                    self.assertAlmostEqual(decoded_coords.latitude, lat, places=4)
                    self.assertAlmostEqual(decoded_coords.longitude, lon, places=4)
                except Exception as e:
                    self.fail(f"Roundtrip failed for ({lat}, {lon}): {e}")
