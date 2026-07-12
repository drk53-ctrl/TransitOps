from sqlalchemy.orm import Session
from datetime import datetime

from backend.model import Trip, Vehicle, Driver


def create_trip_service(
    db: Session,
    data
):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == data.vehicle_id
    ).first()

    if not vehicle:
        return None, "Vehicle not found"


    driver = db.query(Driver).filter(
        Driver.id == data.driver_id
    ).first()

    if not driver:
        return None, "Driver not found"


    if vehicle.status != "Available":
        return None, "Vehicle is not available"


    if driver.status != "Available":
        return None, "Driver is not available"


    trip = Trip(
        **data.model_dump(),
        start_time=datetime.now()
    )


    vehicle.status = "On Trip"
    driver.status = "On Trip"


    db.add(trip)
    db.commit()
    db.refresh(trip)


    return trip, None



def complete_trip_service(
    db: Session,
    trip_id: int
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()


    if not trip:
        return None, "Trip not found"


    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip.vehicle_id
    ).first()


    driver = db.query(Driver).filter(
        Driver.id == trip.driver_id
    ).first()


    trip.status = "Completed"
    trip.end_time = datetime.now()


    if vehicle:
        vehicle.status = "Available"


    if driver:
        driver.status = "Available"


    db.commit()
    db.refresh(trip)


    return trip, None



def cancel_trip_service(
    db: Session,
    trip_id: int
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()


    if not trip:
        return None, "Trip not found"


    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip.vehicle_id
    ).first()


    driver = db.query(Driver).filter(
        Driver.id == trip.driver_id
    ).first()


    trip.status = "Cancelled"


    if vehicle:
        vehicle.status = "Available"


    if driver:
        driver.status = "Available"


    db.commit()
    db.refresh(trip)


    return trip, None



def get_active_trips_service(
    db: Session
):

    return db.query(Trip).filter(
        Trip.status == "Running"
    ).all()



def get_completed_trips_service(
    db: Session
):

    return db.query(Trip).filter(
        Trip.status == "Completed"
    ).all()