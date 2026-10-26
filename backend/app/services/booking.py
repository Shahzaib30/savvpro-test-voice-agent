from datetime import datetime, time, timedelta

WEEKDAY_NAMES = {
    0 : "Monday",
    1 : "Tuesday",
    2 : "Wednesday",
    3 : "Thursday",
    4 : "Friday",   
    5 : "Saturday",
    6 : "Sunday"
}

OPENING_HOURS = {
    0 : (time(9,0), time(17,0)),
    1 : (time(9,0), time(17,0)),
    2 : (time(9,0), time(17,0)),
    3 : (time(9,0), time(17,0)),
    4 : (time(9,0), time(17,0)),
    5 : (time(9,0), time(17,0)),
    6 : None
}

APPOINTMENT_DURATION = timedelta(minutes=30)
SEARCH_LIMIT = timedelta(days=14)

SERVICES = {
    "checkup": 1500,
    "cleaning": 3000,
    "filling": 4000,
    "root canal": 12000,
    "wisdom tooth extraction": 10000,
}

class SlotTakenError(Exception):
    pass

class ClinicCalendar:
    def __init__(self):
        self.booked_slots: dict[datetime, dict] = {}

    def is_on_grid(self, start_time: datetime) -> bool:
        return start_time.minute % 30 == 0 and start_time.second == 0 and start_time.microsecond == 0
    
    def is_taken(self, start_time: datetime) -> bool:
        return start_time in self.booked_slots
    
    def book(self, start_time: datetime, patient_name: str, patient_phone_number: str, service: str):
        if not self.is_on_grid(start_time):
            raise ValueError("Appointment time must be on the 30-minute grid.")

        if not is_within_opening_hours(start_time):
            raise ValueError("Appointment time is outside of opening hours.")
        
        if self.is_taken(start_time):
            raise SlotTakenError("This time slot is already taken.")
        
        if service not in SERVICES:
            raise ValueError("Invalid service selected.")
        
        self.booked_slots[start_time] = {
            "patient_name": patient_name,
            "patient_phone_number": patient_phone_number,
            "service": service
        }
    def _round_up_to_grid(self, moment: datetime) -> datetime:
        rounded = moment.replace(second=0, microsecond=0)
        leftover_minutes = rounded.minute % 30
        if leftover_minutes !=0:
            rounded += timedelta(minutes=(30 - leftover_minutes))
        return rounded

    def next_available_slot(self, start_time: datetime, count: int = 1) -> datetime:
        slots : list[datetime] = []
        candidate = self._round_up_to_grid(start_time)
        limit = start_time + SEARCH_LIMIT

        while len(slots) < count and candidate < limit:
            if is_within_opening_hours(candidate) and not self.is_taken(candidate):
                slots.append(candidate)
            candidate += APPOINTMENT_DURATION

        if len(slots) == 0:
            raise ValueError("No available slots found.")

        return slots


def is_within_opening_hours(appointment_time: datetime) -> bool:
    opening_hours = OPENING_HOURS.get(appointment_time.weekday())
    if opening_hours is None:
        return False

    open_time, close_time = opening_hours
    appointment_starts = appointment_time.time()
    appointment_ends = (appointment_time + APPOINTMENT_DURATION).time()
    return (
        open_time <= appointment_starts < close_time
        and open_time <= appointment_ends <= close_time
    )


