"""description"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import debugpy
from routers import routespull
from routers import routes
from routers import routesbalance
from routers import routesmerchant
from helper.logging import setup_logger

debugpy.listen(("0.0.0.0", 5678))

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)


@app.get("/")
def index():
    """hello"""
    # var = os.environ['COUCHDB_USER']
    return {"details": "Hello my friends! "}

# if __name__ == "__main__":
#  uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)


setup_logger()

app.include_router(routespull.routerpull)
app.include_router(routes.router)
app.include_router(routesmerchant.routermerch)
app.include_router(routesbalance.routerbalance)
