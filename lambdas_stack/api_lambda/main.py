import uvicorn
from fastapi import FastAPI, APIRouter
from mangum import Mangum

import endpoints

app = FastAPI(title="MyApi")
api_router = APIRouter()
api_router.include_router(router=endpoints.router)
app.include_router(api_router)

handler = Mangum(app=app)

if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port=5000, reload=True)
