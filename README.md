This Repo is a repo for a webserver that communicates to a maximum of 7 bluetooth serial passthrough modules to control the TV or Projectors to turn on /off, select inputs and other commands stated in the TV/Projector manual

Python library Flask will be used to host the webpage for :<br/>
1. Direct Control of each switch<br />
2. Presets macros configs<br />



Notes:
To add new bluetooth receivers:
1. modify /etc/bluetooth/rfcomm.conf<br />
2. Go into bluetoothctl<br />
3. Trust device <br />
4. "agent NoInputNoOutput"<br />
5. "default-agent"<br />
6. pair device (PIN: 1234)<br />
