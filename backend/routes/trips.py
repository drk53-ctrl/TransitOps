from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from backend.database import get_db
from backend.model import Trip, Vehicle, Driver
from backend.schemas import TripCreate, TripUpdate, TripOut

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)

@router.get("/", response_model=list[TripOut])
def get_trips(db: Session = Depends(get_db)):
    return db.query(Trip).all()

@router.get("/{trip_id}", response_model=TripOut)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    return trip

@router.post("/", response_model=TripOut)
def create_trip(data: TripCreate, db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == data.vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    driver = db.query(Driver).filter(
        Driver.id == data.driver_id
    ).first()

    if not driver:
        raise HTTPException(404, "Driver not found")

    if vehicle.status != "Available":
        raise HTTPException(
            400,
            "Vehicle is not available."
        )

    if driver.status != "Available":
        raise HTTPException(
            400,
            "Driver is not available."
        )

    if driver.license_expiry < date.today():
        raise HTTPException(
            400,
            "Driver license expired."
        )

    if data.cargo_weight > vehicle.capacity:
        raise HTTPException(
            400,
            "Cargo exceeds vehicle capacity."
        )

    trip = Trip(
        **data.model_dump(),
        status="Draft"
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return trip

@router.post("/{trip_id}/dispatch")
def dispatch_trip(trip_id: int, db: Session = Depends(get_db)):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(404, "Trip not found")

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip.vehicle_id
    ).first()

    driver = db.query(Driver).filter(
        Driver.id == trip.driver_id
    ).first()

    vehicle.status = "On Trip"
    driver.status = "On Trip"
    trip.status = "Dispatched"

    db.commit()

    return {"message": "Trip dispatched successfully."}

@router.post("/{trip_id}/complete")
def complete_trip(
    trip_id: int,
    final_odometer: float,
    fuel_used: float,
    db: Session = Depends(get_db)
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(404, "Trip not found")

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip.vehicle_id
    ).first()

    driver = db.query(Driver).filter(
        Driver.id == trip.driver_id
    ).first()

    trip.status = "Completed"
    trip.actual_distance = final_odometer - vehicle.odometer
    trip.end_odometer = final_odometer
    trip.fuel_used = fuel_used

    vehicle.odometer = final_odometer
    vehicle.status = "Available"

    driver.status = "Available"

    db.commit()

    return {"message": "Trip completed successfully."}

@router.post("/{trip_id}/cancel")
def cancel_trip(trip_id: int, db: Session = Depends(get_db)):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(404, "Trip not found")

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip.vehicle_id
    ).first()

    driver = db.query(Driver).filter(
        Driver.id == trip.driver_id
    ).first()

    trip.status = "Cancelled"

    vehicle.status = "Available"
    driver.status = "Available"

    db.commit()

    return {"message": "Trip cancelled successfully."}

@router.put("/{trip_id}", response_model=TripOut)
def update_trip(
    trip_id: int,
    data: TripUpdate,
    db: Session = Depends(get_db)
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(404, "Trip not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(trip, key, value)

    db.commit()
    db.refresh(trip)

    return trip

@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:
        raise HTTPException(404, "Trip not found")

    db.delete(trip)
    db.commit()

    return {"message": "Trip deleted successfully."}