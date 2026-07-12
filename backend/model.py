from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="User"
    )


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_number = Column(
        String,
        unique=True,
        nullable=False
    )

    vehicle_type = Column(
        String,
        nullable=False
    )

    model = Column(
        String
    )

    year = Column(
        Integer
    )

    capacity = Column(
        Integer
    )

    status = Column(
        String,
        default="Available"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    trips = relationship(
        "Trip",
        back_populates="vehicle"
    )

    maintenance = relationship(
        "Maintenance",
        back_populates="vehicle"
    )

    fuel_records = relationship(
        "Fuel",
        back_populates="vehicle"
    )



class Driver(Base):
    __tablename__ = "drivers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    phone = Column(
        String
    )

    license_number = Column(
        String,
        unique=True,
        nullable=False
    )

    license_expiry = Column(
        Date
    )

    status = Column(
        String,
        default="Available"
    )


    trips = relationship(
        "Trip",
        back_populates="driver"
    )



class Trip(Base):
    __tablename__ = "trips"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id")
    )

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id")
    )

    source = Column(
        String,
        nullable=False
    )

    destination = Column(
        String,
        nullable=False
    )

    start_time = Column(
        DateTime
    )

    end_time = Column(
        DateTime
    )

    distance = Column(
        Float
    )

    status = Column(
        String,
        default="Running"
    )


    vehicle = relationship(
        "Vehicle",
        back_populates="trips"
    )

    driver = relationship(
        "Driver",
        back_populates="trips"
    )



class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id")
    )

    description = Column(
        String
    )

    service_date = Column(
        Date
    )

    next_service_date = Column(
        Date
    )

    cost = Column(
        Float
    )

    status = Column(
        String,
        default="Pending"
    )


    vehicle = relationship(
        "Vehicle",
        back_populates="maintenance"
    )



class Fuel(Base):
    __tablename__ = "fuel"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id")
    )

    quantity = Column(
        Float
    )

    cost = Column(
        Float
    )

    date = Column(
        Date,
        default=datetime.utcnow
    )


    vehicle = relationship(
        "Vehicle",
        back_populates="fuel_records"
    )



class Expense(Base):
    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    category = Column(
        String
    )

    description = Column(
        String
    )

    amount = Column(
        Float
    )

    date = Column(
        Date
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )