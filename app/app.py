from fastapi import FastAPI, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.auth import AuthBearer
from app.core.exchange import exchange_rates_usd2mxn
from app.models.exchange_model import Rates
from app.core.limiter import Limiter

app = FastAPI()
security = AuthBearer()


@app.get("/exchange", response_model=Rates, dependencies=[Depends(Limiter(times=5, minutes=1))])
async def exchange(_: HTTPAuthorizationCredentials = Security(security)):
    response = exchange_rates_usd2mxn()
    return response
