#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    currently_seeking = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(250))
    image_link = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
      return f'<Venue: {self.id}, name: {self.name}, genres: {self.genres}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, website_link: {self.website_link}, facebook_link: {self.facebook_link}, currently_seeking: {self.currently_seeking}, seeking_description: {self.seeking_description}, image_link: {self.image_link}, shows: {self.shows}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    currently_seeking = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(250))
    image_link = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref='artist', lazy=True)
    

    def __repr__(self):
        return f'<Artist: {self.id}, name: {self.name}, genres: {self.genres}, city: {self.city}, state: {self.state}, phone: {self.phone}, website_link: {self.website_link}, facebook_link: {self.facebook_link}, currently_seeking: {self.currently_seeking}, seeking_description: {self.seeking_description}, image_link: {self.image_link}, shows: {self.shows}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    show_date = db.Column(db.DateTime, nullable=False)
    
    # ForeignKeys
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)

    # Reference: https://knowledge.udacity.com/questions/339040
    # Relationships
    artist = db.relationship('Artist', backref=db.backref('shows', cascade='all, delete'))
    venue = db.relationship('Venue', backref=db.backref('shows', cascade='all, delete'))

    def __repr__(self):
        return f'<Show: {self.id}, show_date: {self.show_date}, artist_id: {self.artist_id}, venue_id {self.venue_id}>'
