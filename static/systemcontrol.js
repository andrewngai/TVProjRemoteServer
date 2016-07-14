function restartsystem(delay){
    var xhr = new XMLHttpRequest();
    var url = "system_restart?delay="+delay;
    xhr.open("GET",url, true);
    xhr.send();

    xhr.addEventListener("readystatechange",
        function (){
            if(xhr.readyState == 4 && xhr.status == 200){
                document.getElementById("text").innerHTML = xhr.responseText;
            }else if(xhr.readyState == 4 && (xhr.status == 500 || xhr.status == 404)){
                alert("Reset Commands  Failed");
            }
    }, false);
}
