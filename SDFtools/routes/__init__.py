__author__ = 'kwhatcher'

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask.ext.stormpath import login_required, user
from flask.ext.stormpath import groups_required
from flask import render_template_string
import boto
from flask.ext import menu


from SDFtools.forms import AlertForm
from SDFtools.forms.user import ContactForm
from SDFtools.forms.user import SettingsForm
from SDFtools.models import gawxstations
from SDFtools.models.user import setuserwx


boto.set_stream_logger('boto')

gui = Blueprint('gui', __name__)


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