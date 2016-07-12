import serial
import os
import os.path
import json
from flask import Flask, render_template, request


app = Flask(__name__)
f = open("deviceMac.json")
address_json = json.loads(f.read())

for i in range(0, 6):
    if not(os.path.exists("/dev/rfcomm"+str(i))):
        os.system("sudo rfcomm bind " + str(i) + " " + address_json[str(i)])

leftProjSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)
rightProjSerial = serial.Serial("/dev/rfcomm1", baudrate=9600)
annexTVSerial = serial.Serial("/dev/rfcomm2", baudrate=9600)
reverseTVSerial = serial.Serial("/dev/rfcomm3", baudrate=9600)
balconyTVSerial = serial.Serial("/dev/rfcomm4", baudrate=9600)
fireplaceTVSerial = serial.Serial("/dev/rfcomm5", baudrate=9600)

deviceDictionary = {"0": leftProjSerial,
                    "1": rightProjSerial,
                    "2": annexTVSerial,
                    "3": reverseTVSerial,
                    "4": balconyTVSerial,
                    "5": fireplaceTVSerial
                    }




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def testpage():
    leftProjSerial.write(b"testpage loaded\n")
    return render_template('index.html')
    # return 'testPage'


@app.route('/sendThings', methods=['POST'])
def get_results():
    print("I got it!")
    print(request.form['data'])
    print("Switch is " + request.form["switch"])
    return render_template('index.html')


@app.route('/setConfig', methods=['POST'])
def set_presets():
    presetData = {"projLeft": "",
                "projRight": "",
                "tvAnnex": "",
                "tvAnnexInput": "",
                "tvReverse": "",
                "tvReverseInput": "",
                "tvBalcony": "",
                "tvBalconyInput": ""
                }

    presetData["projLeft"] = request.form["projLeft"]
    presetData["projRight"] = request.form["projRight"]
    presetData["tvAnnex"] = request.form["tvAnnex"]
    presetData["tvAnnexInput"] = request.form["tvAnnexInput"]
    presetData["tvReverse"] = request.form["tvReverse"]
    presetData["tvReverseInput"] = request.form["tvReverseInput"]
    presetData["tvBalcony"] = request.form["tvBalcony"]
    presetData["tvBalconyInput"] = request.form["tvBalconyInput"]

    preset_to_config = request.form["congregationSel"]
    filename = ""
    if preset_to_config == "canto":
        filename = "cantoPreset.json"
    elif preset_to_config == "eng":
        filename = "engPreset.json"
    elif preset_to_config == "mando":
        filename = "mandoPreset.json"

    g = open(filename, 'w')
    g.write(json.dumps(presetData))
    g.close()

    return render_template('setConfigRedirect.html')


@app.route('/getConfig', methods=['GET'])
def get_config():
    filename = ""
    if request.args['congregation'] == "canto":
        filename = "cantoPreset.json"
    elif request.args['congregation'] == "eng":
        filename = "engPreset.json"
    elif request.args['congregation'] == "mando":
        filename = "mandoPreset.json"

    if os.path.isfile(filename):
        return open(filename).read()
    else:
        return {"File": "Not Found"}


@app.route('/getDeviceCommands', methods=['GET'])
def get_device_commands():
    return open("DeviceCommands.json").read()


@app.route('/presetconfig')
def display_config_page():
    return render_template('presetconfig.html')


@app.route('/dashboard')
def display_dashboard():
    return render_template('dashboard.html')


@app.route('/sendCommand', methods=['GET'])
def send_command():
    """Handles html send commands from json file"""

    device = request.args['device']
    command = request.args['command']
    channel = request.args['channel']
    h = open("DeviceCommands.json")
    commands_json = json.loads(h.read())

    # TODO
    # implement deviceDictionary for different btSerial

    return write_command(channel, commands_json[device][command])


def write_command(channel, data):
    """Writes data to channel"""
    deviceDictionary[channel].write(bytes(data, 'UTF-8'))
    return data


@app.route('/status')
def status():
    rfcomm0 = "online"
    rfcomm1 = "online"
    # if not btSerial.isOpen():
    #     rfcomm0 = "offline"
    # if not btSerial2.isOpen():
    #     rfcomm1 = "offline"
    return render_template('status.html', rfcomm0=rfcomm0, rfcomm1=rfcomm1)


@app.route('/applyPreset', methods=['GET'])
def applypreset():
    """Applies(Executes) a preset"""
    congregationpreset = request.args['congregation']

    h = open("DeviceCommands.json")
    commands_json = json.loads(h.read())

    j = open("" + congregationpreset + "Preset.json")

    congragation_json = json.loads(j.read())
    #############################################################################
    choice = congragation_json["projLeft"]

    if choice == "on":
        write_command("0", commands_json["BENQ", "ON"])
    elif choice == "off":
        write_command("0", commands_json["BENQ", "OFF"])
    #############################################################################
    choice = congragation_json["projRight"]

    if choice == "on":
        write_command("1", commands_json["BENQ", "ON"])
    elif choice == "off":
        write_command("1", commands_json["BENQ", "OFF"])
    #############################################################################
    choice = congregationpreset["tvAnnex"]

    if choice == "on":
        write_command("2", commands_json["SHARP", "ON"])
    elif choice == "off":
        write_command("2", commands_json["SHARP", "OFF"])
    #############################################################################
    choice = congregationpreset["tvAnnexInput"]

    if choice == "input":
        write_command("2", commands_json["SHARP", "INPUT1"])
    #############################################################################
    choice = congregationpreset["tvReverse"]

    if choice == "on":
        write_command("3", commands_json["SHARP", "ON"])
    elif choice == "off":
        write_command("3", commands_json["SHARP", "OFF"])
    #############################################################################
    choice = congregationpreset["tvReverseInput"]

    if choice == "input":
        write_command("3", commands_json["SHARP", "INPUT1"])
    #############################################################################
    choice = congregationpreset["tvBalcony"]

    if choice == "on":
        write_command("4", commands_json["SHARP", "ON"])
    elif choice == "off":
        write_command("4", commands_json["SHARP", "OFF"])
    #############################################################################
    choice = congregationpreset["tvBalconyInput"]

    if choice == "input":
        write_command("4", commands_json["SHARP", "INPUT1"])
    #############################################################################

    return "OKOKOK"
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
