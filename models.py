from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ENV.env import DATABASE_URL

Base = declarative_base()

class Prompt(Base):
    """Database model for system prompts"""
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserProfile(Base):
    """Database model for user nutrition profiles"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    age = Column(Integer, nullable=True)
    sports = Column(Boolean, default=False)
    allergies = Column(String, nullable=True)
    budget = Column(Integer, nullable=True)
    goal = Column(String, nullable=True)  # lose_weight, stay_fit, balanced, family_menu
    preferences = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MealPlan(Base):
    """Database model for meal plans"""
    __tablename__ = "meal_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    plan_content = Column(String, nullable=False)
    duration = Column(String)  # week, month
    created_at = Column(DateTime, default=datetime.utcnow)


# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
