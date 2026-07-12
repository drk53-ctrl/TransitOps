from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.database import engine, Base

from backend.routes import (
    vehicles,
    drivers,
    trips,
    maintenance,
    dashboard,
    auth_routes
)

from backend.routes import web_routes


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="TransitOps"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


BASE_DIR = Path(__file__).resolve().parent.parent


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            BASE_DIR / "frontend" / "static"
        )
    ),
    name="static"
)


templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "frontend" / "templates"
    )
)


app.include_router(auth_routes.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(trips.router)
app.include_router(maintenance.router)
app.include_router(dashboard.router)
app.include_router(web_routes.router)


@app.get("/")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.get("/signup")
def signup_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={}
    )


@app.exception_handler(Exception)
async def debug_exception(
    request: Request,
    exc: Exception
):

    print("\n\nERROR:", repr(exc), "\n\n")

    raise exc