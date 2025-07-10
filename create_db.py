from ext import app, db
from models import User

with app.app_context():
    db.drop_all()
    db.create_all()

    existing_admin = User.query.filter_by(username="Admin").first()
    if not existing_admin:
        admin = User(
            username="Admin",
            password="Adminpass",
            first_name="sesili",
            last_name="sulkhanishvili",
            gender="მდედრობითი",
            role="Admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin მომხმარებელი დაემატა")