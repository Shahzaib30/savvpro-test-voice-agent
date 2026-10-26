from datetime import datetime
from app.services.booking import ClinicCalendar


def test_booked_slot_is_taken():
    calendar = ClinicCalendar()
    start_time = datetime(2026, 10, 27, 11, 0)
    calendar.book(start_time, "John Doe", "1234567890", "checkup")
    assert calendar.is_taken(start_time) is True