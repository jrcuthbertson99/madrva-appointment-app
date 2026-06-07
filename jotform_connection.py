from jotform import JotformAPIClient
from typing import Any
from datetime import datetime
from dataclasses import dataclass
import zoneinfo


@dataclass
class appointment:
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

def get_submissions()->Any:
     jotformAPIClient = JotformAPIClient('xxx')
     forms = jotformAPIClient.get_forms(None, 1, None, None)
     latestForm = forms[0]
     latestFormID = latestForm["id"]
     submissions = jotformAPIClient.get_form_submissions(latestFormID)
     answers = [submission["answers"] for submission in submissions] 
     answers = [{k: v for k, v in item.items() if k != "1" and k!="2"} for item in answers]
     return answers

def parse_and_localize(dt_str: str, tz_name: str = "America/New_York") -> datetime:
    dt = datetime.fromisoformat(dt_str)
    return dt.replace(tzinfo=zoneinfo.ZoneInfo(tz_name))

def parse_yes_no(value: str) -> bool:
    if value.strip().lower() == "yes":
        return True
    elif value.strip().lower() == "no":
        return False
    else:
        raise ValueError(f"Expected 'Yes' or 'No', got: {value!r}")

def prepare_data(submissions:list[dict])->list[appointment]:
    appointments:list[appointment]=list()
    for submission in submissions:
        if "answer" not in submission["10"]:
            submission["10"]["answer"] = ""
        app=appointment(0,submission["3"]["prettyFormat"],submission["4"]["answer"],submission["5"]["prettyFormat"],parse_and_localize(submission["6"]["answer"]["date"]),submission["7"]["answer"],parse_yes_no(submission["8"]["answer"]),parse_yes_no(submission["9"]["answer"]),submission["10"]["answer"],False)
        appointments.append(app)
    return appointments

def main():
    print(prepare_data(get_submissions()))
    return
if __name__ == "__main__":
    main()
    
