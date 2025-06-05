from typing import Optional

from pydantic import BaseModel, Field


class CoordinatesInput(BaseModel):
    """
    Schema for input coordinates for encoding.
    """

    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees.")
    longitude: float = Field(
        ..., ge=-180.0, le=180.0, description="Longitude in decimal degrees."
    )


class EncodeResponse(BaseModel):
    """
    Schema for the Digipin encoding response.
    """

    latitude: float = Field(..., description="Input latitude.")
    longitude: float = Field(..., description="Input longitude.")
    digipin: str = Field(..., description="Generated DIGIPIN.")
    detail: Optional[str] = Field(default=None, description="details")


class DecodeResponse(BaseModel):
    """
    Schema for the Digipin decoding response.
    """

    digipin: str = Field(..., description="Input DIGIPIN.")
    latitude: float = Field(..., description="Decoded latitude.")
    longitude: float = Field(..., description="Decoded longitude.")
    detail: Optional[str] = Field(default=None, description="details")
