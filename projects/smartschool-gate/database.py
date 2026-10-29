from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Vehicle(db.Model):
    __tablename__ = "authorized_vehicles"

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(7), unique=True, nullable=False, index=True)
    responsible_name = db.Column(db.String(120), nullable=False)
    student_name = db.Column(db.String(120), nullable=False)
    class_name = db.Column(db.String(40), nullable=False)
    room = db.Column(db.String(40), nullable=True)
    authorized = db.Column(db.Boolean, nullable=False, default=False)


class AccessEvent(db.Model):
    __tablename__ = "access_events"

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(7), nullable=True, index=True)
    status = db.Column(db.String(60), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
