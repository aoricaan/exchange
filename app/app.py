from fastapi import Depends
from fastapi import FastAPI
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials

from app.core.auth import AuthBearer
from app.core.exchange import exchange_rates_usd2mxn
from app.core.limiter import Limiter
from app.models.exchange_model import Rates

app = FastAPI()
security = AuthBearer()


@app.get("/exchange", response_model=Rates, dependencies=[Depends(Limiter(times=5, minutes=1))])
async def exchange(_: HTTPAuthorizationCredentials = Security(security)):
    response = exchange_rates_usd2mxn()
    return response
