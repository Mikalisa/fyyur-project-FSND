from .extensions import db
from datetime import datetime, timedelta





## classes for the database

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean)
    facebook_link = db.Column(db.String(120))
    description = db.Column(db.String)
    website = db.Column(db.String)


    shows = db.relationship('Show', backref='venue', lazy=True)
    



   

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))


    image_link = db.Column(db.String(500))
    website = db.Column(db.String)
    facebook_link = db.Column(db.String(120))
    description = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean)

    shows = db.relationship('Show', backref='artist', lazy=True)

   
    



class Show(db.Model):

  __tablename__ = 'Show'
  
  
  id = db.Column(db.Integer, primary_key=True)

  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  


  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
 


  start_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)



 