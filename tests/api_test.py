import pytest
from django.test import Client

@pytest.mark.django_db
def test_api_healthcheck():
    client = Client()
    response = client.get("/")
    assert response.status_code in [200, 404]

