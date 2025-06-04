from digipin import Digipin, Coordinates
from digipin.error import (
    LatitudeOutOfRangeError,
    LongitudeOutOfRangeError,
    InvalidDigipinError,
    InvalidDigipinCharError,
)

# Initialize the encoder/decoder
digipin_handler = Digipin()

# --- Encoding Example ---
print("--- Encoding Examples ---")
try:
    # Example 1: Latitude and Longitude within bounds
    lat1, lon1 = 22.5726, 88.3639
    digipin1 = digipin_handler.get_digipin(lat1, lon1)
    print(
        f"Coordinates ({lat1}, {lon1}) -> DIGIPIN: {digipin1}"
    )  # Expected: F3K-C4M-95P-86T (example from JS)

    # Example 2: Another set of coordinates
    lat2, lon2 = 12.9716, 77.5946  # Bengaluru
    digipin2 = digipin_handler.get_digipin(lat2, lon2)
    print(f"Coordinates ({lat2}, {lon2}) -> DIGIPIN: {digipin2}")

    # Example 3: Latitude out of range
    # lat_invalid_high, lon_valid = 40.0, 80.0
    # digipin_handler.get_digipin(lat_invalid_high, lon_valid)

except LatitudeOutOfRangeError as e:
    print(f"Error encoding: {e}")
except LongitudeOutOfRangeError as e:
    print(f"Error encoding: {e}")
except Exception as e:
    print(f"An unexpected error occurred during encoding: {e}")


# --- Decoding Example ---
print("\n--- Decoding Examples ---")
try:
    # Example 1: Decode the previously generated DIGIPIN
    decoded_coords1 = digipin_handler.get_lat_lng_from_digipin(digipin1)
    print(
        f"DIGIPIN {digipin1} -> Decoded Coordinates: ({decoded_coords1.latitude}, {decoded_coords1.longitude})"
    )

    # Example 2: Decode another valid DIGIPIN
    test_digipin = "J3K-C4M-95P-86T"  # Example for testing
    decoded_coords2 = digipin_handler.get_lat_lng_from_digipin(test_digipin)
    print(
        f"DIGIPIN {test_digipin} -> Decoded Coordinates: ({decoded_coords2.latitude}, {decoded_coords2.longitude})"
    )

    # Example 3: Invalid DIGIPIN length
    # invalid_pin_len = "ABC"
    # digipin_handler.get_lat_lng_from_digipin(invalid_pin_len)

    # Example 4: Invalid character in DIGIPIN
    # invalid_pin_char = "F3K-C4M-X5P-86T"
    # digipin_handler.get_lat_lng_from_digipin(invalid_pin_char)

except InvalidDigipinError as e:
    print(f"Error decoding: {e}")
except InvalidDigipinCharError as e:
    print(f"Error decoding: {e}")
except Exception as e:
    print(f"An unexpected error occurred during decoding: {e}")
