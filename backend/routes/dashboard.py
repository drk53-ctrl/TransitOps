from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.model import Vehicle, Driver, Trip, Maintenance

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard(db: Session = Depends(get_db)):

    total_vehicles = db.query(Vehicle).count()

    available_vehicles = db.query(Vehicle).filter(
        Vehicle.status == "Available"
    ).count()

    maintenance_vehicles = db.query(Vehicle).filter(
        Vehicle.status == "Maintenance"
    ).count()

    available_drivers = db.query(Driver).filter(
        Driver.status == "Available"
    ).count()

    active_trips = db.query(Trip).filter(
        Trip.status == "Dispatched"
    ).count()

    completed_trips = db.query(Trip).filter(
        Trip.status == "Completed"
    ).count()

    pending_maintenance = db.query(Maintenance).filter(
        Maintenance.status == "Pending"
    ).count()

    trip_status = db.query(
        Trip.status,
        func.count(Trip.id)
    ).group_by(
        Trip.status
    ).all()

    vehicle_status = db.query(
        Vehicle.status,
        func.count(Vehicle.id)
    ).group_by(
        Vehicle.status
    ).all()

    recent_trips = db.query(Trip).order_by(
        Trip.id.desc()
    ).limit(5).all()

    upcoming_maintenance = db.query(Maintenance).filter(
        Maintenance.status == "Pending"
    ).order_by(
        Maintenance.scheduled_date
    ).limit(5).all()

    return {
        "summary": {
            "total_vehicles": total_vehicles,
            "available_vehicles": available_vehicles,
            "maintenance_vehicles": maintenance_vehicles,
            "available_drivers": available_drivers,
            "active_trips": active_trips,
            "completed_trips": completed_trips,
            "pending_maintenance": pending_maintenance
        },
        "trip_status": [
            {
                "status": status,
                "count": count
            }
            for status, count in trip_status
        ],
        "vehicle_status": [
            {
                "status": status,
                "count": count
            }
            for status, count in vehicle_status
        ],
        "recent_trips": [
            {
                "id": trip.id,
                "vehicle_id": trip.vehicle_id,
                "driver_id": trip.driver_id,
                "status": trip.status,
                "start_date": trip.start_date,
                "destination": trip.destination
            }
            for trip in recent_trips
        ],
        "upcoming_maintenance": [
            {
                "id": item.id,
                "vehicle_id": item.vehicle_id,
                "issue": item.issue,
                "scheduled_date": item.scheduled_date,
                "status": item.status
            }
            for item in upcoming_maintenance
        ]
    }