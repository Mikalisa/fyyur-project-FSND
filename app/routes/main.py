
from flask import Blueprint, render_template


main = Blueprint('main', __name__)



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@main.route('/')
def index():
  return render_template('pages/home.html')



@main.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500




