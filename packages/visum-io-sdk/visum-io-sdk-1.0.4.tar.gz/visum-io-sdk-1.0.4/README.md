## Visum.IO API client

### Installation

```shell
pip install visum-io-sdk
```

### Usage example

```python
from visum_sdk import VisumIOClient, QuestionnaireDTO, DocumentTypes, VisaStatuses


API_KEY = '***'
HOST = 'demo.visum.io'
IS_SANDBOX = True


client = VisumIOClient(
    api_key=API_KEY,
    host=HOST,
    is_sandbox=IS_SANDBOX,
)


## Questionnaire creating
questionnaire: QuestionnaireDTO = client.create_questionnaire(
    DocumentTypes.INDIAN_E_VISA,
    answers={
        'passport_data': {
            'surname': 'Mustermann',
            'name': 'Alex',
        }
    }
)


## Getting questionnaire
new_questionnaire: QuestionnaireDTO = client.get_questionnaire(questionnaire.access_token)

assert questionnaire.access_token == new_questionnaire.access_token


## Send questionnaire visa request
client.send_visa_request(questionnaire.visa_status)


## Get questionnaire status
status: VisaStatuses = client.send_visa_request(questionnaire.visa_status)

```