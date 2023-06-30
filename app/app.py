import json
from flask import Flask,render_template,request,redirect,flash,url_for,Blueprint
from app.models import Club, Competition


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

def create_app():
    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.register_blueprint(main)
    return app

main = Blueprint("main", __name__)


competitions = Competition.get_competitions_from_json()
clubs = Club.get_clubs_from_json()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    club = Club.get_club(email=email)
    if club:
        return render_template('welcome.html',club=club,competitions=competitions)
    else:
        flash('Sorry, that email wasn\'t found.')
        return render_template('index.html')

@main.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@main.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@main.route('/logout')
def logout():
    return redirect(url_for('index'))