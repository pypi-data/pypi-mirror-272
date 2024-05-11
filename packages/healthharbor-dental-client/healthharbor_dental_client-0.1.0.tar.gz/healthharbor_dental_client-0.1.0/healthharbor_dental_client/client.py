import requests
from typing import Optional, List
from .models import DentalInquiry, DentalInquiryResponse

class HealthHarborDentalClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.headers = {'Authorization': f'Bearer {self.auth_token}'}

    def get_inquiries(self, external_id: Optional[str] = None, limit: int = 200) -> List[DentalInquiryResponse]:
        """Retrieve dental inquiries with optional filters."""
        url = f"{self.base_url}/api/v0/dental/inquiries"
        params = {'external_id': external_id, 'limit': limit}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()  # Raises HTTPError for bad requests
        return DentalInquiryResponse.parse_list(response.json())

    def create_inquiry(self, inquiry_data: dict) -> DentalInquiryResponse:
        """Create a new dental inquiry."""
        url = f"{self.base_url}/api/v0/dental/inquiries"
        response = requests.post(url, headers=self.headers, json=inquiry_data)
        response.raise_for_status()
        return DentalInquiryResponse.parse(response.json())
