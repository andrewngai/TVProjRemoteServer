import serial
import os
from flask import Flask, render_template, request


app = Flask(__name__)
if not(os.path.exists("/dev/rfcomm0")):
    os.system("sudo rfcomm bind 0 30:14:11:25:14:38")

btSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)

btSerial.write(b"testing")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def testpage():
    btSerial.write(b"testpage loaded\n")
    return render_template('index.html')
    # return 'testPage'

@app.route('/sendThings', methods = ['POST'])
def getresults():
    print("I got it!")
    print(request.form['data'])
    print("Switch is "+ request.form["switch"])
    return render_template('index.html')

@app.route('/getConfig')
def getpresets():
    return render_template('presetconfig.html')

@app.route('/presetconfig')
def displayConfigPage():
    return render_template('presetconfig.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')