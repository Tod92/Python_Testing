from tests.conftest import (
    TEST_CLUBS_FILE,
    TEST_COMPETITIONS_FILE,
    TEST_BOOKINGS_FILE,
    testfiles_rebuilder
    )
from app import models, util


class TestClass:
    def setup_class(cls):
        # Club "Iron Temple"
        cls.club = models.Club(name="Iron Temple",email="mail@mail.com",points="0")
        # Competition "Spring Festival"
        cls.competition = models.Competition(name="Spring Festival",date="01012023",numberOfPlaces="0")

    def teardown_class(cls):
        # Rebuilds json test files
        testfiles_rebuilder()

    def mocking_json_files(self, mocker):
        mocker.patch.object(models.Club, '_json_file_path', TEST_CLUBS_FILE)
        mocker.patch.object(models.Competition, '_json_file_path', TEST_COMPETITIONS_FILE)
        mocker.patch.object(models.Booking, '_json_file_path', TEST_BOOKINGS_FILE)

    def test_setup(self):
        assert self.club.name == "Iron Temple"
        assert self.competition.name == "Spring Festival"
    
    def test_should_error_if_not_enough_points(self, mocker):
        self.mocking_json_files(mocker)
        self.club.points = 2
        result = util.book(self.club,self.competition,3)
        assert type(result) == str
        assert result == "Club can't afford that many places. Not enough points left."

    def test_should_error_if_not_enough_places(self, mocker):
        self.mocking_json_files(mocker)
        self.club.points = 5
        self.competition.numberOfPlaces = 2
        result = util.book(self.club,self.competition,3)
        assert type(result) == str
        assert result == "Competition has not enough places left to do this"

    def test_should_error_if_more_than_max_authorized_bookings_per_competition(self, mocker):
        self.mocking_json_files(mocker)
        self.club.points = 13
        self.competition.numberOfPlaces = 15
        mocker.patch.object(util, 'MAX_PLACES_PER_COMP', 12)
        result = util.book(self.club, self.competition, 13)
        assert type(result) == str
        assert result == 'Maximum places per competition for a club is 12'
        mocker.patch.object(util, 'MAX_PLACES_PER_COMP', 2)
        result = util.book(self.club, self.competition, 3)        
        assert type(result) == str
        assert result == 'Maximum places per competition for a club is 2'

    def test_should_book_and_save(self, mocker):
        self.mocking_json_files(mocker)
        self.club.points = 5
        self.competition.numberOfPlaces = 5
        self.club.save()
        self.competition.save()
        result = util.book(self.club, self.competition, 4)
        assert result == True
        booking = models.Booking.get_bookings(self.club.name)
        assert booking != None
        assert booking.get_booking(self.competition.name) == 4