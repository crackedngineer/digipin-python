from digipin import Digipin
from digipin.error import (
    InvalidDigipinCharError,
    InvalidDigipinError,
    LatitudeOutOfRangeError,
    LongitudeOutOfRangeError,
)

from ..error import APIError
from ..schemas.digipin_schemas import DecodeResponse, EncodeResponse


class DigipinService:
    """
    Service responsible for interacting with the DigipinEncoderDecoder package.
    Handles encoding and decoding, including error translation from the package's
    exceptions to API-specific exceptions.
    """

    def __init__(self):
        self.encoder_decoder = Digipin()

    def encode_digipin(self, latitude: float, longitude: float) -> EncodeResponse:
        """
        Encodes latitude and longitude into a DIGIPIN.

        Args:
            latitude (float): Latitude.
            longitude (float): Longitude.

        Returns:
            EncodeResponse: The generated DIGIPIN and input coordinates.

        Raises:
            APIError: If coordinates are out of the valid range for Digipin generation.
        """
        try:
            digipin = self.encoder_decoder.get_digipin(latitude, longitude)
            return EncodeResponse(latitude=latitude, longitude=longitude, digipin=digipin)
        except (LatitudeOutOfRangeError, LongitudeOutOfRangeError) as e:
            raise APIError(f"Coordinates out of DIGIPIN bounds: {e.message}", status_code=400)
        except Exception as e:
            raise APIError(
                f"An unexpected error occurred during Digipin encoding: {e}", status_code=500
            )

    def decode_digipin(self, digipin_str: str) -> DecodeResponse:
        """
        Decodes a DIGIPIN string into latitude and longitude.

        Args:
            digipin_str (str): The DIGIPIN string.

        Returns:
            DecodeResponse: The decoded coordinates and input Digipin.

        Raises:
            APIError: If the DIGIPIN is invalid.
        """
        try:
            coords = self.encoder_decoder.get_lat_lng_from_digipin(digipin_str)
            return DecodeResponse(
                digipin=digipin_str, latitude=coords.latitude, longitude=coords.longitude
            )
        except (InvalidDigipinError, InvalidDigipinCharError) as e:
            raise APIError(f"Invalid DIGIPIN: {e.message}", status_code=400)
        except Exception as e:
            raise APIError(
                f"An unexpected error occurred during Digipin decoding: {e}", status_code=500
            )
