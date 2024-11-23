from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from src.utils.auth import decode_access_token
from src.constants.routes import get_private_routes
from fastapi.security import  HTTPAuthorizationCredentials
class AuthVerificationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get private routes
        token: HTTPAuthorizationCredentials = request.headers.get("Authorization")
        private_routes = get_private_routes()

        # Check if the current route is a private route
        if any(request.url.path.startswith(route) for route in private_routes):
            # Check for Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authorization header missing"}
                )

            # Split and validate token format
            parts = auth_header.split(" ", 1)
            if len(parts) != 2:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid Authorization header format"}
                )

            token_type, token = parts
            if token_type.lower() != "bearer":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token type"}
                )

            # Decode and validate token
            try:
                payload = decode_access_token(token)
                if payload is None:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Invalid or expired token"}
                    )
                
                # Store payload in request state for route access
                request.state.user = payload

            except Exception as e:
                # Log unexpected errors
                print(f"Token verification error: {str(e)}")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authentication failed"}
                )

        # Continue to the next middleware or route handler
        try:
            response = await call_next(request)
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
        except Exception as exc:
            print(f"Unhandled exception: {str(exc)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"}
            )

        return response