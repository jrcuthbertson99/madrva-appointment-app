import dialmycalls_client
from dialmycalls_client.rest import ApiException
from jotform_connection import Appointment
import os
from dotenv import load_dotenv

def sendConfirmation(confirmed:list[Appointment]):
    load_dotenv()
    dialmycalls_client.configuration.api_key['X-Auth-ApiKey'] = os.environ['DIAL_MY_CALLS_API_KEY']
    api = dialmycalls_client.TextsApi()
    kw_id=dialmycalls_client.KeywordsApi().get_keywords()[0].id
    for app in confirmed:
        confirmation_message:str = f'Your appointment for {app.time} has been confirmed. Your confirmation number is {app.confirmation_number}'
        params = dialmycalls_client.CreateTextParameters(
                name='',
                keyword_id=kw_id,
                messages =[confirmation_message],
                send_immediately=True,
                contacts=[dialmycalls_client.ContactAttributes(phone=app.phone_number)]
        )
        try:
            resp = api.create_text(params)
            print(resp)
        except ApiException as e:
            print(f'create_text failed: {e}')
    return
