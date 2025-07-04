from app import create_app, db
from app.models import FitnessClass
from app.utils import ist_to_utc

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    seed_classes = [
        FitnessClass(name="Yoga", datetime_utc=ist_to_utc("2025-07-01 10:00"), instructor="Alice", available_slots=10),
        FitnessClass(name="Zumba", datetime_utc=ist_to_utc("2025-07-02 12:00"), instructor="Bob", available_slots=8),
        FitnessClass(name="HIIT", datetime_utc=ist_to_utc("2025-07-03 09:00"), instructor="Charlie", available_slots=5),
    ]

    db.session.bulk_save_objects(seed_classes)
    db.session.commit()
    print("Seed data added.")
