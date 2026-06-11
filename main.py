from jotform_connection import *
import dataclasses
import itertools
from tabulate import tabulate
from dmc_connection import *

def print_table(apps):
    headers = [f.name for f in dataclasses.fields(apps[0])]
    rows = [list(dataclasses.astuple(app)) for app in apps]
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    return

def list_of_duplicates(appointments:list[appointment]):
    to_be_removed:list[appointment] = list()
    for a, b in itertools.combinations(appointments, 2):
        if a.alias == b.alias:
            if a.phone_number==b.phone_number:
                to_be_removed.append(min(a, b, key=lambda x: x.time))
            else:
                a.duplicate = True
                b.duplicate = True
    return to_be_removed

def main():
    appointments:list[appointment]= prepare_data(get_submissions())
    unique_appointments = [x for x in appointments if x not in list_of_duplicates(appointments)]
    for confirmation_slot, app in enumerate(unique_appointments, start=1):
        app.confirmation_number = confirmation_slot
    sendConfirmation(unique_appointments)
