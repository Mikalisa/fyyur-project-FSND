

from app.extensions import db, format_datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, Blueprint

from app.models import Artist, Show
from app.forms import *


artist = Blueprint('artist', __name__)









#  Artists
#  ----------------------------------------------------------------
@artist.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database


  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@artist.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search = request.form.get('search_term', '')

  result = Artist.query.filter(Artist.name.ilike("%" + search + "%")).all()
  
  response = {
        "count": len(result),
        "data": result
    }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@artist.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  

  artist = Artist.query.filter_by(id=artist_id).one()

  shows = Show.query.filter_by(artist_id=artist_id).all()

  past_shows = []
  upcoming_shows = []

  current_time = datetime.now()

  for show in shows:

    data = {
          "artist_id": show.venue_id,
          "artist_name": show.venue.name,
           "artist_image_link": show.venue.image_link,
           "start_time": format_datetime(str(show.start_time))
        }
    if show.start_time > current_time:
      upcoming_shows.append(data)
    else:
      past_shows.append(data)


  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_talent": artist.seeking_venue,
    "seeking_description":artist.description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  
  
  return render_template('pages/show_artist.html', artist=data)




#  Update
#  ----------------------------------------------------------------
@artist.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@artist.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  result = Artist.query.filter_by(id=artist_id).one()

  try:
    

    result.name = form.name.data
   
    result.city = form.city.data
    result.state = form.state.data
    result.phone = form.phone.data
    result.genres = form.genres.data
    result.facebook_link = form.facebook_link.data
    result.website = form.website.data
    result.image_link = form.image_link.data
    result.seeking_talent = form.seeking_venue.data
    result.description = form.description.data
    db.session.add(result)
    db.session.commit()
    flash('Artist ' + form.name.data + ' was successfully Edited!')

  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + form.name.data + ' could not be Edited.')
    

  finally:
    db.session.close()
    

  return redirect(url_for('artist.show_artist', artist_id=artist_id))




#  Create Artist
#  ----------------------------------------------------------------

@artist.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@artist.route('/artists/create', methods=['POST'])
def create_artist_submission():

  form = ArtistForm(request.form)

  try:
    new_artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      genres=form.genres.data,
      
      
      image_link=form.image_link.data,
      website = form.website.data,
      facebook_link=form.facebook_link.data,
      
      description = form.description.data,
      seeking_venue = form.seeking_venue.data)
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + form.name.data + ' was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')

  finally:
    db.session.close()


 

  

  return render_template('pages/home.html')