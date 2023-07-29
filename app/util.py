from app.models import Club, Competition

MAX_PLACES_PER_COMP = 12

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
        print("HERE")
        return "Club can't afford that many places. Not enough points left."
    elif competition.numberOfPlaces < placesRequired:
        return "Competition has not enough places left to do this"
    # TODO : club limit for this competition condition
    elif placesRequired > MAX_PLACES_PER_COMP:
        return f'Maximum places per competition for a club is {MAX_PLACES_PER_COMP}'
    elif competition.name in club.bookings.keys():
        if int(club.bookings[competition.name]) + placesRequired > MAX_PLACES_PER_COMP:
            return f'Club can\'t book more than {MAX_PLACES_PER_COMP} places for this competition'

    else:
        club.points -= placesRequired
        competition.numberOfPlaces -= placesRequired

        club.points = str(club.points)
        competition.numberOfPlaces = str(competition.numberOfPlaces)
        
        # Add to club's bookings dict
        if competition.name not in club.bookings.keys():
            club.bookings[competition.name] = placesRequired
        else:
            club.bookings[competition.name] += placesRequired

        club.save()
        competition.save()
        return True