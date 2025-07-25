from app.core.config import settings
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.auth import get_password_hash

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if we have any users
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        user = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            full_name="Admin",
            is_superuser=True,
            balance=1000.0  # Initial balance for testing
        )
        db.add(user)
        db.commit()
        print("Created first superuser")
    else:
        print("Superuser already exists")
    
    db.close()

if __name__ == "__main__":
    print("Creating initial data")
    init_db()
    print("Initial data created")
