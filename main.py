from jotform_connection import *
import dataclasses
import itertools
from tabulate import tabulate

def print_table(apps):
    headers = [f.name for f in dataclasses.fields(apps[0])]
    rows = [list(dataclasses.astuple(app)) for app in apps]
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    return

def deduplicate(appointments:list[appointment]):
    to_be_removed:list[appointment] = list()
    for a, b in itertools.combinations(appointments, 2):
        if a.alias == b.alias:
            if a.phone_number==b.phone_number:
                to_be_removed.append(min(a, b, key=lambda x: x.time))
            else:
                a.duplicate = True
                b.duplicate = True
    return to_be_removed

confirmation_slot=1
appointments:list[appointment]= prepare_data(get_submissions())
unique_appointments = [x for x in appointments where x not in deduplicate(appointments)]
for app in unique_appointments:
    appointment.confirmation_number = confirmation_slot
    confirmation_slot +=1
