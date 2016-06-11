import serial
from flask import Flask, render_template
from time import sleep

app = Flask(__name__)
bluetoothSerial = serial.Serial("/dev/rfcomm1",baudrate=9600)



bluetoothSerial.write("testing")


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')