from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class DynamicCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        origin = request.headers.get("origin")

        if request.method == "OPTIONS":
            resp = Response(status_code=204)
            if origin:
                resp.headers["Access-Control-Allow-Origin"] = origin
                resp.headers["Vary"] = "Origin"
                resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
                resp.headers["Access-Control-Allow-Headers"] = request.headers.get(
                    "access-control-request-headers", "*"
                )
                resp.headers["Access-Control-Allow-Credentials"] = "true"
                resp.headers["Access-Control-Max-Age"] = "600"
            return resp

        response = await call_next(request)
        if origin:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Vary"] = "Origin"
            response.headers["Access-Control-Allow-Credentials"] = "true"
        return response