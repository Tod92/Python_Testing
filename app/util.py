from app.models import Club, Competition

def book(club: Club, competition: Competition, placesRequired: int):
    """
    Spends club points (if avaible) to book required number of places in
    competition (if avaible).
    Returns True for sucess or string with error for failure
    Errors:
    - "Club can't afford that many places. Not enough points left."
    - "Competition has not enough places left to do this"
    - "Club limit reached for this competition"
    """
    club.points = int(club.points)
    competition.numberOfPlaces = int(competition.numberOfPlaces)
    
    if club.points < placesRequired:
        return "Club can't afford that many places. Not enough points left."
    elif competition.numberOfPlaces < placesRequired:
        return "Competition has not enough places left to do this"
    # TODO : club limit for this competition condition
    else:
        club.points -= placesRequired
        competition.numberOfPlaces -= placesRequired

        club.points = str(club.points)
        competition.numberOfPlaces = str(competition.numberOfPlaces)

        club.save()
        competition.save()
        return True