import time

from fastapi import HTTPException
from pydantic import conint
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

REQUESTS = {

}


class Limiter:
    def __init__(self,
                 times: conint(ge=0) = 1,
                 seconds: conint(ge=-1) = 0,
                 minutes: conint(ge=-1) = 0):
        self.times = times
        self.milliseconds = 1000 * seconds + 60000 * minutes

    @staticmethod
    def default_identifier(request: Request):
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.client.host
        return ip + ":" + request.scope["path"]

    def __call__(self, request: Request, response: Response):
        identifier = self.default_identifier(request)
        if identifier not in REQUESTS:
            REQUESTS[identifier] = time.time()
        else:
            t = self.milliseconds - int((time.time() - REQUESTS[identifier]) * 1000)
            if t > 0:
                raise HTTPException(
                    HTTP_429_TOO_MANY_REQUESTS, "Too Many Requests", headers={"Retry-After": str(t)}
                )
            REQUESTS.pop(identifier)
