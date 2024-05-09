try:
    from rpl_config import load
except ImportError:
    from .rpl_config import load
finally:
    load()

from qrlib.api.dbCLI import dbCLI

from contextlib import asynccontextmanager
import uvicorn
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI
from qrlib.api.routers import allRouters


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("启动前执行")

    if not dbCLI.is_connected():
        dbCLI.connect()
    yield
    print("关闭后前执行")
    dbCLI.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(allRouters, prefix="/apis")


@app.get("/")
def read_root():
    return {"version": "1.0.0"}


if __name__ == '__main__':
    uvicorn.run(
        app='app:app',
        host='127.0.0.1',
        port=8000,
        root_path='/',
        reload=True
    )
