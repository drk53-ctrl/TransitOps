from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.model import Vehicle, Driver, Trip, Maintenance

router = APIRouter()

templates = Jinja2Templates(directory="frontend/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):

    total_vehicles = db.query(Vehicle).count()

    available_drivers = db.query(Driver).filter(
        Driver.status == "Available"
    ).count()

    active_trips = db.query(Trip).filter(
        Trip.status == "Dispatched"
    ).count()

    maintenance_due = db.query(Maintenance).filter(
        Maintenance.status == "Pending"
    ).count()

    recent_trips = db.query(Trip).order_by(
        Trip.id.desc()
    ).limit(5).all()

    maintenance_list = db.query(Maintenance).filter(
        Maintenance.status == "Pending"
    ).limit(5).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total_vehicles": total_vehicles,
            "available_drivers": available_drivers,
            "active_trips": active_trips,
            "maintenance_due": maintenance_due,
            "recent_trips": recent_trips,
            "maintenance_list": maintenance_list
        }
    )


@router.get("/vehicles", response_class=HTMLResponse)
def vehicles(request: Request, db: Session = Depends(get_db)):

    vehicles = db.query(Vehicle).all()

    return templates.TemplateResponse(
        "vehicles/list.html",
        {
            "request": request,
            "vehicles": vehicles
        }
    )


@router.get("/vehicles/add", response_class=HTMLResponse)
def add_vehicle(request: Request):

    return templates.TemplateResponse(
        "vehicles/add.html",
        {
            "request": request
        }
    )


@router.get("/vehicles/{vehicle_id}/edit", response_class=HTMLResponse)
def edit_vehicle(
    vehicle_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    return templates.TemplateResponse(
        "vehicles/edit.html",
        {
            "request": request,
            "vehicle": vehicle
        }
    )


@router.get("/drivers", response_class=HTMLResponse)
def drivers(request: Request, db: Session = Depends(get_db)):

    drivers = db.query(Driver).all()

    return templates.TemplateResponse(
        "drivers/list.html",
        {
            "request": request,
            "drivers": drivers
        }
    )


@router.get("/drivers/add", response_class=HTMLResponse)
def add_driver(request: Request):

    return templates.TemplateResponse(
        "drivers/add.html",
        {
            "request": request
        }
    )


@router.get("/drivers/{driver_id}/edit", response_class=HTMLResponse)
def edit_driver(
    driver_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    return templates.TemplateResponse(
        "drivers/edit.html",
        {
            "request": request,
            "driver": driver
        }
    )


@router.get("/trips", response_class=HTMLResponse)
def trips(request: Request, db: Session = Depends(get_db)):

    trips = db.query(Trip).all()

    return templates.TemplateResponse(
        "trips/list.html",
        {
            "request": request,
            "trips": trips
        }
    )


@router.get("/trips/create", response_class=HTMLResponse)
def create_trip(request: Request, db: Session = Depends(get_db)):

    vehicles = db.query(Vehicle).filter(
        Vehicle.status == "Available"
    ).all()

    drivers = db.query(Driver).filter(
        Driver.status == "Available"
    ).all()

    return templates.TemplateResponse(
        "trips/create.html",
        {
            "request": request,
            "vehicles": vehicles,
            "drivers": drivers
        }
    )


@router.get("/trips/{trip_id}", response_class=HTMLResponse)
def trip_details(
    trip_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    return templates.TemplateResponse(
        "trips/details.html",
        {
            "request": request,
            "trip": trip
        }
    )


@router.get("/maintenance", response_class=HTMLResponse)
def maintenance(request: Request, db: Session = Depends(get_db)):

    maintenance_records = db.query(
        Maintenance
    ).all()

    return templates.TemplateResponse(
        "maintenance/list.html",
        {
            "request": request,
            "maintenance_records": maintenance_records
        }
    )


@router.get("/maintenance/create", response_class=HTMLResponse)
def create_maintenance(
    request: Request,
    db: Session = Depends(get_db)
):

    vehicles = db.query(Vehicle).all()

    return templates.TemplateResponse(
        "maintenance/create.html",
        {
            "request": request,
            "vehicles": vehicles
        }
    )


@router.get("/reports", response_class=HTMLResponse)
def reports(request: Request):

    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request
        }
    )


@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request):

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request
        }
    )