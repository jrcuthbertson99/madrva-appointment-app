from jotform import JotformAPIClient
from datetime import datetime
from dataclasses import dataclass
import json

import os
from dotenv import load_dotenv

@dataclass
class Appointment:
    confirmation_number:int
    alias:str
    phone_number:str
    email:str
    time:datetime
    household_size:int
    assistance_required:bool
    add_to_communications:bool
    additional_questions:str
    duplicate:bool
    def __post_init__(self):
        if self.additional_questions is None:
            self.additional_questions = ""

    def to_dict(self):
        return {
            "confirmation_number": self.confirmation_number,
            "alias": self.alias,
            "phone_number": self.phone_number,
            "email": self.email,
            "time": self.time.isoformat(),
            "household_size": self.household_size,
            "assistance_required": self.assistance_required,
            "add_to_communications": self.add_to_communications,
            "additional_questions": self.additional_questions,
            "duplicate": self.duplicate
        }

def get_appointments() -> list[Appointment]:
    form_id = os.getenv('JOTFORM_FORM_ID')
    client = JotformAPIClient(os.environ['JOTFORM_API_KEY'])

    submissions = client.get_form_submissions(form_id)

    return map_appointments(submissions)

def map_appointments(submissions) -> list[Appointment]:
    appointments = []
    for s in submissions:
        answers = s["answers"]

        appt = Appointment(
            confirmation_number=int(get_value_by_name("uniqueId", answers)),
            alias=get_value_by_name("pleaseEnter", answers),
            phone_number=get_value_by_name("phoneNumber", answers)["full"],
            email=get_value_by_name("emailAddress", answers),
            time=to_time(get_value_by_name("whatDate13", answers)["date"]),
            household_size=to_int(get_value_by_name("howMany", answers), default=1),
            assistance_required=parse_yes_no(get_value_by_name("willYou", answers), default=False),
            add_to_communications=parse_yes_no(get_value_by_name("canWe", answers), default=False),
            additional_questions=get_value_by_name("doYou", answers),
            duplicate=False
        )

        appointments.append(appt)

    return appointments

def to_int(value: str, default: int | None = None) -> int | None:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def to_time(value: str, default: datetime | None = None) -> datetime | None:
    format = "%Y-%m-%d %H:%M"
    try:
        return datetime.strptime(value, format)
    except (ValueError, TypeError) as e:
        return default

def get_value_by_name(name:str, items: dict[str, str]) -> str | None:
    return next((v for k, v in items.items() if v['name'] == name), {}).get('answer', None)


def parse_yes_no(value: str, default: bool | None = None) -> bool | None:
    if value is None:
        return default

    if "yes" in value.strip().lower():
        return True

    if "no" in value.strip().lower():
        return False

    return default

def main():
    load_dotenv()

    print(json.dumps([appt.to_dict() for appt in get_appointments()], indent=2))
    return

if __name__ == "__main__":
    main()
