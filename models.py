import json

CLUBS_FILE = "clubs.json"
COMPETITIONS_FILE = "competitions.json"

class Club():
    
    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = points

    def __repr__(self):
        return self.name

    @classmethod
    def get_clubs_from_json(cls):
        with open(CLUBS_FILE) as c:
            listOfClubs = json.load(c)['clubs']
        return listOfClubs
    
    @classmethod
    def get_club_list(cls):
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
            if c.email == email:
                return c
        return None
    

class Competition():
    
    def __init__(self, name, date, points):
        self.name = name
        self.email = date
        self.points = points

    def __repr__(self):
        return self.name

    @classmethod
    def get_competitions_from_json(cls):
        with open(COMPETITIONS_FILE) as c:
            listOfCompetitions = json.load(c)['clubs']
        return listOfCompetitions
    
    @classmethod
    def get_competition_list(cls):
        result = []
        listOfCompetitions = Competition.get_competitions_from_json()
        
        for c in listOfCompetitions:
            instance = cls(c["name"],c["date"],c["points"])
            result.append(instance)
        return result

    @classmethod
    def get_competition(cls, name=None):
        competitions = Competition.get_club_list()
        for c in competitions:
            if c.name == name:
                return c
        return None