from typing import List

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


@router.post(
    "/batch-encode",
    response_model=List[EncodeResponse],
    summary="Batch Encode Multiple Coordinates to Digipins",
)
async def batch_encode_lat_lon_to_digipins(
    coords_list: List[CoordinatesInput],
    digipin_service: DigipinService = Depends(get_digipin_service),
):
    """
    Encodes a list of latitude and longitude pairs into their respective DIGIPIN strings.
    Returns a list of results, where each result corresponds to an input coordinate.
    """
    results: List[EncodeResponse] = []
    for coords in coords_list:
        try:
            results.append(digipin_service.encode_digipin(coords.latitude, coords.longitude))
        except APIError as e:
            # For batch operations, you might want to return errors for individual items
            # or skip them. Here, we'll append a placeholder and log the error.
            print(f"Error encoding {coords.latitude},{coords.longitude}: {e.message}")
            results.append(
                EncodeResponse(
                    latitude=coords.latitude,
                    longitude=coords.longitude,
                    digipin="ERROR",
                    detail=e.message,
                )
            )
        except Exception as e:
            print(f"Unexpected error encoding {coords.latitude},{coords.longitude}: {e}")
            results.append(
                EncodeResponse(
                    latitude=coords.latitude,
                    longitude=coords.longitude,
                    digipin="ERROR",
                    detail="Unexpected server error",
                )
            )
    return results


@router.post(
    "/batch-decode",
    response_model=List[DecodeResponse],
    summary="Batch Decode Multiple Digipins to Coordinates",
)
async def batch_decode_digipins_to_lat_lon(
    digipin_strs: List[str], digipin_service: DigipinService = Depends(get_digipin_service)
):
    """
    Decodes a list of DIGIPIN strings back into their central latitude and longitude.
    Returns a list of results, where each result corresponds to an input Digipin.
    """
    results: List[DecodeResponse] = []
    for digipin_str in digipin_strs:
        try:
            results.append(digipin_service.decode_digipin(digipin_str))
        except APIError as e:
            print(f"Error decoding {digipin_str}: {e.message}")
            results.append(
                DecodeResponse(digipin=digipin_str, latitude=0.0, longitude=0.0, detail=e.message)
            )
        except Exception as e:
            print(f"Unexpected error decoding {digipin_str}: {e}")
            results.append(
                DecodeResponse(
                    digipin=digipin_str,
                    latitude=0.0,
                    longitude=0.0,
                    detail="Unexpected server error",
                )
            )
    return results
