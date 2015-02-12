__author__ = 'kwhatcher'

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask.ext.stormpath import login_required, user
from flask.ext.stormpath import groups_required
import boto
from flask.ext import menu
from flask.ext import restful




from SDFtools.forms import AlertForm
from SDFtools.forms.user import ContactForm
from SDFtools.forms.user import SettingsForm

from SDFtools.models import gawxstations
from SDFtools.models.user import setuserwx
from SDFtools.models import missions
from SDFtools.models import blutrac



boto.set_stream_logger('boto')

gui = Blueprint('gui', __name__)
api = restful.Api(gui)

sns = boto.connect_sns()
snstopic_arn = "arn:aws:sns:us-east-1:150179862823:5bde_alerts"

@gui.route('/')
@menu.register_menu(gui, 'Home', 'Dashboard')
@login_required
def hello_world():
    return render_template('base.html')

@gui.route('/alert')
@menu.register_menu(gui, 'Send Alert', 'Send Alert')
@groups_required(['approved'])
def send_alert():
 
    subscriptions = sns.get_all_subscriptions_by_topic(snstopic_arn)
    return render_template('alert.html', form=AlertForm(), subscriptions=subscriptions  )

@gui.route('/submit', methods=('GET', 'POST'))
@groups_required(['approved'])
def submit():
 
    form = AlertForm()
    if form.validate_on_submit():

        msg = "Hi there\nI am sending this message over boto.\nYour booty Jan"
        subj = form.data['msg']

        res = sns.publish(snstopic_arn, msg, subj)
        flash('Message Sent')
        return redirect('/alert')
    return render_template('submit.html', form=form)

@gui.route('/success')
@groups_required(['approved'])
def success():
 
    return render_template('success.html', form=AlertForm() )


@gui.route('/settings')
@login_required
def settings():
 
    stations = gawxstations()
    return render_template('settings.html', user=user , form=SettingsForm())

@gui.route('/settings/submit', methods=('GET', 'POST'))
@login_required
def settingssubmit():
    form = SettingsForm()
    if form.validate_on_submit():
        flash('Data Received')
        station = form.data['wxstation']
        print station
        setuserwx(station)
        return redirect('/settings')
    stations = gawxstations()
    flash('Data error')
    return render_template('settings.html', user=user , form=SettingsForm())

@gui.route('/profile')
@login_required
def profile():
 
    return render_template('profile.html', user=user , contactform=ContactForm())

@gui.route('/profile/submit', methods=('GET', 'POST'))
@groups_required(['approved'])
def profilesubmit():
 
    form = ContactForm()
    if form.validate_on_submit():
        user.custom_data['phone'] = form.data['phone']
        user.save()
        print('User Data:')
        print user.custom_data['phone']
        flash('Data Received')
        return redirect('/profile')
    return render_template('profile.html', contactform=ContactForm())

@gui.route('/help')
@login_required
def help():
    return render_template('help.html' )


""" Missions Tracker """

@gui.route('/missions')
@menu.register_menu(gui, 'missiontracker', 'Mission Tracker')
@groups_required(['approved'])
def missionsroot():
    data = missions.getallmissions()
    urls = []
    for item in data:
        #print "##################SAD TESTINGS#############################"
        #print item['SAD_ID']
        url = missions.getmissionurl(item['SAD_ID'])
        #print url
        urls.append(url)

    print urls
    return render_template('missions.html', data=data, urls=urls)

""" BluTrac """

@gui.route('/blutrac')
@menu.register_menu(gui, 'blutrac', 'Troop Tracker')
@groups_required(['5BDE HQ'])
def trackerroot():
    #data = missions.getallmissions()
    return render_template('blutrac.html')

""" API """

class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}

locations = {'hat': {'lat': 45, 'log': 22}, 'jim': {'lat': 17, 'log': 82}}


from flask.ext.restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()
parser.add_argument('location', type=str)
parser.add_argument('lat', type=str)
parser.add_argument('log', type=str)
parser.add_argument('user', type=str)


class Location(restful.Resource):
    def get(self, userid):
        return blutrac.getuserlast(userid)

    def put(self, userid):
        args = parser.parse_args()
        locations[userid] = {'location': args['location']}
        print args['location']
        print locations[userid]
        return {locations: locations[userid]}

# LocationList
#   shows a list of all todos, and lets you POST to add new tasks
class LocationList(Resource):
    def get(self):
        users = {'hat6974'}
        data = blutrac.getallusers(users)
        print data
        return data

    def post(self):
        results={}
        #print request.json
        args = parser.parse_args()
        #print args
        blutrac.updateuser(args['user'],args['lat'], args['log'])
        locations[args['user']] = {args['user']: {'lat': args['lat'], 'log': args['log']}}
        print locations[args['user']]
        return locations[args['user']], 201

"""
[kwhatcher@hatchlap ~]$ curl -H "Content-type: application/json" http://localhost:5000/api/locations -d "{\"location\": \"32.333\",\"user\": \"kerry\"}" -X POST -v
[kwhatcher@hatchlap ~]$ curl -H "Content-type: application/json" http://localhost:5000/api/locations   -X GET -v
"""

api.add_resource(LocationList, '/api/locations')
api.add_resource(Location, '/api/locations/<string:userid>')