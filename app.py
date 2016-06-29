#import serial
import os
import os.path
import json
from flask import Flask, render_template, request


app = Flask(__name__)
#if not(os.path.exists("/dev/rfcomm0")):
#    os.system("sudo rfcomm bind 0 30:14:11:25:14:38")

#btSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)

#btSerial.write(b"testing")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def testpage():
#    btSerial.write(b"testpage loaded\n")
    return render_template('index.html')
    # return 'testPage'

@app.route('/sendThings', methods = ['POST'])
def getresults():
    print("I got it!")
    print(request.form['data'])
    print("Switch is "+ request.form["switch"])
    return render_template('index.html')

@app.route('/setConfig', methods = ['POST'])
def setpresets():
    presetData = {"projLeft": "",
                "projRight": "",
                "tvAnnex": "",
                "tvAnnexInput": "",
                "tvReverse": "",
                "tvReverseInput": "",
                "tvBalcony": "",
                "tvBalconyInput": "",
                "tvFireplace": "",
                "tvFireplaceInput": ""
                }

    presetData["projLeft"] = request.form["projLeft"]
    presetData["projRight"] = request.form["projRight"]
    presetData["tvAnnex"] = request.form["tvAnnex"]
    presetData["tvAnnexInput"] = request.form["tvAnnexInput"]
    presetData["tvReverse"] = request.form["tvReverse"]
    presetData["tvReverseInput"] = request.form["tvReverseInput"]
    presetData["tvBalcony"] = request.form["tvBalcony"]
    presetData["tvBalconyInput"] = request.form["tvBalconyInput"]
    presetData["tvFireplace"] = request.form["tvFireplace"]
    presetData["tvFireplaceInput"] = request.form["tvFireplaceInput"]

    presetToConfig = request.form["congregationSel"]
    filename = ""
    if presetToConfig == "canto":
        filename = "cantoPreset.json"
    elif presetToConfig == "eng":
        filename = "engPreset.json"
    elif presetToConfig == "mando":
        filename = "mandoPreset.json"

    f = open(filename, 'w')
    f.write(json.dumps(presetData))
    f.close()





    return render_template('setConfigRedirect.html')

@app.route('/getConfig', methods=['GET'])
def getConfig():
    filename = ""
    if request.args['congregation'] == "canto":
        filename = "cantoPreset.json"
    elif request.args['congregation'] == "eng":
        filename = "engPreset.json"
    elif request.args['congregation'] == "mando":
        filename = "mandoPreset.json"

    if os.path.isfile(filename):
        return open(filename, 'r').read()
    else:
        return "File Not Found"


@app.route('/getDeviceCommands', methods=['GET'])
def getDeviceCommands():
    return open("DeviceCommands.json", 'r').read()

@app.route('/presetconfig')
def displayConfigPage():
    return render_template('presetconfig.html')

@app.route('/dashboard')
def displayDashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')