import json

CLUBS_FILE = "../data/clubs.json"
COMPETITIONS_FILE = "../data/competitions.json"

class Club():
    
    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = points

    def __repr__(self):
        return self.name

    @classmethod
    def get_clubs_from_json(cls):
        """
        Reads JSON file 
        Returns a dict
        """
        with open(CLUBS_FILE) as c:
            listOfClubs = json.load(c)['clubs']
        return listOfClubs
    
    @classmethod
    def get_club_list(cls):
        """
        Reads JSON file (with get_clubs_from_json method)
        Returns a list of Club Objects
        """
        result = []
        listOfClubs = Club.get_clubs_from_json()
        
        for c in listOfClubs:
            instance = cls(c["name"],c["email"],c["points"])
            result.append(instance)
        return result

    @classmethod
    def get_club(cls, name=None, email=None):
        clubs = Club.get_club_list()
        for c in clubs:
            if c.name == name:
                return c
            elif c.email == email:
                return c
        return None
    
    def save(self):
        # Get list of all Club instances from json file
        clubs = Club.get_club_list()
        # Replace self in club list
        clubs = [self if c.name == self.name else c for c in clubs]
        # Transform Club instances to dict
        clubs = [c.__dict__ for c in clubs]
        # Transform to fit json file format {"clubs":[clubList]}
        clubs = {"clubs":clubs}
        # Dumps into json file
        file = open(CLUBS_FILE, 'w')
        json.dump(clubs, file)
        file.close()


class Competition():
    
    def __init__(self, name, date, numberOfPlaces):
        self.name = name
        self.date = date
        self.numberOfPlaces = numberOfPlaces

    def __repr__(self):
        return self.name

    @classmethod
    def get_competitions_from_json(cls):
        with open(COMPETITIONS_FILE) as c:
            listOfCompetitions = json.load(c)['competitions']
        return listOfCompetitions
    
    @classmethod
    def get_competition_list(cls):
        result = []
        listOfCompetitions = Competition.get_competitions_from_json()
        
        for c in listOfCompetitions:
            instance = cls(c["name"],c["date"],c["numberOfPlaces"])
            result.append(instance)
        return result

    @classmethod
    def get_competition(cls, name=None):
        competitions = Competition.get_competition_list()
        for c in competitions:
            if c.name == name:
                return c
        return None
    
    def save(self):
        # Get list of all Competition instances from json file
        competitions = Competition.get_competition_list()
        # Replace self in competition list
        competitions = [self if c.name == self.name else c for c in competitions]
        # Transform competition instances to dict
        competitions = [c.__dict__ for c in competitions]
        # Transform to fit json file format {"competitions":[competitionList]}
        competitions = {"competitions":competitions}
        # Dumps into json file
        file = open(COMPETITIONS_FILE, 'w')
        json.dump(competitions, file)
        file.close()