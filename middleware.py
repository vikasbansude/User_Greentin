from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse

from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction
import time
from collections import defaultdict
from typing import Dict

from starlette.types import ASGIApp

import os
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Read configuration values from environment variables
SKIP_PATHS = os.getenv("SKIP_PATHS", "").split(",")
RATE_LIMIT_INTERVAL = float(os.getenv("RATE_LIMIT_INTERVAL", 1))
    
class AdvMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)
        
    async def dispatch(self, request: Request, call_next):

        if request.url.path in SKIP_PATHS:
            return await call_next(request)
        
        client_ip = request.client.host
        current_time = time.time()
        
        if current_time - self.rate_limit_records[client_ip] < RATE_LIMIT_INTERVAL:
            return Response(content="Rate limit exceeded",status_code=429)
        
        self.rate_limit_records[client_ip] = current_time
        
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add custom header to response
        response.headers["X-Process-Time"] = str(process_time)

        # Proceed with request if Authorization is valid
        # For secured endpoints, check for Authorization header
        if "Authorization" not in request.headers:
            # raise HTTPException(status_code=403, detail="Unauthorized access")  // results in "Internal Server Error"
            return Response(content="Middleware : Unauthorized access",status_code=403)
            # return JSONResponse(status_code=403, content={"detail": "Unauthorized access"})
            # response_body = {"Unauthorized access"}
            # return JSONResponse(content=response_body, status_code=403)
        # response = await call_next(request)
        # response_body = {"message": "Middleware Request & Response was successful"}
        # return JSONResponse(content=response_body, status_code=200)
        return response