from backend.database import init_db, SessionLocal
from backend.models import Profile


print("Starting database test...")

# Create database and tables
init_db()

print("Database tables created successfully!")

# Open database session
db = SessionLocal()

try:
    # Check whether a profile exists
    profile = db.query(Profile).first()

    if profile is None:
        print("No profile found yet.")
    else:
        print("Profile found:")
        print(profile.name)

finally:
    db.close()

print("Database test completed successfully!")