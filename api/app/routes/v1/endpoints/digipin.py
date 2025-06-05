from app.dependencies import get_digipin_service
from app.error import APIError
from app.schemas.digipin_schemas import (
    CoordinatesInput,
    DecodeResponse,
    EncodeResponse,
)
from app.services.digipin_services import DigipinService
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/digipin",
    tags=["core"],
)


@router.post(
    "/encode", response_model=EncodeResponse, summary="Encode Latitude and Longitude to Digipin"
)
async def encode_lat_lon_to_digipin(
    coords: CoordinatesInput, digipin_service: DigipinService = Depends(get_digipin_service)
):
    """
    Encodes a given latitude and longitude into a DIGIPIN string.
    """
    try:
        return digipin_service.encode_digipin(coords.latitude, coords.longitude)
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )


@router.get(
    "/decode/{digipin_str}",
    response_model=DecodeResponse,
    summary="Decode Digipin to Latitude and Longitude",
)
async def decode_digipin_to_lat_lon(
    digipin_str: str, digipin_service: DigipinService = Depends(get_digipin_service)
):
    """
    Decodes a DIGIPIN string back into its central latitude and longitude.
    """
    try:
        return digipin_service.decode_digipin(digipin_str)
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )
