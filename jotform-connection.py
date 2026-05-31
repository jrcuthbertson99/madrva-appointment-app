from jotform import *
from typing import Any

def get_Submissions()->Any:
     jotformAPIClient = JotformAPIClient('YOUR API KEY')
     forms = jotformAPIClient.get_forms(None, 1, None, None)
     latestForm = forms[0]
     latestFormID = latestForm["id"]
     submissions = jotformAPIClient.get_form_submissions(latestFormID)
     print(type(submissions))
     print(submissions)
     return submissions
