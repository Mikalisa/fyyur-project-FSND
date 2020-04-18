

from app.extensions import db, format_datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, Blueprint

from app.models import Venue, Show
from app.forms import *




venue = Blueprint('venue', __name__)













@venue.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  result=[]

  venues = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state)

  for venue in venues:
      venues_in_city = db.session.query(Venue.id, Venue.name).filter(Venue.city == venue[0]).filter(Venue.state == venue[1])
      result.append({
        "city": venue[0],
        "state": venue[1],
        "venues": venues_in_city
      })
  
  
  return render_template('pages/venues.html', areas=result)


@venue.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search = request.form.get('search_term', '')

  result = Venue.query.filter(Venue.name.ilike("%" + search + "%")).all()
  
  response = {
        "count": len(result),
        "data": result
    }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))




@venue.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.filter_by(id=venue_id).one()

  shows = Show.query.filter_by(venue_id=venue_id).all()

  past_shows = []
  upcoming_shows = []

  current_time = datetime.now()

  for show in shows:

    data = {
          "artist_id": show.artist_id,
          "artist_name": show.artist.name,
           "artist_image_link": show.artist.image_link,
           "start_time": format_datetime(str(show.start_time))
        }
    if show.start_time > current_time:
      upcoming_shows.append(data)
    else:
      past_shows.append(data)

  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description":venue.description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  
  return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@venue.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@venue.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)

  try:
    new_venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      genres = form.genres.data,
      phone=form.phone.data,
      image_link=form.image_link.data,
      seeking_talent = form.seeking_talent.data,
      
      facebook_link=form.facebook_link.data,
      description = form.description.data,
      website = form.website.data
      
      
    )

    

    db.session.add(new_venue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()

    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  finally:
    db.session.close()

  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')




@venue.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  try:
    venue = Venue.query.filter_by(id=venue_id).first_or_404()

    db.session.delete(venue)
    
    db.session.commit()
    
    flash('Venue has been removed!')


    return render_template('pages/home.html')

  except:
    db.session.rollback()
    flash('Venue could not be removed!')

  finally:
    db.session.close()

    
  return None




#  Update
#  ----------------------------------------------------------------

@venue.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm(request.form)

  result = Venue.query.filter_by(id=venue_id).one()


  form.state.process_data(result.state)
  form.genres.process_data(result.genres)
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=result)



@venue.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  form = VenueForm(request.form)
  result = Venue.query.filter_by(id=venue_id).one()

  try:
     result.name = form.name.data
     result.genres = form.genres.data
     result.address = form.address.data
     result.city = form.city.data
     result.state = form.state.data
     result.phone = form.phone.data
     result.facebook_link = form.facebook_link.data
     result.website = form.website.data
     result.image_link = form.image_link.data
     result.seeking_talent = form.seeking_talent.data
     result.description = form.description.data
     db.session.add(result)
     db.session.commit()

     flash('Venue ' + form.name.data + ' was successfully Edited!')

  except:
    db.session.rollback()
    return('An error occurred')
    
    flash('An error occurred. Venue ' + form.name.data + ' could not be Edited.')

  finally:
    db.session.close()
  
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('venue.show_venue', venue_id=venue_id))