import pytest

from app.app import create_app

# Data paths for test
TEST_CLUBS_FILE = "../tests/data/test_clubs.json"
TEST_COMPETITIONS_FILE = "../tests/data/test_competitions.json"
TEST_BOOKINGS_FILE = "../tests/data/test_bookings.json"


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client