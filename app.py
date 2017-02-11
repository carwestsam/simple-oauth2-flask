from flask import Flask
from flask import redirect, request
from furl import furl
import random
import json
import requests
import os

client_id = ""
client_secret = ""
home_uri="https://xxxxxxxx.ngrok.io/"
redirect_uri = home_uri + "oauth/callback"
authorize_uri = ""
access_token_uri=""
scopes = ""
state = 'random state ' + str(random.randint(0, 10000))

code = ""
access_token = ""
token_type= ""
id_token= ""
refresh_token=""
xoauth_yahoo_guid=""

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/start")
def start():
    compressed_uri = furl(authorize_uri).set({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scopes,
        "state": state,
        "response_type": "code"
    }).url
    print("redirecting to : ", compressed_uri)
    return redirect(compressed_uri)

@app.route("/oauth/callback")
def oauthCodeCallback():
    print(request.args)

    if "code" in request.args:
        code = request.args.get('code')
        print('Got Code: ', code)

        result = requests.post(access_token_uri,
                      data={
                          'client_id':client_id,
                          'client_secret': client_secret,
                          'code' : code,
                          'redirect_uri' : redirect_uri,
                          'grant_type': 'authorization_code'
                      })

        print('result :' + result.text)
        kvs = json.loads(result.text)
        print (kvs)

        if "access_token" in kvs:
            global access_token, token_type, refresh_token, xoauth_yahoo_guid, id_token

            access_token = kvs['access_token']
            refresh_token = kvs['refresh_token']
            token_type = kvs['token_type']

            print('access_token:', access_token)
            print('refresh_token:', refresh_token)

            print('get access token successful')
            return redirect(home_uri)

        else :
            print("not get access token")
            return redirect(home_uri)

    else:
        return "something"

@app.route("/requests")
def requestData():

    global access_token

    print('access token', access_token)

    result = requests.get('', headers={
        'Authorization': 'Bearer ' + access_token
    })

    return result.text

if __name__ == "__main__":
    app.run()
