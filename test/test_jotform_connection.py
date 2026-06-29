
import json
from jotform_connection import map_appointments, to_int, to_time, parse_yes_no, get_value_by_name
from datetime import datetime


def load_example_submissions() -> list[dict]:
    # Load example submissions from a JSON file for testing purposes
    with open('test/example/submissions.json', 'r') as f:
        submissions = json.load(f)
    return submissions


def test_map_appointments():
    appts = map_appointments(load_example_submissions())
    assert len(appts) == 1
    assert appts[0].confirmation_number == 513
    assert appts[0].alias == "John Public"
    assert appts[0].phone_number == "(804) 555-0100"
    assert appts[0].email == "john.public@example.com"
    assert appts[0].time.isoformat() == "2026-06-27T07:00:00"
    assert appts[0].household_size == 1
    assert appts[0].assistance_required is False
    assert appts[0].add_to_communications is False

def test_to_int():
    assert to_int("5") == 5
    assert to_int("abc", default=0) == 0
    assert to_int(None, default=10) == 10

def test_to_time():
    assert to_time("2026-06-27 07:00").isoformat() == "2026-06-27T07:00:00"
    assert to_time("invalid", default=datetime(2020, 1, 1)).isoformat() == "2020-01-01T00:00:00"
    assert to_time(None, default=datetime(2021, 1, 1)).isoformat() == "2021-01-01T00:00:00"

def test_parse_yes_no():
    assert parse_yes_no("Yes") is True
    assert parse_yes_no("No") is False
    assert parse_yes_no("yes") is True
    assert parse_yes_no("no") is False
    assert parse_yes_no("maybe", default=True) is True
    assert parse_yes_no(None, default=False) is False

def test_get_value_by_name():
    submissions = load_example_submissions()
    answers = submissions[0]["answers"]
    assert get_value_by_name("uniqueId", answers) == "0513"
    assert get_value_by_name("pleaseEnter", answers) == "John Public"
    assert get_value_by_name("invalid", answers) == None

