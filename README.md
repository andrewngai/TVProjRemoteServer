This Repo is a repo for a webserver that communicates to a maximum of 7 bluetooth serial passthrough modules to control the TV or Projectors to turn on /off, select inputs and other commands stated in the TV/Projector manual

Python library Flask will be used to host the webpage for :<br/>
1. Direct Control of each switch<br />
2. Presets macros configs<br />

Schematic: <br/>
![alt tag](https://cloud.githubusercontent.com/assets/14185939/16537569/17fcd0ce-3fbb-11e6-9532-a1019858d785.png)

Notes:<br />
To add new bluetooth receivers:<br />
1. <strike>modify /etc/bluetooth/rfcomm.conf</strike><br />
2. Go into bluetoothctl<br />
3. Trust device <br />
4. "agent NoInputNoOutput"<br />
5. "default-agent"<br />
6. pair device (PIN: 1234)<br />
