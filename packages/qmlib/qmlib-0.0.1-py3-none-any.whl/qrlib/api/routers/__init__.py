from fastapi import APIRouter

from qrlib.api.routers.channel import router as channelRouter

allRouters = APIRouter()
allRouters.include_router(channelRouter)

__all__ = ["allRouters"]
