from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    """
    A dataclass to represent geographical coordinates.

    Attributes:
        latitude (float): The latitude in decimal degrees.
                          Must be between -90.0 and 90.0.
        longitude (float): The longitude in decimal degrees.
                           Must be between -180.0 and 180.0.
    """

    latitude: float
    longitude: float


@dataclass(frozen=True)
class DigipinBounds:
    """
    A dataclass to represent the geographical bounds for DIGIPIN generation.

    Attributes:
        min_lat (float): Minimum allowed latitude.
        max_lat (float): Maximum allowed latitude.
        min_lon (float): Minimum allowed longitude.
        max_lon (float): Maximum allowed longitude.
    """

    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
