
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.base import main_router

app = FastAPI()
app.include_router(main_router)
app.add_middleware(CORSMiddleware, allow_origins="*")


if __name__ == ("__main__"):
    uvicorn.run("main:app", host='127.0.0.1', port=8127, reload=True)
