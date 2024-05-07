from dataclasses import dataclass, field

from visum_sdk.enums import DocumentTypes


@dataclass
class ValidatorDTO:
    name: str
    meta: dict | None


@dataclass
class FieldDTO:
    required: bool
    name: str
    label: str
    type: str
    validators: list[ValidatorDTO] = field(default_factory=list)
    value: str | dict | list | int | float = None
    nested_fields: list['FieldDTO'] = field(default_factory=list)
    choices: list[str] = field(default_factory=list)
    address_fields: dict = None
    address_country_only: str = None


@dataclass
class SectionDTO:
    name: str
    label: str
    fields: list[FieldDTO]
    errors: dict[str, list[str]]
    required_fields_count: int
    valid_fields_count: int
    answers_fields_count: int
    is_valid: bool
    icon_name: str


@dataclass
class FormDTO:
    document_type: DocumentTypes
    sections: list[SectionDTO]


@dataclass
class QuestionnaireDTO:
    document_type: str
    access_token: str
    filling_status: str
    visa_status: str
    answers: dict
    form: FormDTO
