from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models import User, OtpLog
from app.schemas import RegisterRequest, LoginRequest, OtpVerifyRequest
from app.utils.auth import generate_otp, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    if not data.email and not data.mobile:
        raise HTTPException(400, "Email or mobile is required")

    query = db.query(User)

    if data.email:
        query = query.filter(User.email == data.email)
    if data.mobile:
        query = query.filter(User.mobile == data.mobile)

    if query.first():
        raise HTTPException(400, "User already registered")

    user = User(name=data.name, email=data.email, mobile=data.mobile)
    db.add(user)
    db.commit()
    db.refresh(user)

    otp = generate_otp()
    db.add(OtpLog(
        user_id=user.id,
        otp=otp,
        expiry=datetime.utcnow() + timedelta(minutes=5)
    ))
    db.commit()

    print("OTP:", otp)
    return {"message": "OTP sent", "user_id": user.id}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    if not data.email and not data.mobile:
        raise HTTPException(400, "Email or mobile is required")

    query = db.query(User)
    if data.email:
        query = query.filter(User.email == data.email)
    if data.mobile:
        query = query.filter(User.mobile == data.mobile)

    user = query.first()

    if not user:
        raise HTTPException(404, "User not found")

    otp = generate_otp()
    db.add(OtpLog(
        user_id=user.id,
        otp=otp,
        expiry=datetime.utcnow() + timedelta(minutes=5)
    ))
    db.commit()

    print("OTP:", otp)
    return {"message": "OTP sent", "user_id": user.id}


@router.post("/verify-otp")
def verify(data: OtpVerifyRequest, db: Session = Depends(get_db)):
    record = db.query(OtpLog).filter(
        OtpLog.user_id == data.user_id,
        OtpLog.otp == data.otp,
        OtpLog.is_used == 0,
        OtpLog.expiry > datetime.utcnow()
    ).first()

    if not record:
        raise HTTPException(400, "Invalid OTP")

    record.is_used = 1
    user = db.query(User).filter(User.id == data.user_id).first()
    user.is_verified = 1
    db.commit()

    token = create_access_token({"user_id": user.id})
    return {"token": token, "user": {"id": user.id, "name": user.name}}
