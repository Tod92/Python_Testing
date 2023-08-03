import json

CLUBS_FILE = "../data/clubs.json"
CLUBS_KEY = "clubs"
COMPETITIONS_FILE = "../data/competitions.json"
COMPETITIONS_KEY = "competitions"
BOOKINGS_FILE = "../data/bookings.json"
BOOKINGS_KEY = "bookings"


class Model:
    """
    Abstract model to inherit from. Manage json file read and write.
    """
    _json_file_path = None
    _json_key_name = None

    def __repr__(self):
        return self.name

    @classmethod
    def get_dict_from_json(cls):
        """
        Reads JSON file
        Returns a dict
        """
        with open(cls._json_file_path) as c:
            listOfClubs = json.load(c)[cls._json_key_name]
        return listOfClubs

    def db_write(self, json_file):
        file = open(self._json_file_path, 'w')
        json.dump(json_file, file)
        file.close()

    def get_list(self):
        """
        To define in subclass
        Should return list of all class instance found in json file
        """
        pass

    def save(self):
        # Get list of all Club instances from json file
        result = self.get_list()
        # Replace self in club list
        result = [self if c.name == self.name else c for c in result]
        # Add self if not already in json file (mandatory for bookings)
        if self not in result:
            result.append(self)
        # Transform Club instances to dict
        result = [c.__dict__ for c in result]
        # Transform to fit json file format {"clubs":[clubList]}
        result = {self._json_key_name: result}
        # Dumps into json file
        self.db_write(result)
        # Returns writed club list when sucess
        return result


class Club(Model):

    _json_file_path = CLUBS_FILE
    _json_key_name = CLUBS_KEY

    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = points

    @classmethod
    def get_list(cls):
        """
        Reads JSON file (with get_clubs_from_json method)
        Returns a list of Club Objects
        """
        result = []
        listOfClubs = Club.get_dict_from_json()

        for c in listOfClubs:
            instance = cls(c["name"], c["email"], c["points"])
            result.append(instance)
        return result

    @classmethod
    def get_club(cls, name=None, email=None):
        clubs = Club.get_list()
        for c in clubs:
            if c.name == name:
                return c
            elif c.email == email:
                return c
        return None


class Competition(Model):

    _json_file_path = COMPETITIONS_FILE
    _json_key_name = COMPETITIONS_KEY

    def __init__(self, name, date, numberOfPlaces):
        self.name = name
        self.date = date
        self.numberOfPlaces = numberOfPlaces

    @classmethod
    def get_list(cls):
        result = []
        listOfCompetitions = Competition.get_dict_from_json()

        for c in listOfCompetitions:
            instance = cls(c["name"], c["date"], c["numberOfPlaces"])
            result.append(instance)
        return result

    @classmethod
    def get_competition(cls, name=None):
        competitions = Competition.get_list()
        for c in competitions:
            if c.name == name:
                return c
        return None


class Booking(Model):
    """
    Class to track bookings per club
    booked format : {"name": "club1", "booked": {"competition1" : points, "competition2": points}}
    """
    _json_file_path = BOOKINGS_FILE
    _json_key_name = BOOKINGS_KEY

    def __init__(self, name, booked={}):
        self.name = name
        self.booked = booked

    def __repr__(self):
        return 'Bookings for ' + self.name

    @classmethod
    def get_list(cls):
        result = []
        listOfBookings = Booking.get_dict_from_json()

        for b in listOfBookings:
            instance = cls(b["name"], b["booked"])
            result.append(instance)
        return result

    @classmethod
    def get_bookings(cls, name=None):
        """
        Return Booking instance for the searched club name
        """
        bookings = Booking.get_list()
        for b in bookings:
            if b.name == name:
                return b
        return None

    def get_booking(self, competition_name=None):
        """
        Returns nb_booked for competition_name
        None if not found
        """
        return self.booked.get(competition_name)
