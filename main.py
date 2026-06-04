from jotform_connection import *
import dataclasses
import itertools
from tabulate import tabulate

def deduplicate(appointments:list[appointment]):
    to_be_removed:list[appointment] = list()
    for a, b in itertools.combinations(appointments, 2):
        if a.alias == b.alias and a.phone_number == b.phone_number and a.email==b.email:
            to_be_removed.append(min(a, b, key=lambda x: x.time))
    print(to_be_removed)
    return to_be_removed

appointments:list[appointment] = prepare_data(get_submissions())
unique_appointments = [x for x in appointments where x not in deduplicate(appointments)]

def print_table(apps):
    headers = [f.name for f in dataclasses.fields(apps[0])]
    rows = [list(dataclasses.astuple(app)) for app in apps]
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    return

