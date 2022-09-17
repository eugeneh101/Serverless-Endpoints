import json

import pytest
from fastapi.testclient import TestClient

from handler import app


client = TestClient(app)


def test_list_endpoints():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Available endpoints": [
            "GET /",
            "GET /greeting",
            "GET /greeting/{name}",
            "POST /greeting_with_date_or_day",
        ]
    }


def test_greeting():
    response = client.get("/greeting")
    assert response.status_code == 200
    assert response.json() == "Hello, welcome to my endpoint!"


def test_greeting_name_query():
    response = client.get("/greeting/name", params={"name": "Rob"})
    assert response.status_code == 200
    assert response.json() == "Hello Rob, welcome to my endpoint!"


def test_greeting_name_path():
    response = client.get("/greeting/Rob")
    assert response.status_code == 200
    assert response.json() == "Hello Rob, welcome to my endpoint!"


def test_greeting_with_date():
    response = client.post(
        "/greeting_with_date_or_day", data=json.dumps({"date": "1/2/3"})
    )
    assert response.status_code == 200
    assert response.json() == "Hello, the date is 1/2/3. Welcome to my endpoint!"


@pytest.mark.parametrize(
    "day",
    ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
)
def test_greeting_with_day(day):
    response = client.post("/greeting_with_date_or_day", data=json.dumps({"day": day}))
    assert response.status_code == 200
    assert response.json() == f"Hello, the day is {day}. Welcome to my endpoint!"


def test_greeting_with_day_failure():
    response = client.post(
        "/greeting_with_date_or_day",
        data=json.dumps({"day": "non-existent-day"}),
    )
    assert not response.ok


def test_greeting_with_date_and_day_failure():
    response = client.post(
        "/greeting_with_date_or_day",
        data=json.dumps({"date": "1/2/3", "day": "Sunday"}),
    )
    assert not response.ok
