from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from backend.database import get_db
from backend.model import Fuel, Vehicle
from backend.schemas import FuelCreate, FuelUpdate, FuelOut


router = APIRouter(
    prefix="/fuel",
    tags=["Fuel"]
)



@router.get("", response_model=list[FuelOut])
def get_fuel_records(
    db: Session = Depends(get_db)
):

    return db.query(Fuel).order_by(
        Fuel.id.desc()
    ).all()




@router.get("/{fuel_id}", response_model=FuelOut)
def get_fuel(
    fuel_id: int,
    db: Session = Depends(get_db)
):

    fuel = db.query(Fuel).filter(
        Fuel.id == fuel_id
    ).first()

    if not fuel:
        raise HTTPException(
            status_code=404,
            detail="Fuel record not found"
        )

    return fuel



# Add fuel record
@router.post("", response_model=FuelOut)
def create_fuel(
    data: FuelCreate,
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


    fuel = Fuel(
        **data.model_dump()
    )

    db.add(fuel)
    db.commit()
    db.refresh(fuel)

    return fuel



# Update fuel record
@router.put("/{fuel_id}", response_model=FuelOut)
def update_fuel(
    fuel_id: int,
    data: FuelUpdate,
    db: Session = Depends(get_db)
):

    fuel = db.query(Fuel).filter(
        Fuel.id == fuel_id
    ).first()

    if not fuel:
        raise HTTPException(
            status_code=404,
            detail="Fuel record not found"
        )


    values = data.model_dump(
        exclude_unset=True
    )

    for key, value in values.items():
        setattr(fuel, key, value)


    db.commit()
    db.refresh(fuel)

    return fuel



# Delete fuel record
@router.delete("/{fuel_id}")
def delete_fuel(
    fuel_id: int,
    db: Session = Depends(get_db)
):

    fuel = db.query(Fuel).filter(
        Fuel.id == fuel_id
    ).first()

    if not fuel:
        raise HTTPException(
            status_code=404,
            detail="Fuel record not found"
        )


    db.delete(fuel)
    db.commit()


    return {
        "message": "Fuel record deleted successfully."
    }



# Get fuel history of a vehicle
@router.get("/vehicle/{vehicle_id}")
def vehicle_fuel_history(
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


    return db.query(Fuel).filter(
        Fuel.vehicle_id == vehicle_id
    ).order_by(
        Fuel.date.desc()
    ).all()



# Fuel consumed today
@router.get("/today")
def today_fuel(
    db: Session = Depends(get_db)
):

    return db.query(Fuel).filter(
        Fuel.date == date.today()
    ).all()



# Total fuel cost
@router.get("/stats/total-cost")
def total_fuel_cost(
    db: Session = Depends(get_db)
):

    records = db.query(Fuel).all()

    total = sum(
        fuel.cost for fuel in records
    )

    return {
        "total_fuel_cost": total
    }



# Total fuel quantity
@router.get("/stats/total-litres")
def total_fuel_quantity(
    db: Session = Depends(get_db)
):

    records = db.query(Fuel).all()

    total = sum(
        fuel.quantity for fuel in records
    )

    return {
        "total_litres": total
    }