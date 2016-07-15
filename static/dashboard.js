/*
Javascript file for dashboard.html

*/

var deviceCommands;
var xhr;

function startupScript(){
    fetchDeviceCommands();
}

function fetchDeviceCommands(){
    xhr = new XMLHttpRequest();
    var url = "getDeviceCommands";
    xhr.open("GET",url, true);
    xhr.send();

    xhr.addEventListener("readystatechange",
        function (){
            if(xhr.readyState == 4 && xhr.status == 200){
                deviceCommands = xhr.responseText;
                document.getElementById("text").innerHTML = JSON.parse(deviceCommands).SHARP.OFF;
            }else if(xhr.readyState == 4 && (xhr.status == 500 || xhr.status == 404)){
                alert("Device Commands Fetch Failed");
            }
    }, false);
}

function sendCommand(device, command, channel){
    var xhr = new XMLHttpRequest();
    var url = "sendCommand?device=" + device + "&command=" + command + "&channel=" + channel;
    xhr.open("GET",url, true);
    xhr.send();

    xhr.addEventListener("readystatechange",
        function (){
            if(xhr.readyState == 4 && xhr.status == 200){
                var response = xhr.responseText;
                document.getElementById("text").innerHTML = response;
            }else if(xhr.readyState == 4 && (xhr.status == 500 || xhr.status == 404)){
                alert("Commands Send Failed");
            }
    }, false);
}

function applyPreset(congregation){
    var xhr = new XMLHttpRequest();
    var url = "applyPreset?congregation=" + congregation;
    xhr.open("GET",url, true);
    xhr.send();

    xhr.addEventListener("readystatechange",
        function (){
            if(xhr.readyState == 4 && xhr.status == 200){
                var response = xhr.responseText;
                document.getElementById("text").innerHTML = response;
            }else if(xhr.readyState == 4 && (xhr.status == 500 || xhr.status == 404)){
                alert("Apply Preset Failed");
            }
    }, false);
}
