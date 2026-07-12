from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: str
    role: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class VehicleBase(BaseModel):
    vehicle_number: str
    vehicle_type: str
    model: Optional[str] = None
    year: Optional[int] = None
    capacity: Optional[int] = None
    status: Optional[str] = "Available"


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    vehicle_number: Optional[str] = None
    vehicle_type: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    capacity: Optional[int] = None
    status: Optional[str] = None


class VehicleOut(VehicleBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DriverBase(BaseModel):
    name: str
    phone: Optional[str] = None
    license_number: str
    license_expiry: Optional[date] = None
    status: Optional[str] = "Available"


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    license_expiry: Optional[date] = None
    status: Optional[str] = None


class DriverOut(DriverBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class TripBase(BaseModel):
    vehicle_id: int
    driver_id: int
    source: str
    destination: str
    distance: Optional[float] = None
    status: Optional[str] = "Running"


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    source: Optional[str] = None
    destination: Optional[str] = None
    distance: Optional[float] = None
    status: Optional[str] = None
    end_time: Optional[datetime] = None


class TripOut(TripBase):
    id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class MaintenanceBase(BaseModel):
    vehicle_id: int
    description: Optional[str] = None
    service_date: Optional[date] = None
    next_service_date: Optional[date] = None
    cost: Optional[float] = None
    status: Optional[str] = "Pending"


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    description: Optional[str] = None
    service_date: Optional[date] = None
    next_service_date: Optional[date] = None
    cost: Optional[float] = None
    status: Optional[str] = None


class MaintenanceOut(MaintenanceBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class FuelBase(BaseModel):
    vehicle_id: int
    quantity: float
    cost: float
    x_date: Optional[date] = None


class FuelCreate(FuelBase):
    pass


class FuelUpdate(BaseModel):
    quantity: Optional[float] = None
    cost: Optional[float] = None
    x_date: Optional[date] = None


class FuelOut(FuelBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class ExpenseBase(BaseModel):
    category: str
    description: Optional[str] = None
    amount: float
    x_date: date


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    x_date: Optional[date] = None


class ExpenseOut(ExpenseBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )