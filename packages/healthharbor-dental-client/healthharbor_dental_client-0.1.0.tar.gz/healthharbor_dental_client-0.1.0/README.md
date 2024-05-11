# HealthHarbor Dental Client

An unofficial client library for interacting with the Health Harbor Dental API. This library provides a convenient Python interface to access dental-specific endpoints of the Health Harbor API.

## Features

- Retrieve dental inquiries.
- Create new dental inquiries.
- Handle both individual and batch inquiries.

## Installation

Install `healthharbor_dental_client` using pip:

```bash
pip install healthharbor_dental_client
```

## Usage

Here is a quick example to get you started:

```python
from healthharbor_dental_client.client import HealthHarborDentalClient

# Initialize the client with your API key
client = HealthHarborDentalClient(base_url='https://api.healthharbor.com', auth_token='your_auth_token')

# Fetch dental inquiries
inquiries = client.get_inquiries()
print(inquiries)

# Create a new dental inquiry
response = client.create_inquiry({
    'patient_name': 'John Doe',
    'dob': '1980-01-01',
    'member_id': '1234567890',
    'npi': '9876543210',
    'tax_id': '123456789',
    'insurance': 'CIGNA'
})
print(response)
```

## Requirements

- Python 3.8+
- requests

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you have any issues or feature requests, please [open an issue](https://github.com/copyleftdev/healthharbor_dental_client/issues) on GitHub.

## Authors

- **Don Johnson** - *Initial work* - [DonJohnson](https://github.com/copyleftdev)
