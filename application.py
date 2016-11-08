""" Demo Flask + LWA application """
from flask import Flask
from flask import render_template
from flask import request
import requests, urllib2, os

application = Flask(__name__)
LWA = {"AMAZON_CLIENT_ID" : os.environ['AMAZON_CLIENT_ID'],
       "AMAZON_CLIENT_SECRET" : os.environ['AMAZON_CLIENT_SECRET']}

@application.route("/")
def home():
    """Home Screen"""
    return render_template('main.html', lwa=LWA)

@application.route("/callback")
def callback():
    """LWA callback"""
    access_token = request.args.get('access_token')
    code = request.args.get('code')
    blurb = ""

    if code:
        request_parameters = {'grant_type': 'authorization_code',
                              'code': code,
                              'client_id': LWA["AMAZON_CLIENT_ID"],
                              "client_secret" : LWA["AMAZON_CLIENT_SECRET"]}
        response = requests.post("https://api.amazon.com/auth/o2/token", data=request_parameters)
        access_token = response.json()['access_token']
        blurb = "Access Token Request: %s \n\n" % response.json()

    if access_token:
        profile = urllib2.urlopen("https://api.amazon.com/user/profile?access_token=" + access_token).read()
        blurb = blurb + "Profile: %s" % profile

    return render_template('main.html', lwa=LWA, blurb=blurb)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=int("3000"))
