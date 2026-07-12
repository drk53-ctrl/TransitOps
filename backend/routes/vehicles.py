from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.model import Vehicle
from backend.schemas import VehicleCreate, VehicleUpdate, VehicleOut

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


@router.get("", response_model=list[VehicleOut])
def get_vehicles(db: Session = Depends(get_db)):

    return db.query(Vehicle).order_by(
        Vehicle.id.desc()
    ).all()


@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(
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

    return vehicle


@router.post("", response_model=VehicleOut)
def create_vehicle(
    data: VehicleCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Vehicle).filter(
        Vehicle.vehicle_number == data.vehicle_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Vehicle number already exists."
        )

    vehicle = Vehicle(
        **data.model_dump()
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(
    vehicle_id: int,
    data: VehicleUpdate,
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

    values = data.model_dump(
        exclude_unset=True
    )

    for key, value in values.items():
        setattr(vehicle, key, value)

    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.delete("/{vehicle_id}")
def delete_vehicle(
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

    db.delete(vehicle)
    db.commit()

    return {
        "message": "Vehicle deleted successfully."
    }


@router.get("/status/available")
def available_vehicles(
    db: Session = Depends(get_db)
):

    vehicles = db.query(Vehicle).filter(
        Vehicle.status == "Available"
    ).all()

    return vehicles


@router.get("/status/maintenance")
def maintenance_vehicles(
    db: Session = Depends(get_db)
):

    vehicles = db.query(Vehicle).filter(
        Vehicle.status == "Maintenance"
    ).all()

    return vehicles


@router.put("/{vehicle_id}/status")
def update_vehicle_status(
    vehicle_id: int,
    status: str,
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

    vehicle.status = status

    db.commit()

    return {
        "message": "Vehicle status updated successfully."
    }