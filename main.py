from jotform_connection import Appointment, get_appointments
from dotenv import load_dotenv
import dataclasses
import itertools
from tabulate import tabulate
import os
from dmc_connection import sendConfirmation

def print_table(apps):
    headers = [f.name for f in dataclasses.fields(apps[0])]
    rows = [list(dataclasses.astuple(app)) for app in apps]
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    return

def list_of_duplicates(appointments:list[Appointment]):
    to_be_removed:list[Appointment] = list()
    for a, b in itertools.combinations(appointments, 2):
        if a.alias == b.alias:
            if a.phone_number == b.phone_number:
                to_be_removed.append(min(a, b, key=lambda x: x.time))
            else:
                a.duplicate = True
                b.duplicate = True
    return to_be_removed

def main():
    load_dotenv()

    appointments:list[Appointment] = get_appointments()
    unique_appointments = [x for x in appointments if x not in list_of_duplicates(appointments)]

    print_table(unique_appointments)

    if os.getenv('SEND_CONFIRMATIONS', "false").lower() == "true":
        sendConfirmation(unique_appointments)

if __name__ == "__main__":
    main()
