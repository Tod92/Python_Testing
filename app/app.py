from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    Blueprint
    )
from app.models import Club, Competition
from app import util


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = 'something_special'
    app.register_blueprint(main)
    return app


main = Blueprint("main", __name__)


@main.route('/')
def index():
    clubs = Club.get_list()
    return render_template('index.html', clubs=clubs)


@main.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = Club.get_club(email=email)
    clubs = Club.get_list()
    competitions = Competition.get_competition_list()
    if club:
        return render_template('welcome.html', club=club, clubs=clubs, competitions=competitions)
    else:
        flash('Sorry, that email wasn\'t found.')
        return render_template('index.html', clubs=clubs)


@main.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = Club.get_club(name=club)
    foundCompetition = Competition.get_competition(name=competition)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        clubs = Club.get_list()
        competitions = Competition.get_competition_list()
        return render_template('welcome.html', club=club, clubs=clubs, competitions=competitions)


@main.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = Competition.get_competition(name=request.form['competition'])
    club = Club.get_club(name=request.form['club'])
    placesRequired = int(request.form['places'])
    sucess = util.book(club, competition, placesRequired)
    if sucess is True:
        flash('Great-booking complete!')
    else:
        flash('ERROR : ' + sucess)
    clubs = Club.get_list()
    competitions = Competition.get_list()
    return render_template('welcome.html', club=club, clubs=clubs, competitions=competitions)


@main.route('/logout')
def logout():
    return redirect(url_for('main.index'))
