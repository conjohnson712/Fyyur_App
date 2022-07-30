#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

# Reference for project: TODOAPP-CRUD-LISTS-SOLUTIONS app_sol.py
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from forms import * 
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
import sys
from models import db, app, Artist, Venue, Show

# Suggestion from Knowledge since I am on Windows
import collections
import collections.abc
collections.Callable = collections.abc.Callable

#----------------------------------------------------------------------------#
# Filters.
# Reference: https://knowledge.udacity.com/questions/451081
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
        date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  Venues
#  Reference: https://knowledge.udacity.com/questions/338265
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    regions = []
    venues = Venue.query.all()
    for place in Venue.query.distinct(Venue.city, Venue.state).all():
        regions.append({
            'city': place.city,
            'state': place.state,
            'venues': [{
                'id': venue.id,
                'name': venue.name,
            } for venue in venues if
                venue.city == place.city and venue.state == place.state]
        })
    return render_template('pages/venues.html', areas=regions)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Reference: https://knowledge.udacity.com/questions/711360
  search = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike("%" + search + "%")).all()
  
  data = []
  for venue in venues:
    data.append({
        'id': venue.id,
        'name': venue.name,
    })

  response = {
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # References: 
  # https://knowledge.udacity.com/questions/654966
  # https://knowledge.udacity.com/questions/452402 - Mostly this one to satisfy the JOIN requirement
  # https://knowledge.udacity.com/questions/328047
  venue = Venue.query.get(venue_id)
 
  past_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time < datetime.now()).all()
  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time > datetime.now()).all()
  data= {
    'id': venue_id,
    'name': venue.name,
    'city': venue.city,
    'state': venue.state,
    'address': venue.address,
    'phone': venue.phone,
    'image_link': venue.image_link,
    'facebook_link': venue.facebook_link,
    'website_link': venue.website_link,
    'genres': venue.genres,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'upcoming_shows': [{
      'artist_id': artist.id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': show.start_time
        } for artist, show in upcoming_shows], 
    'past_shows': [{
      'artist_id': artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time
      } for artist, show in past_shows],  
    'upcoming_shows_count': len(upcoming_shows),
    'past_shows_count': len(past_shows)
    }
    #   "past_shows_count": len(past_shows),
    #   "upcoming_shows_count": len(upcoming_shows),
  
  return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  References: 
#  https://knowledge.udacity.com/questions/474735
#  https://knowledge.udacity.com/questions/575403#575407
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
        venue = Venue(
            name=form.name.data,
            genres=form.genres.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            website_link=form.website_link.data,
            facebook_link=form.facebook_link.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data,
            image_link=form.image_link.data,
            )
        db.session.add(venue)
        db.session.commit()
        for field, err in form.errors.items():
            message.append(field + ' ' + '|'.join(err))
        # flash('Errors ' + str(message))
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except ValueError as e:
        print(e)
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
      doomed_venue = Venue.query.get(venue_id)
      db.session.delete(doomed_venue)
      db.session.commit()
      flash('Venue Successfully Deleted')
  except():
      db.session.rollback()
      error = True
  finally:
      db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None


#  Artists
#  Reference: https://knowledge.udacity.com/questions/103618
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Reference: https://knowledge.udacity.com/questions/711360
  search = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike("%" + search + "%")).all()
  data = []
  for artist in artists:
      data.append({
          'id': artist.id,
          'name': artist.name,
      })
  response = {
      "count": len(artists),
      "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # Reference: https://knowledge.udacity.com/questions/400757
  # Reference: https://knowledge.udacity.com/questions/654966
  # https://knowledge.udacity.com/questions/452402 - Mostly this one to satisfy the JOIN requirement
  # https://knowledge.udacity.com/questions/328047
  # shows the artist page with the given artist_id
  artist = Artist.query.get(artist_id)
 
  past_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
    filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time < datetime.now()).all()
  upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
    filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time > datetime.now()).all()
  data= {
    'id': artist_id,
    'name': artist.name,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'image_link': artist.image_link,
    'facebook_link': artist.facebook_link,
    'website_link': artist.website_link,
    'genres': artist.genres,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'upcoming_shows': [{
      'venue_id': venue.id,
      'venue_name': venue.name,
      'venue_image_link': venue.image_link,
      'start_time': show.start_time
        } for venue, show in upcoming_shows], 
    'past_shows': [{
      'venue_id': venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": show.start_time
      } for venue, show in past_shows],  
    'upcoming_shows_count': len(upcoming_shows),
    'past_shows_count': len(past_shows)
    }
  return render_template('pages/show_artist.html', artist=data)


#  Update
#  Reference: https://knowledge.udacity.com/questions/383703
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.filter(Artist.id == artist_id).first()
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  try:
      artist = Artist.query.filter(Artist.id == artist_id).first()
      form.populate_obj(artist)
      db.session.commit()
      flash(f'Artist {form.name.data} was successfully edited!')
  except ValueError as e:
      db.session.rollback()
      flash(f'An error occurred in {form.name.data}. Error: {str(e)}')
  finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue= Venue.query.filter(Venue.id == venue_id).first()
  form = VenueForm(obj=venue)
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)
  try:
      venue = Venue.query.filter(Venue.id == venue_id).first()
      form.populate_obj(venue)
      db.session.commit()
      flash(f'Venue {form.name.data} was successfully edited!')
  except ValueError as e:
      db.session.rollback()
      flash(f'An error occurred in {form.name.data}. Error: {str(e)}')
  finally:
      db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  if form.validate():
    try:
        artist = Artist(
            name=form.name.data,
            genres=form.genres.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            website_link=form.website_link.data,
            facebook_link=form.facebook_link.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data,
            image_link=form.image_link.data,
        )
        db.session.add(artist)
        db.session.commit()
        for field, err in form.errors.items():
                message.append(field + ' ' + '|'.join(err))
        flash('Errors ' + str(message))
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except ValueError as e:
        print(e)
        flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close() 
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  data = Show.query.all()

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # References: 
  # https://knowledge.udacity.com/questions/653784
  # https://www.programiz.com/python-programming/datetime/strftime 
  form = ShowForm(request.form)
  if form.validate():
    try:
      show = Show(
          artist_id=form.artist_id.data,
          venue_id=form.venue_id.data,
          start_time=form.start_time.data,
          )
      db.session.add(show)
      db.session.commit()
       # on successful db insert, flash success
      flash('Show was successfully listed!')
    except ValueError as e:
        print(e)
        for field, err in form.errors.items():
            message.append(field + ' ' + '|'.join(err))
        flash('Errors ' + str(message))
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Show could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
