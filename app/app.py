import json
from flask import Flask,render_template,request,redirect,flash,url_for,Blueprint
from app.models import Club, Competition
from app import util

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


#competitions = Competition.get_competitions_from_json()
#clubs = Club.get_clubs_from_json()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    club = Club.get_club(email=email)
    competitions = Competition.get_competition_list()
    if club:
        return render_template('welcome.html',club=club,competitions=competitions)
    else:
        flash('Sorry, that email wasn\'t found.')
        return render_template('index.html')

@main.route('/book/<competition>/<club>')
def book(competition,club):
    # foundClub = [c for c in clubs if c['name'] == club][0]
    foundClub = Club.get_club(name=club)
    # foundCompetition = [c for c in competitions if c['name'] == competition][0]
    foundCompetition = Competition.get_competition(name=competition)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@main.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    # competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    competition = Competition.get_competition(name=request.form['competition'])
    # club = [c for c in clubs if c['name'] == request.form['club']][0]
    club = Club.get_club(name=request.form['club'])
    placesRequired = int(request.form['places'])
    # competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    sucess = util.book(club, competition, placesRequired)
    if sucess == True:
        flash('Great-booking complete!')
    else:
        flash('ERROR : '+ sucess)
    competitions = Competition.get_competition_list()
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@main.route('/logout')
def logout():
    return redirect(url_for('main.index'))