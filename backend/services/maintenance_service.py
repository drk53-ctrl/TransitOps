from sqlalchemy.orm import Session
from datetime import date, timedelta

from backend.model import Maintenance, Vehicle


def create_maintenance_service(
    db: Session,
    data
):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == data.vehicle_id
    ).first()

    if not vehicle:
        return None, "Vehicle not found"


    maintenance = Maintenance(
        **data.model_dump()
    )


    vehicle.status = "Maintenance"


    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)


    return maintenance, None



def complete_maintenance_service(
    db: Session,
    maintenance_id: int
):

    maintenance = db.query(Maintenance).filter(
        Maintenance.id == maintenance_id
    ).first()


    if not maintenance:
        return None, "Maintenance record not found"


    vehicle = db.query(Vehicle).filter(
        Vehicle.id == maintenance.vehicle_id
    ).first()


    maintenance.status = "Completed"


    if vehicle:
        vehicle.status = "Available"


    db.commit()
    db.refresh(maintenance)


    return maintenance, None



def get_vehicle_maintenance_service(
    db: Session,
    vehicle_id: int
):

    return db.query(Maintenance).filter(
        Maintenance.vehicle_id == vehicle_id
    ).order_by(
        Maintenance.id.desc()
    ).all()



def get_pending_maintenance_service(
    db: Session
):

    return db.query(Maintenance).filter(
        Maintenance.status == "Pending"
    ).all()



def get_upcoming_service(
    db: Session,
    days: int = 30
):

    limit = date.today() + timedelta(days=days)

    return db.query(Maintenance).filter(
        Maintenance.next_service_date <= limit
    ).all()



def calculate_maintenance_cost(
    db: Session
):

    records = db.query(Maintenance).all()

    total = sum(
        record.cost for record in records
        if record.cost
    )

    return {
        "total_maintenance_cost": total
    }