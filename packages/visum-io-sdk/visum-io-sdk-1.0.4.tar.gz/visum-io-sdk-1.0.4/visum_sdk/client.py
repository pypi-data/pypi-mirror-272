import uuid
from typing import Dict

import requests

from visum_sdk.dto import QuestionnaireDTO, FormDTO, SectionDTO, FieldDTO, ValidatorDTO
from visum_sdk.enums import DocumentTypes, VisaStatuses

DEFAULT_HOST = 'demo.visum.io'


class VisumIOClient:
    def __init__(self, api_key: str, host: str = DEFAULT_HOST, is_sandbox: bool = True):
        self.api_key = api_key
        self.host = host
        self.is_sandbox = is_sandbox

    def create_questionnaire(
            self,
            document_type: DocumentTypes,
            answers: Dict[str, Dict[str, object]],
            simple: bool = False,
    ) -> QuestionnaireDTO:
        url = '/api/v1/create_questionnaire/'
        if simple:
            url += '?simple=true'
        result = self._post(url, {
            'document_type': document_type,
            'answers': answers,
        }).json()
        return QuestionnaireDTO(
            document_type=result['document_type'],
            access_token=result['access_token'],
            filling_status=result['filling_status'],
            visa_status=result['visa_status'],
            answers=result['answers'],
            form=self._deserialize_form(result['form']),
        )

    def get_questionnaire(
            self,
            access_token: str,
            simple: bool = False,
    ) -> QuestionnaireDTO:
        url = f'/api/v1/create_questionnaire/?access_token={access_token}'
        if simple:
            url += '&simple=true'
        result = self._get(url).json()
        return QuestionnaireDTO(
            document_type=result['document_type'],
            access_token=result['access_token'],
            filling_status=result['filling_status'],
            visa_status=result['visa_status'],
            answers=result['answers'],
            form=self._deserialize_form(result['form']),
        )

    def send_visa_request(
            self,
            access_token: str,
            pay_for_evisa: bool = False,
            bank_card_number: str = None,
            bank_card_month: str = None,
            bank_card_year: str = None,
            bank_card_cvv: str = None,
            bank_card_holder: str = None,
    ):
        url = f'/api/v1/send_visa_request/?access_token={access_token}'
        result = self._post(url, {
            'pay_for_evisa': pay_for_evisa,
            'bank_card_number': bank_card_number,
            'bank_card_month': bank_card_month,
            'bank_card_year': bank_card_year,
            'bank_card_cvv': bank_card_cvv,
            'bank_card_holder': bank_card_holder,
        }).json()
        if not result['ok']:
            raise Exception('Questionnaire generation was not started')

    def visa_status(
            self,
            access_token: str,
    ) -> VisaStatuses:
        url = f'/api/v1/visa_status/?access_token={access_token}'
        result = self._get(url).json()
        return VisaStatuses(result['visa_status'])

    def _get(self, url: str):
        response = requests.get(self._get_url(url), headers=self._get_headers())
        response.raise_for_status()
        return response

    def _post(self, url: str, json):
        response = requests.post(self._get_url(url), json=json, headers=self._get_headers())
        response.raise_for_status()
        return response

    def _get_url(self, url: str) -> str:
        if url.startswith('/'):
            url = url[1:]
        return f'{self.host}/{url}'

    def _get_headers(self) -> dict:
        headers = {
            'Content-Type': 'application/json'
        }
        if self.is_sandbox:
            headers['X-Sandbox'] = 'true'
        else:
            headers['Idempotency-Key'] = str(uuid.uuid4())
            headers['X-Sandbox'] = 'false'
        return headers

    def _deserialize_form(self, form: dict) -> FormDTO:
        return FormDTO(
            document_type=form['document_type'],
            sections=[
                SectionDTO(
                    name=section['name'],
                    label=section['label'],
                    fields=[
                        self._deserialize_field(field)
                        for field in section['fields']
                    ],
                    errors=section['errors'],
                    required_fields_count=section['required_fields_count'],
                    valid_fields_count=section['valid_fields_count'],
                    answers_fields_count=section['answers_fields_count'],
                    is_valid=section['is_valid'],
                    icon_name=section['icon_name'],
                ) for section in form['sections']
            ],
        )

    def _deserialize_field(self, field: dict) -> FieldDTO:
        return FieldDTO(
            required=field['required'],
            name=field['name'],
            label=field['label'],
            type=field['type'],
            validators=[
                ValidatorDTO(
                    name=validator['name'],
                    meta=validator['meta'],
                ) for validator in field['validators']
            ],
            value=field['value'],
            nested_fields=[
                self._deserialize_field(field)
                for field in field['nested_fields']
            ],
            choices=field['choices'],
            address_fields=field['address_fields'],
            address_country_only=field['address_country_only'],
        )
