from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.model import User
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post("/signup")
def signup(
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == email
    ).first()


    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    user = User(
        email=email,
        password=hash_password(password),
        role=role
    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return RedirectResponse(
        url="/",
        status_code=303
    )



@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == username
    ).first()


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )



    if not verify_password(
        password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )



    token = create_access_token(
        {
            "email": user.email,
            "role": user.role
        }
    )


    response = RedirectResponse(
        url="/dashboard",
        status_code=303
    )


    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )


    return response



@router.get("/logout")
def logout():

    response = RedirectResponse(
        url="/",
        status_code=303
    )


    response.delete_cookie(
        "access_token"
    )


    return response