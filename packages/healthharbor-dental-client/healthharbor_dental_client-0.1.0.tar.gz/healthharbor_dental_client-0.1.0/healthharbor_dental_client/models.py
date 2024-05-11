from typing import Dict, Any, List

class DentalInquiry:
    def __init__(self, patient_name: str, dob: str, member_id: str, npi: str, tax_id: str, insurance: str):
        self.patient_name = patient_name
        self.dob = dob
        self.member_id = member_id
        self.npi = npi
        self.tax_id = tax_id
        self.insurance = insurance

    @staticmethod
    def parse(data: Dict[str, Any]) -> 'DentalInquiry':
        return DentalInquiry(**data)

class DentalInquiryResponse:
    def __init__(self, id: str, status: str):
        self.id = id
        self.status = status

    @staticmethod
    def parse(data: Dict[str, Any]) -> 'DentalInquiryResponse':
        """Parse JSON data to create a DentalInquiryResponse object."""
        return DentalInquiryResponse(id=data['id'], status=data['status'])

    @staticmethod
    def parse_list(data: List[Dict[str, Any]]) -> List['DentalInquiryResponse']:
        """Parse a list of JSON data to create a list of DentalInquiryResponse objects."""
        return [DentalInquiryResponse.parse(item) for item in data]
