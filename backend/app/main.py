import datetime
import os
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./habit.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    habits = relationship("Habit", back_populates="owner")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    frequency = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="habits")
    completions = relationship("HabitCompletion", back_populates="habit")


class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date, default=datetime.date.today)

    habit = relationship("Habit", back_populates="completions")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    name: str
    email: str


class UserRead(UserCreate):
    id: int

    class Config:
        orm_mode = True


class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    frequency: str
    user_id: int


class HabitRead(HabitCreate):
    id: int

    class Config:
        orm_mode = True


class TrackingCreate(BaseModel):
    habit_id: int
    date: datetime.date


class TrackingRead(BaseModel):
    id: int
    habit_id: int
    date: datetime.date

    class Config:
        orm_mode = True


app = FastAPI(title="Habit Tracker API")


@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/habits", response_model=HabitRead)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == habit.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_habit = Habit(
        title=habit.title,
        description=habit.description,
        frequency=habit.frequency,
        user_id=habit.user_id,
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


@app.get("/habits", response_model=List[HabitRead])
def list_habits(db: Session = Depends(get_db)):
    return db.query(Habit).all()


@app.post("/tracking", response_model=TrackingRead)
def track_habit(tracking: TrackingCreate, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == tracking.habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    record = HabitCompletion(habit_id=tracking.habit_id, date=tracking.date)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/tracking", response_model=List[TrackingRead])
def list_tracking(db: Session = Depends(get_db)):
    return db.query(HabitCompletion).all()
