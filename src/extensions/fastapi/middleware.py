from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse


class GlobalMiddleware:

    def __init__(self, app: FastAPI):
        self.app = app

    @staticmethod
    async def dispatch_request(request: Request, call_next):
        response: StreamingResponse = await call_next(request)
        return response

    def init(self):
        self.app.add_middleware(
            BaseHTTPMiddleware, dispatch=self.dispatch_request
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
