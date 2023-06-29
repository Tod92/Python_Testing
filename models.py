import json

CLUBS_FILE = "clubs.json"

class Club():
    
    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = points

    def __repr__(self):
        return self.name
       
    @classmethod
    def get_club_list(cls):
        result = []
        with open(CLUBS_FILE) as c:
            listOfClubs = json.load(c)['clubs']
        
        for c in listOfClubs:
            instance = cls(c["name"],c["email"],c["points"])
            result.append(instance)
        return result

    @classmethod
    def get_club(cls, email):
        clubs = Club.get_club_list()
        for c in clubs:
            if c.email == email:
                return c
        return None
    