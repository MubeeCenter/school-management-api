import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("uvicorn.error")

def add_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8", errors="ignore")

        logger.error("VALIDATION ERROR -> %s", exc.errors())
        logger.error("BODY RECEIVED -> %s", body_str)

        return JSONResponse(
            status_code=422,
            content={
                "detail": exc.errors(),
                "body": body_str
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error("HTTP EXCEPTION -> %s", exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
