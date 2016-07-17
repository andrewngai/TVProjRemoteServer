import json
import os
import os.path
import serial
from flask import Flask, render_template, request
import sys

pid = str(os.getpid())
pidfile = "/tmp/mydaemon.pid"

if os.path.isfile(pidfile):
    # print "%s already exists, exiting" % pidfile
    os.system("sudo rm /tmp/mydaemon.pid")
pidFile = open(pidfile, 'w')
pidFile.write(pid)
pidFile.close()

app = Flask(__name__)
f = open("/home/pi/TVProjRemoteServer/deviceMac.json")
address_json = json.loads(f.read())

os.system("sudo /home/pi/hub-ctrl.c/hub-ctrl -h 0 -P 4 -p 0 ; sleep 3; sudo /home/pi/hub-ctrl.c/hub-ctrl  -h 0 -P 4 -p 1")

for i in range(0, 6):
    if not(os.path.exists("/dev/rfcomm"+str(i))):
        os.system("sudo rfcomm bind " + str(i) + " " + address_json[str(i)])

# Channel 0: Annex TV
# Channel 1: Reverse TV
# Channel 2: Balcony TV
# Channel 3: Left Projector
# Channel 4: Right Projector
# Channel 5:


channel_zero_serial = serial.Serial("/dev/rfcomm0", baudrate=9600)
channel_one_serial = serial.Serial("/dev/rfcomm1", baudrate=9600)
channel_two_serial = serial.Serial("/dev/rfcomm2", baudrate=9600)
channel_three_serial = serial.Serial("/dev/rfcomm3", baudrate=9600)
channel_four_serial = serial.Serial("/dev/rfcomm4", baudrate=9600)
channel_five_serial = serial.Serial("/dev/rfcomm5", baudrate=9600)

deviceDictionary = {"0": channel_zero_serial,
                    "1": channel_one_serial,
                    "2": channel_two_serial,
                    "3": channel_three_serial,
                    "4": channel_four_serial,
                    "5": channel_five_serial
                    }


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/test')
def testpage():
    return render_template('index.html')

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
    filename="/home/pi/TVProjRemoteServer/"+filename
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

    filename="/home/pi/TVProjRemoteServer/"+filename
    if os.path.isfile(filename):
        return open(filename).read()
    else:
        return {"File": "Not Found"}


@app.route('/getDeviceCommands', methods=['GET'])
def get_device_commands():
    return open("/home/pi/TVProjRemoteServer/DeviceCommands.json").read()


@app.route('/presetconfig')
def display_config_page():
    return render_template('presetconfig.html')


# @app.route('/dashboard')
# def display_dashboard():
#     return render_template('dashboard.html')
#

@app.route('/sendCommand', methods=['GET'])
def send_command():
    """Handles html send commands from json file"""

    device = request.args['device']
    command = request.args['command']
    channel = request.args['channel']
    h = open("/home/pi/TVProjRemoteServer/DeviceCommands.json")
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
    rfcomm = {"0": "online O",
              "1": "online O",
              "2": "online O",
              "3": "online O",
              "4": "online O",
              "5": "online O"
              }

    for deviceIndex in range(0, 6):
        try:
            deviceDictionary[str(deviceIndex)].write("testing")
        except Exception:
            rfcomm[str(deviceIndex)] = "offline X"

    return render_template('status.html', rfcomm0=rfcomm[str(0)], rfcomm1=rfcomm[str(1)], rfcomm2=rfcomm[str(2)], rfcomm3=rfcomm[str(3)], rfcomm4=rfcomm[str(4)], rfcomm5=rfcomm[str(5)])


@app.route('/applyPreset', methods=['GET'])
def applypreset():
    """Applies(Executes) a preset"""
    congregationpreset = request.args['congregation']

    h = open("/home/pi/TVProjRemoteServer/DeviceCommands.json")
    commands_json = json.loads(h.read())

    j = open("/home/pi/TVProjRemoteServer/" + congregationpreset + "Preset.json")

    congragation_json = json.loads(j.read())
    #############################################################################
    choice = congragation_json["projLeft"]

    if choice == "on":
        write_command("3", commands_json["BENQ", "ON"])
    elif choice == "off":
        write_command("3", commands_json["BENQ", "OFF"])
    #############################################################################
    choice = congragation_json["projRight"]

    if choice == "on":
        write_command("4", commands_json["BENQ", "ON"])
    elif choice == "off":
        write_command("4", commands_json["BENQ", "OFF"])
    #############################################################################
    choice = congregationpreset["tvAnnex"]

    if choice == "on":
        write_command("0", commands_json["SHARP", "ON"])
    elif choice == "off":
        write_command("0", commands_json["SHARP", "OFF"])
    #############################################################################
    choice = congregationpreset["tvAnnexInput"]

    if choice == "input":
        write_command("0", commands_json["SHARP", "INPUT1"])
    #############################################################################
    choice = congregationpreset["tvReverse"]

    if choice == "on":
        write_command("1", commands_json["SHARP", "ON"])
    elif choice == "off":
        write_command("1", commands_json["SHARP", "OFF"])
    #############################################################################
    choice = congregationpreset["tvReverseInput"]

    if choice == "input":
        write_command("1", commands_json["SHARP", "INPUT1"])
    #############################################################################
    choice = congregationpreset["tvBalcony"]

    if choice == "on":
        write_command("2", commands_json["SHARP", "ON"])
    elif choice == "off":
        write_command("2", commands_json["SHARP", "OFF"])
    #############################################################################
    choice = congregationpreset["tvBalconyInput"]

    if choice == "input":
        write_command("2", commands_json["SHARP", "INPUT1"])
    #############################################################################

    return "OKOKOK"


@app.route('/system_control')
def systemcontrolpage():
    return render_template('systemcontrol.html')


@app.route('/system_restart', methods=['GET'])
def restart_system():
    delay = request.args['delay']
    os.system("(sleep " + delay + ";sudo reboot) &")
    return "System restarting in " + delay + " second(s)"


@app.route('/pull_new_code')
def pull_new_code():
    return os.popen("cd /home/pi/TVProjRemoteServer;git pull").read()

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
