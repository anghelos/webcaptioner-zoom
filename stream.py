# stream.py
# Send captions from Web Captioner to Zoom Meeting.

import os, sys, json, logging, requests
from flask import Flask, request, make_response
from datetime  import datetime

# global constants/flags
DEBUG = False
PORT = 9999
LINE_LENGTH = 80
ZOOM_API_TOKEN = "YOUR_ZOOM_API_TOKEN"
LANGAUGE = "en-US"  # Language code - ISO country code, e.g. de-DE.
counter = 0

if not DEBUG:
    # if we're not debugging hide requests
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

# clear function
def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')

# define a flask app
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Hello world!"

@flask_app.route('/transcribe', methods=['GET'])
def transcribe_get():
    return make_response("Can access /transcribe just fine", 200,
    {"Access-Control-Allow-Origin": "https://webcaptioner.com"})

# main post request handler
@flask_app.route('/transcribe', methods=['POST', 'PUT'])
def transcribe_post():
    # for some reason, response.get_json won't parse right
    # so we'll make json ourselves
    data = json.loads(request.get_data(as_text=True))
    reqText = data['transcript']
    sequence = data['sequence']

    # send captions to zoom
    url = ZOOM_API_TOKEN \
        + "&seq=" + str(sequence) \
        + "&lang=" + LANGAUGE
    content = reqText + ' '
    headers = {'content-type': 'text/plain'}

    r = requests.post(url=url, data=content.encode('utf-8'), headers=headers)

    # print the request
    print(url)
    print(sequence, content)
    sys.stdout.flush()

    # break every 80 characters
    global counter
    if counter >= LINE_LENGTH:
        print('')
        counter = 0
    else:
        counter += (len(reqText) + 1)

    # return a correct response
    return make_response(json.dumps({"message": "recieved"}), 200,
    {"Content-Type": 'application/json',
     "Access-Control-Allow-Origin": "https://webcaptioner.com"
    })

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', debug=DEBUG, port=PORT, ssl_context=('cert.pem', 'key.pem'))
