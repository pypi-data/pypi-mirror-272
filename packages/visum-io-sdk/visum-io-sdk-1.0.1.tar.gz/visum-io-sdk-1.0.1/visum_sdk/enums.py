from enum import Enum


class DocumentTypes(str, Enum):
    CHINESE_VISA = 'CHINESE_VISA'
    INDIAN_E_VISA = 'INDIAN_E_VISA'
    SRI_LANKA_E_VISA = 'SRI_LANKA_E_VISA'
    UAE_E_VISA = 'UAE_E_VISA'
    SAUDI_E_VISA = 'SAUDI_E_VISA'


class VisaStatuses(str, Enum):
    NOT_STARTED = 'NOT_STARTED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    FAILED_TO_PAY = 'FAILED_TO_PAY'
    DONE = 'DONE'
    ERROR = 'ERROR'
