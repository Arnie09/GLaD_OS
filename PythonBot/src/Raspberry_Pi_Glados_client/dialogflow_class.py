import os
import sys
import dialogflow_v2
from google.api_core.exceptions import InvalidArgument

class DialogFlow():

    def __init__(self,text):
        self.text_to_be_analyzed = text
        self.response = ""
        self.run()

    def run(self):
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(sys.path[0],'GLaD-OS-99f13c598280.json')

        DIALOGFLOW_PROJECT_ID = 'glad-os-vuaplf'
        DIALOGFLOW_LANGUAGE_CODE = 'en-US'
        GOOGLE_APPLICATION_CREDENTIALS = os.path.join(sys.path[0],'GLaD-OS-99f13c598280.json')
        SESSION_ID = 'current-user-id'

        session_client = dialogflow_v2.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

        text_input = dialogflow_v2.types.TextInput(text=self.text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow_v2.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise

        
        self.response =  response.query_result.fulfillment_text

# obj = DialogFlow("ashvdhvasjhdva")
# print(obj.response)