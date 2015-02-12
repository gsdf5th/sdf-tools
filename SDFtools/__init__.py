__author__ = 'kwhatcher'


from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from os.path import expanduser
from flask.ext.stormpath import StormpathManager
from flask.ext import menu
from os import environ

from flask.ext.cors import CORS

import ast
from flask.ext.cache import Cache




from routes import gui
from cache import cache
from SDFtools.api import api
from SDFtools import weather
from SDFtools import gmaps




app = Flask(__name__)

app.register_blueprint(gui)

app.register_blueprint(api, urlprefix="api")

Bootstrap(app)
app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)
#app.config['SECRET_KEY'] = "734yt98473yt734ytc98y3tn98y897r67no"
#app.config['STORMPATH_API_KEY_FILE'] = expanduser('~/.stormpath')

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
app.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')

app.config['STORMPATH_APPLICATION'] = 'gsdf5th'
app.config['STORMPATH_ENABLE_GOOGLE'] = True
app.config['STORMPATH_SOCIAL'] = {
    'GOOGLE': {
        'client_id': environ.get('GOOGLE_CLIENT_ID'),
        'client_secret': environ.get('GOOGLE_CLIENT_SECRET'),
    }
}


#app.config['STORMPATH_LOGIN_TEMPLATE'] = 'login.html'

stormpath_manager = StormpathManager(app)
menu.Menu(app=app)
app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}
cors = CORS(app)



weather.Weather(app=app)
gmaps.Gmap(app=app)







