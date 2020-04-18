
from app.extensions import db
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, Blueprint

from app.models import Show, Venue, Artist
from app.forms import *


show = Blueprint('show', __name__)




#  Shows
#  ----------------------------------------------------------------



@show.route('/shows')
def shows():

  shows = Show.query.all()


  data = []


  for show in shows:
        venue = Venue.query.get(show.venue_id)
        artist = Artist.query.get(show.artist_id)
        data.extend([{
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        }])
  
  return render_template('pages/shows.html', shows=data)



@show.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@show.route('/shows/create', methods=['POST'])
def create_show_submission():

  form = ShowForm()

  try:
    show = Show()
    show.artist_id = form.artist_id.data
    show.venue_id = form.venue_id.data
    show.start_time = form.start_time.data
    db.session.add(show)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')

  finally:
    db.session.close()

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
