from app import models
from tests.conftest import TEST_CLUBS_FILE, TEST_COMPETITIONS_FILE, TEST_BOOKINGS_FILE


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


def test_should_get_clubs_dict_from_json(mocker):
    """
    Testing Club.get_dict_from_json() class method
    """
    # Mocking global path variable to use test json file
    mocker.patch.object(models.Club, '_json_file_path', TEST_CLUBS_FILE)
    assert models.Club._json_file_path == TEST_CLUBS_FILE
    assert models.Club.get_dict_from_json() == EXPECTED_CLUBS

def test_should_get_competitions_dict_from_json(mocker):
    """
    Testing Competition.get_dict_from_json() class method
    """
    # Mocking global path variable to use test json file
    mocker.patch.object(models.Competition, '_json_file_path', TEST_COMPETITIONS_FILE)

    assert models.Competition.get_dict_from_json() == EXPECTED_COMPETITIONS

def test_should_get_bookings_dict_from_json(mocker):
    """
    Testing Booking.get_dict_from_json() class method
    """
    # Mocking global path variable to use test json file
    mocker.patch.object(models.Booking, '_json_file_path', TEST_BOOKINGS_FILE)

    assert models.Booking.get_dict_from_json() == EXPECTED_BOOKINGS


def test_should_get_clubs_list(mocker):
    """
    Testing Club.get_list() class method
    """
    # Mocking bound method get_dict_from_json called within tested method get_list
    mocker.patch('app.models.Club.get_dict_from_json', return_value=EXPECTED_CLUBS)
    clubs = models.Club.get_list()
    assert len(clubs) == 3
    assert clubs[0].name == "Simply Lift"
    assert clubs[1].email == "admin@irontemple.com"
    assert clubs[2].points == "12"

def test_should_get_competitions_list(mocker):
    """
    Testing Competition.get_list() class method
    """
    # Mocking bound method get_dict_from_json called within tested method get_list
    mocker.patch('app.models.Competition.get_dict_from_json', return_value=EXPECTED_COMPETITIONS)
    competitions = models.Competition.get_list()
    assert len(competitions) == 3
    assert competitions[0].name == "Spring Festival"
    assert competitions[1].date == "2020-10-22 13:30:00"
    assert competitions[2].numberOfPlaces == "0"

def test_should_get_bookings_list(mocker):
    """
    Testing Booking.get_list() class method
    """
    # Mocking bound method get_dict_from_json called within tested method get_list
    mocker.patch('app.models.Booking.get_dict_from_json', return_value=EXPECTED_BOOKINGS)
    bookings = models.Booking.get_list()
    assert len(bookings) == 2
    assert bookings[0].name == "Simply Lift"
    assert bookings[1].booked["Fall Classic"] == 12


def test_should_get_club_via_name(mocker):
    """
    Testing Club.get_club() class method with 'name' keyword argument
    """
    # Mocking bound method get_list called within tested method get_club
    mocker.patch('app.models.Club.get_list', return_value=CLUBS_INSTANCES)
    
    name = "Iron Temple"
    email = "admin@irontemple.com"
    points = "4"
    club = models.Club.get_club(name="Iron Temple")
    
    assert isinstance(club, models.Club)
    assert club.name == name
    assert club.email == email
    assert club.points == points

def test_should_get_club_via_email(mocker):
    """
    Testing Club.get_club() class method with 'email' keyword argument
    """
    # Mocking bound method get_list called within tested method get_club
    mocker.patch('app.models.Club.get_list', return_value=CLUBS_INSTANCES)
    
    name = "Iron Temple"
    email = "admin@irontemple.com"
    points = "4"
    club = models.Club.get_club(email=email)
    
    assert isinstance(club, models.Club)
    assert club.name == name
    assert club.email == email
    assert club.points == points


def test_should_get_competition_via_name(mocker):
    """
    Testing Competition.get_competition() class method with 'name' keyword argument
    """
    # Mocking bound method get_list called within tested method get_competition
    mocker.patch('app.models.Competition.get_list', return_value=COMPETITIONS_INSTANCES)
    
    name = "Fall Classic"
    date = "2020-10-22 13:30:00"
    numberOfPlaces = "13"
    competition = models.Competition.get_competition(name="Fall Classic")
    
    assert isinstance(competition, models.Competition)
    assert competition.name == name
    assert competition.date == date
    assert competition.numberOfPlaces == numberOfPlaces

def test_should_get_bookings_via_name(mocker):
    """
    Testing Booking.get_bookings() class method with 'name' keyword argument
    """
    # Mocking bound method get_list called within tested method get_booking
    mocker.patch('app.models.Booking.get_list', return_value=BOOKINGS_INSTANCES)

    name = "She Lifts"
    competition_name = "Spring Festival"
    number_booked = 2
    booking = models.Booking.get_bookings(name="She Lifts")
    
    assert isinstance(booking, models.Booking)
    assert booking.name == name
    assert booking.booked[competition_name] == number_booked

def test_should_update_club_when_saving(mocker):
    """
    Testing club_instance.save() method updates json data with instance informations
    """
    # Mocking bound method get_list called within tested method save
    mocker.patch('app.models.Club.get_list', return_value=CLUBS_INSTANCES)
    # Mocking bound method db_write called within tested method save
    # Preventing data writing
    mocker.patch('app.models.Club.db_write', return_value=True)
    
    club = models.Club(
                        name= "Iron Temple",
                        email= "thisIsModified@test.com",
                        points= "42"
    )
    result = club.save()
    for c in result["clubs"]:
        if c["name"] == "Iron Temple":
            assert c["email"] == "thisIsModified@test.com"
            assert c["points"] == "42"

def test_should_update_competition_when_saving(mocker):
    """
    Testing competition_instance.save() method updates json data with instance informations
    """
    # Mocking bound method get_list called within tested method save
    mocker.patch('app.models.Competition.get_list', return_value=COMPETITIONS_INSTANCES)
    # Mocking bound method db_write called within tested method save
    # Preventing data writing
    mocker.patch('app.models.Competition.db_write', return_value=True)
    
    competition = models.Competition(
                        name= "STRONGMAN Festival",
                        date= "2000-01-01 00:01:00",
                        numberOfPlaces= "42"
    )

    result = competition.save()
    for c in result["competitions"]:
        if c["name"] == "STRONGMAN Festival":
            assert c["date"] == "2000-01-01 00:01:00"
            assert c["numberOfPlaces"] == "42"

def test_should_update_booking_when_saving(mocker):
    """
    Testing booking_instance.save() method updates json data with instance informations
    """
    # Mocking bound method get_list called within tested method save
    mocker.patch('app.models.Booking.get_list', return_value=BOOKINGS_INSTANCES)
    # Mocking bound method db_write called within tested method save
    # Preventing data writing
    mocker.patch('app.models.Booking.db_write', return_value=True)
    
    booking = models.Booking(
                        name="She Lifts",
                        booked= {"Fall Classic": 12, "Spring Festival": 6, "STRONGMAN Festival": 1},
    )
    result = booking.save()
    for b in result["bookings"]:
        if b["name"] == "She Lifts":
            assert b["booked"]["Fall Classic"] == 12
            assert b["booked"]["STRONGMAN Festival"] == 1
            assert b["booked"]["Spring Festival"] == 6



