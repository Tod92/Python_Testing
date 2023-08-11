import pytest, json
from app import models
from app.server import create_app

# Data paths for test
TEST_CLUBS_FILE = "../tests/data/test_clubs.json"
TEST_COMPETITIONS_FILE = "../tests/data/test_competitions.json"
TEST_BOOKINGS_FILE = "../tests/data/test_bookings.json"

# Expected results
EXPECTED_CLUBS = [
    {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    },
    
    {
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },
    {   "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }
    ]
EXPECTED_COMPETITIONS = [
    {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    },
    {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    },
    {
        "name": "STRONGMAN Festival",
        "date": "2023-06-28 10:00:00",
        "numberOfPlaces": "0"
    }
    ]
EXPECTED_BOOKINGS = [
    {
        "name": "Simply Lift", 
        "booked": 
        {
            "Fall Classic": 7, 
            "STRONGMAN Festival": 3
        }
    }, 
    {
        "name": "She Lifts", 
        "booked": 
        {
            "Fall Classic": 12, 
            "Spring Festival": 2
        }
    }
    ]

# Building list of instances with list comprehension
CLUBS_INSTANCES = [models.Club(name=c['name'],
                               email=c['email'],
                               points=c['points']) for c in EXPECTED_CLUBS]

COMPETITIONS_INSTANCES = [models.Competition(name=c['name'],
                                             date=c['date'],
                                             numberOfPlaces=c['numberOfPlaces']) for c in EXPECTED_COMPETITIONS]

BOOKINGS_INSTANCES =  [models.Booking(name=b["name"],
                                      booked=b["booked"]) for b in EXPECTED_BOOKINGS]


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def testfiles_rebuilder():
        clubs_json = {models.Club._json_key_name: EXPECTED_CLUBS}
        file = open(TEST_CLUBS_FILE, 'w')
        json.dump(clubs_json, file)
        file.close
        competitions_json = {models.Competition._json_key_name: EXPECTED_COMPETITIONS}
        file = open(TEST_COMPETITIONS_FILE, 'w')
        json.dump(competitions_json, file)
        file.close
        bookings_json = {models.Booking._json_key_name: EXPECTED_BOOKINGS}
        file = open(TEST_BOOKINGS_FILE, 'w')
        json.dump(bookings_json, file)
        file.close