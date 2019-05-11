import Adafruit_BMP.BMP085 as BMP085
import requests
import RPi.GPIO
import time
import datetime
from flask import Flask, request
import thread

SLEEP_SECOND = 2
OPENED = False
REMOTE_SERVER_URL = "http://192.168.137.1:8000/data"

app = Flask(__name__)

def getValue(name, value):
    global OPENED
    while OPENED:
        sensor = BMP085.BMP085()
        temperature = '{0:0.2f} *C'.format(sensor.read_temperature())
        pressure = '{0:0.2f} Pa'.format(sensor.read_pressure())
        altitude = '{0:0.2f} m'.format(sensor.read_altitude())
        sealevelPressure = '{0:0.2f} Pa'.format(sensor.read_sealevel_pressure())
        if temperature != None:
            send_data = {"t":temperature, "p":pressure ,"a":altitude, "sp":sealevelPressure}
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            print("time: " + str(datetime.datetime.now()))
            print("send {0}".format(send_data))
        time.sleep(SLEEP_SECOND)

@app.route('/', methods=['GET'])
def index():
    global OPENED
    if 'op' in request.args:
        if request.args['op'] == "on" and not OPENED:
            OPENED = True
            thread.start_new_thread(getValue, ("getValue", None))

        elif request.args['op'] == "off" and OPENED:
            OPENED = False
    return 'ok'

app.run(host='0.0.0.0')