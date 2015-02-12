__author__ = 'kwhatcher'
from flask.ext.stormpath import user
from SDFtools.cache import cache
import  pywapi

def setuserwx(station):
    user.custom_data['wx'] = station
    user.save()

def getuserwxstation():
    print "ERROR ERROR ERROR ERROR"
    try:
        response = user.custom_data['wx']
    except:
        setuserwx('KMCN')
        response = user.custom_data['wx']
    return response

