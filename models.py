from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)

SQLALCHEMY_DATABASE_URI = 'postgresql:/postgres:cnj712@localhost:5432/fyyur'

# Suggestion from error message in terminal
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
# 
# Reference (Genres): https://knowledge.udacity.com/questions/803047
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")

    def __repr__(self):
      return f'<Venue: {self.id}, name: {self.name}, genres: {self.genres}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, website_link: {self.website_link}, facebook_link: {self.facebook_link}, currently_seeking: {self.currently_seeking}, seeking_description: {self.seeking_description}, image_link: {self.image_link}, shows: {self.shows}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(250), nullable=False)
    facebook_link = db.Column(db.String(250), nullable=False)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")
    

    def __repr__(self):
        return f'<Artist: {self.id}, name: {self.name}, genres: {self.genres}, city: {self.city}, state: {self.state}, phone: {self.phone}, website_link: {self.website_link}, facebook_link: {self.facebook_link}, currently_seeking: {self.currently_seeking}, seeking_description: {self.seeking_description}, image_link: {self.image_link}, shows: {self.shows}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    
    # ForeignKeys
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)

    # Reference: https://knowledge.udacity.com/questions/339040
    # Relationships - Commented out until relevance determined
    # artist = db.relationship('Artist', backref=db.backref('shows', cascade='all, delete'))
    # venue = db.relationship('Venue', backref=db.backref('shows', cascade='all, delete'))

    def __repr__(self):
        return f'<Show: {self.id}, artist_id: {self.artist_id}, venue_id {self.venue_id}, start_time: {self.start_time}>'


