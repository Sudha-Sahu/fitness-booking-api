from flask import Blueprint, request, jsonify
from . import db
from .models import FitnessClass, Booking
from .utils import utc_to_timezone
from sqlalchemy.exc import SQLAlchemyError
import pytz

bp = Blueprint("api", __name__)

@bp.route("/classes", methods=["GET"])
def get_classes():
    timezone = request.args.get("tz", "Asia/Kolkata")
    classes = FitnessClass.query.all()
    output = []
    for cls in classes:
        local_time = utc_to_timezone(cls.datetime_utc, timezone)
        output.append({
            "id": cls.id,
            "name": cls.name,
            "datetime": local_time.strftime("%Y-%m-%d %H:%M"),
            "instructor": cls.instructor,
            "available_slots": cls.available_slots
        })
    return jsonify(output)

@bp.route("/book", methods=["POST"])
def book_class():
    data = request.get_json()
    required = {"class_id", "client_name", "client_email"}
    if not data or not required.issubset(data.keys()):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        class_obj = FitnessClass.query.get(data["class_id"])
        if not class_obj:
            return jsonify({"error": "Class not found"}), 404

        if class_obj.available_slots <= 0:
            return jsonify({"error": "No available slots"}), 400

        booking = Booking(
            class_id=class_obj.id,
            client_name=data["client_name"],
            client_email=data["client_email"]
        )

        class_obj.available_slots -= 1
        db.session.add(booking)
        db.session.commit()

        return jsonify({"message": "Booking successful", "booking_id": booking.id}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Booking failed"}), 500

@bp.route("/bookings", methods=["GET"])
def get_bookings():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    bookings = Booking.query.filter_by(client_email=email).all()
    results = []
    for b in bookings:
        cls = FitnessClass.query.get(b.class_id)
        results.append({
            "booking_id": b.id,
            "class": cls.name,
            "datetime": utc_to_timezone(cls.datetime_utc, "Asia/Kolkata").strftime("%Y-%m-%d %H:%M"),
            "instructor": cls.instructor
        })
    return jsonify(results)
