import pytest
import requests
import requests_mock
from healthharbor_dental_client.client import HealthHarborDentalClient
from healthharbor_dental_client.models import DentalInquiryResponse


@pytest.fixture
def client():
    """Fixture to create a client instance with a dummy base URL and auth token."""
    return HealthHarborDentalClient(
        base_url="http://fakeapi.com", auth_token="dummytoken"
    )


def test_get_inquiries_success(client):
    """Test successful retrieval of dental inquiries."""
    with requests_mock.Mocker() as m:
        m.get(
            "http://fakeapi.com/api/v0/dental/inquiries",
            json=[{"id": "123", "status": "SUCCESS"}],
            status_code=200,
        )
        response = client.get_inquiries()
        assert len(response) == 1
        assert isinstance(response[0], DentalInquiryResponse)
        assert response[0].id == "123"
        assert response[0].status == "SUCCESS"


def test_get_inquiries_failure(client):
    """Test handling of server error when retrieving dental inquiries."""
    with requests_mock.Mocker() as m:
        m.get("http://fakeapi.com/api/v0/dental/inquiries", status_code=500)
        with pytest.raises(requests.HTTPError):
            client.get_inquiries()


def test_create_inquiry_success(client):
    """Test successful creation of a dental inquiry."""
    inquiry_data = {
        "patient_name": "John Doe",
        "dob": "1990-01-01",
        "member_id": "123456789",
        "npi": "987654321",
        "tax_id": "123456789",
        "insurance": "CIGNA",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "http://fakeapi.com/api/v0/dental/inquiries",
            json={"id": "123", "status": "SUCCESS"},
            status_code=201,
        )
        response = client.create_inquiry(inquiry_data)
        assert response.id == "123"
        assert response.status == "SUCCESS"


def test_create_inquiry_failure(client):
    """Test handling of server error when creating a dental inquiry."""
    inquiry_data = {
        "patient_name": "John Doe",
        "dob": "1990-01-01",
        "member_id": "123456789",
        "npi": "987654321",
        "tax_id": "123456789",
        "insurance": "CIGNA",
    }
    with requests_mock.Mocker() as m:
        m.post("http://fakeapi.com/api/v0/dental/inquiries", status_code=400)
        with pytest.raises(requests.HTTPError):
            client.create_inquiry(inquiry_data)


@pytest.mark.parametrize(
    "limit,expected_count", [(1, 1), (0, 0), (1000, 5)]
)  # assuming the API caps responses at 5
def test_get_inquiries_varied_limits(client, limit, expected_count):
    with requests_mock.Mocker() as m:
        m.get(
            "http://fakeapi.com/api/v0/dental/inquiries",
            json=[{"id": str(i), "status": "SUCCESS"} for i in range(expected_count)],
            status_code=200,
        )
        response = client.get_inquiries(limit=limit)
        assert len(response) == expected_count


def test_get_inquiries_connection_error(client):
    with requests_mock.Mocker() as m:
        m.get("http://fakeapi.com/api/v0/dental/inquiries", exc=ConnectionError)
        with pytest.raises(ConnectionError):
            client.get_inquiries()


def test_create_inquiry_with_invalid_data(client):
    with requests_mock.Mocker() as m:
        m.post("http://fakeapi.com/api/v0/dental/inquiries", status_code=400)
        with pytest.raises(requests.HTTPError):
            client.create_inquiry({"patient_name": "123"})  # Invalid data as example


def test_api_unauthorized(client):
    with requests_mock.Mocker() as m:
        m.get("http://fakeapi.com/api/v0/dental/inquiries", status_code=401)
        with pytest.raises(requests.HTTPError):
            client.get_inquiries()
