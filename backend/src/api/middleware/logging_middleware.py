"""Structured logging and error handling (T014)."""
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("chimera.api")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        try:
            response = await call_next(request)
            duration = time.perf_counter() - start
            logger.info(
                "%s %s %s %.3fs",
                request.method,
                request.url.path,
                response.status_code,
                duration,
            )
            return response
        except Exception as exc:
            duration = time.perf_counter() - start
            logger.exception("Request failed %s %s %.3fs: %s", request.method, request.url.path, duration, exc)
            raise
