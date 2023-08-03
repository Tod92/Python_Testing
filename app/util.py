from app.models import Club, Competition, Booking


MAX_PLACES_PER_COMP = 12


def book(club: Club, competition: Competition, placesRequired: int):
    """
    Spends club points (if avaible) to book required number of places in
    competition (if avaible).
    Returns True for sucess or string with detailed error for failure
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
    elif placesRequired > MAX_PLACES_PER_COMP:
        return f'Maximum places per competition for a club is {MAX_PLACES_PER_COMP}'

    # Check places already booked for this club
    nb_already_booked = None
    bookings = Booking.get_bookings(name=club.name)
    if bookings:
        # Stays with None value if not found
        nb_already_booked = bookings.get_booking(competition_name=competition.name)
    if nb_already_booked:
        if nb_already_booked + placesRequired > MAX_PLACES_PER_COMP:
            return f'Club can\'t book more than {MAX_PLACES_PER_COMP} places for this competition'

    club.points -= placesRequired
    competition.numberOfPlaces -= placesRequired

    club.points = str(club.points)
    competition.numberOfPlaces = str(competition.numberOfPlaces)

    # Add to club's bookings dict
    if bookings is None:
        bookings = Booking(name=club.name)
    if nb_already_booked:
        bookings.booked[competition.name] += placesRequired
    else:
        bookings.booked[competition.name] = placesRequired

    club.save()
    competition.save()
    bookings.save()

    return True
