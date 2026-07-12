from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.model import Driver
from backend.schemas import DriverCreate, DriverUpdate, DriverOut

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


@router.get("", response_model=list[DriverOut])
def get_drivers(
    db: Session = Depends(get_db)
):

    return db.query(Driver).order_by(
        Driver.id.desc()
    ).all()


@router.get("/{driver_id}", response_model=DriverOut)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return driver


@router.post("", response_model=DriverOut)
def create_driver(
    data: DriverCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Driver).filter(
        Driver.license_number == data.license_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="License number already exists."
        )

    driver = Driver(
        **data.model_dump()
    )

    db.add(driver)
    db.commit()
    db.refresh(driver)

    return driver


@router.put("/{driver_id}", response_model=DriverOut)
def update_driver(
    driver_id: int,
    data: DriverUpdate,
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    values = data.model_dump(
        exclude_unset=True
    )

    for key, value in values.items():
        setattr(driver, key, value)

    db.commit()
    db.refresh(driver)

    return driver


@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    db.delete(driver)
    db.commit()

    return {
        "message": "Driver deleted successfully."
    }


@router.get("/status/available")
def available_drivers(
    db: Session = Depends(get_db)
):

    return db.query(Driver).filter(
        Driver.status == "Available"
    ).all()


@router.get("/status/on-trip")
def busy_drivers(
    db: Session = Depends(get_db)
):

    return db.query(Driver).filter(
        Driver.status == "On Trip"
    ).all()


@router.put("/{driver_id}/status")
def update_driver_status(
    driver_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    driver = db.query(Driver).filter(
        Driver.id == driver_id
    ).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    driver.status = status

    db.commit()

    return {
        "message": "Driver status updated successfully."
    }


@router.get("/license/expired")
def expired_licenses(
    db: Session = Depends(get_db)
):

    from datetime import date

    return db.query(Driver).filter(
        Driver.license_expiry < date.today()
    ).all()


@router.get("/license/expiring")
def expiring_licenses(
    days: int = 30,
    db: Session = Depends(get_db)
):

    from datetime import date, timedelta

    limit = date.today() + timedelta(days=days)

    return db.query(Driver).filter(
        Driver.license_expiry <= limit
    ).all()