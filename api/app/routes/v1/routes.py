from fastapi import APIRouter

from .endpoints.digipin import router as digipin_router

routers = APIRouter()
router_list = [digipin_router]

for router in router_list:
    routers.include_router(router, tags=["v1"])
