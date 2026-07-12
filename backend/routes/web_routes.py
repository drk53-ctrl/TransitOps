from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()


templates = Jinja2Templates(
    directory="frontend/templates"
)



@router.get("/dashboard")
def dashboard_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )



@router.get("/vehicles")
def vehicles_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="vehicles/list.html",
        context={
            "vehicles": []
        }
    )



@router.get("/drivers")
def drivers_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="drivers/list.html",
        context={
            "drivers": []
        }
    )



@router.get("/trips")
def trips_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="trips/list.html",
        context={
            "trips": []
        }
    )



@router.get("/maintenance")
def maintenance_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="maintenance/list.html",
        context={
            "maintenance": []
        }
    )



@router.get("/fuel")
def fuel_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="fuel/list.html",
        context={
            "fuels": []
        }
    )



@router.get("/reports")
def reports_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "total_trips": 0,
            "total_distance": 0,
            "fuel_expense": 0,
            "maintenance_expense": 0,
            "other_expense": 0
        }
    )



@router.get("/profile")
def profile_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={}
    )