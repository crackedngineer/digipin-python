import math
from typing import Dict, List, Tuple

from .error import (
    InvalidDigipinCharError,
    InvalidDigipinError,
    LatitudeOutOfRangeError,
    LongitudeOutOfRangeError,
)
from .model import Coordinates, DigipinBounds

# The DIGIPIN grid as defined in the JavaScript code
DIGIPIN_GRID: List[List[str]] = [
    ["F", "C", "9", "8"],
    ["J", "3", "2", "7"],
    ["K", "4", "5", "6"],
    ["L", "M", "P", "T"],
]

# The geographical bounds as defined in the JavaScript code
BOUNDS: DigipinBounds = DigipinBounds(min_lat=2.5, max_lat=38.5, min_lon=63.5, max_lon=99.5)


class Digipin(object):
    """
    Encodes latitude and longitude into a 10-digit alphanumeric DIGIPIN
    and decodes a DIGIPIN back into its central latitude & longitude.
    """

    def __init__(self):
        """
        Initializes the Digipin.
        The grid and bounds are fixed constants for this implementation.
        """
        self.digipin_grid = DIGIPIN_GRID
        self.bounds = BOUNDS

        # Pre-compute reverse lookup for faster decoding
        self._grid_reverse_lookup: Dict[str, Tuple[int, int]] = {}
        for r_idx, row in enumerate(self.digipin_grid):
            for c_idx, char in enumerate(row):
                self._grid_reverse_lookup[char] = (r_idx, c_idx)

    def get_digipin(self, lat: float, lon: float) -> str:
        """
        Encodes latitude and longitude into a 10-digit alphanumeric DIGIPIN.

        Args:
            lat (float): Latitude in decimal degrees.
            lon (float): Longitude in decimal degrees.

        Returns:
            str: The generated 10-digit DIGIPIN string (e.g., "F3K-C4M-95P-86T").

        Raises:
            LatitudeOutOfRangeError: If latitude is outside the defined bounds.
            LongitudeOutOfRangeError: If longitude is outside the defined bounds.
        """
        if not (self.bounds.min_lat <= lat <= self.bounds.max_lat):
            raise LatitudeOutOfRangeError(
                f"Latitude {lat} out of range " f"[{self.bounds.min_lat}, {self.bounds.max_lat}]"
            )
        if not (self.bounds.min_lon <= lon <= self.bounds.max_lon):
            raise LongitudeOutOfRangeError(
                f"Longitude {lon} out of range" f"[{self.bounds.min_lon}, {self.bounds.max_lon}]"
            )

        current_min_lat = self.bounds.min_lat
        current_max_lat = self.bounds.max_lat
        current_min_lon = self.bounds.min_lon
        current_max_lon = self.bounds.max_lon

        digi_pin_chars: List[str] = []

        for level in range(1, 11):  # Levels 1 to 10
            lat_div = (current_max_lat - current_min_lat) / 4
            lon_div = (current_max_lon - current_min_lon) / 4

            row_idx = 3 - math.floor((lat - current_min_lat) / lat_div)
            col_idx = math.floor((lon - current_min_lon) / lon_div)

            # Ensure indices are within bounds [0, 3]
            row_idx = max(0, min(row_idx, 3))
            col_idx = max(0, min(col_idx, 3))

            digi_pin_chars.append(self.digipin_grid[row_idx][col_idx])

            # Add hyphen after 3rd and 6th character
            if level == 3 or level == 6:
                digi_pin_chars.append("-")

            # This corresponds to picking the specific sub-quadrant.
            # For row_idx (0,1,2,3) from the grid, the corresponding sub-quadrant
            # is (3-row_idx) from the bottom.
            # Example: if row_idx is 0 (top row of grid), it's the 4th quadrant from bottom.
            # if row_idx is 3 (bottom row of grid), it's the 1st quadrant from bottom.

            # Calculate new max_lat based on the selected row_idx
            new_max_lat = current_min_lat + lat_div * (4 - row_idx)
            # Calculate new min_lat based on the selected row_idx
            new_min_lat = current_min_lat + lat_div * (3 - row_idx)

            current_min_lat = new_min_lat
            current_max_lat = new_max_lat

            current_min_lon = current_min_lon + lon_div * col_idx
            current_max_lon = current_min_lon + lon_div

        return "".join(digi_pin_chars)

    def get_lat_lng_from_digipin(self, digi_pin: str) -> Coordinates:
        """
        Decodes a DIGIPIN back into its central latitude & longitude.

        Args:
            digi_pin (str): The 10-digit alphanumeric DIGIPIN string.

        Returns:
            Coordinates: A Coordinates dataclass containing the central latitude and longitude,
                         rounded to 6 decimal places.

        Raises:
            InvalidDigipinError: If the DIGIPIN string has an invalid length.
            InvalidDigipinCharError: If the DIGIPIN string contains an unknown character.
        """
        pin_cleaned = digi_pin.replace("-", "")
        if len(pin_cleaned) != 10:
            raise InvalidDigipinError(
                "Invalid DIGIPIN: Must be 10 alphanumeric characters (excluding hyphens)."
            )

        current_min_lat = self.bounds.min_lat
        current_max_lat = self.bounds.max_lat
        current_min_lon = self.bounds.min_lon
        current_max_lon = self.bounds.max_lon

        for char in pin_cleaned:
            if char not in self._grid_reverse_lookup:
                raise InvalidDigipinCharError(f"Invalid character '{char}' found in DIGIPIN.")

            row_idx, col_idx = self._grid_reverse_lookup[char]

            lat_div = (current_max_lat - current_min_lat) / 4
            lon_div = (current_max_lon - current_min_lon) / 4

            # Calculate the new bounding box for the next level
            # This logic directly maps the grid row/col to the sub-quadrant.
            # Note: The 'ri' (row index) here is the actual grid row index (0-3),
            # not the 'reversed' one used in encoding.

            # For latitude, the grid is "reversed" in encoding.
            # So, row_idx 0 (top row of grid) corresponds to the highest latitude sub-quadrant.
            # row_idx 3 (bottom row of grid) corresponds to the lowest latitude sub-quadrant.
            new_min_lat = current_max_lat - lat_div * (row_idx + 1)
            new_max_lat = current_max_lat - lat_div * row_idx

            new_min_lon = current_min_lon + lon_div * col_idx
            new_max_lon = current_min_lon + lon_div * (col_idx + 1)

            current_min_lat = new_min_lat
            current_max_lat = new_max_lat
            current_min_lon = new_min_lon
            current_max_lon = new_max_lon

        center_lat = (current_min_lat + current_max_lat) / 2
        center_lon = (current_min_lon + current_max_lon) / 2

        # Round to 6 decimal places as in the JavaScript example
        return Coordinates(latitude=round(center_lat, 6), longitude=round(center_lon, 6))
