from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from backend.database import get_db
from backend.model import Maintenance, Vehicle
from backend.schemas import MaintenanceCreate, MaintenanceUpdate, MaintenanceOut


router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


@router.get("", response_model=list[MaintenanceOut])
def get_maintenance(
    db: Session = Depends(get_db)
):

    return db.query(Maintenance).order_by(
        Maintenance.id.desc()
    ).all()


@router.get("/{maintenance_id}", response_model=MaintenanceOut)
def get_maintenance_record(
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    record = db.query(Maintenance).filter(
        Maintenance.id == maintenance_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    return record


@router.post("", response_model=MaintenanceOut)
def create_maintenance(
    data: MaintenanceCreate,
    db: Session = Depends(get_db)
):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == data.vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    maintenance = Maintenance(
        **data.model_dump()
    )

    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)

    return maintenance


@router.put("/{maintenance_id}", response_model=MaintenanceOut)
def update_maintenance(
    maintenance_id: int,
    data: MaintenanceUpdate,
    db: Session = Depends(get_db)
):

    record = db.query(Maintenance).filter(
        Maintenance.id == maintenance_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    values = data.model_dump(
        exclude_unset=True
    )

    for key, value in values.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


@router.delete("/{maintenance_id}")
def delete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    record = db.query(Maintenance).filter(
        Maintenance.id == maintenance_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Maintenance record deleted successfully."
    }


@router.get("/vehicle/{vehicle_id}")
def vehicle_maintenance_history(
    vehicle_id: int,
    db: Session = Depends(get_db)
):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return db.query(Maintenance).filter(
        Maintenance.vehicle_id == vehicle_id
    ).order_by(
        Maintenance.date.desc()
    ).all()


@router.get("/status/pending")
def pending_maintenance(
    db: Session = Depends(get_db)
):

    return db.query(Maintenance).filter(
        Maintenance.status == "Pending"
    ).all()


@router.get("/status/completed")
def completed_maintenance(
    db: Session = Depends(get_db)
):

    return db.query(Maintenance).filter(
        Maintenance.status == "Completed"
    ).all()


@router.get("/upcoming")
def upcoming_maintenance(
    days: int = 30,
    db: Session = Depends(get_db)
):

    from datetime import timedelta

    limit = date.today() + timedelta(days=days)

    return db.query(Maintenance).filter(
        Maintenance.next_service_date <= limit
    ).all()