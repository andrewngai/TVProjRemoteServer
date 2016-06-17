import serial
import os
from flask import Flask, render_template


app = Flask(__name__)
if not(os.path.exists("/dev/rfcomm0")):
    os.system("sudo rfcomm bind 0 30:14:11:25:14:38")

btSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)

btSerial.write(b"testing")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/testpage')
def testpage():
    # btSerial.write(b"testpage loaded\n")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')