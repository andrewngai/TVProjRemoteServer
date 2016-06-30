/*
Javascript file for presetconfig.html
*/

function submitButtonAction(){
        if(isFormValid()){
            document.getElementById("configForm").submit();
        }else{
            alert("Please fill in all the fields");
        }

    }



function isFormValid(){
    var isConSelValid           = isFieldValid("congregationSel");
    var isProjLeftValid         = isFieldValid("projLeft");
    var isProjRightValid        = isFieldValid("projRight");
    var isTvAnnexValid          = isFieldValid("tvAnnex");
    var isTvAnnexInputValid     = isFieldValid("tvAnnexInput");
    var isTvReverseValid        = isFieldValid("tvReverse");
    var isTvReverseInputValid   = isFieldValid("tvReverseInput");
    var isTvBalconyValid        = isFieldValid("tvBalcony");
    var isTvBalconyInputValid   = isFieldValid("tvBalconyInput");
    var isTvFireplaceValid      = isFieldValid("tvFireplace");
    var isTvFireplaceInputValid = isFieldValid("tvFireplaceInput");

    return isConSelValid &&
           isProjLeftValid &&
           isProjRightValid &&
           isTvAnnexValid &&
           isTvAnnexInputValid &&
           isTvReverseValid &&
           isTvReverseInputValid &&
           isTvBalconyValid &&
           isTvBalconyInputValid &&
           isTvFireplaceValid &&
           isTvFireplaceInputValid ;
}


function isFieldValid(field){
    var x = document.getElementsByName(field);
    var i;

    var isValid = 0;

    for(i = 0;i<x.length;i++){
        if(x[i].checked == true){
            isValid = 1;
            break;
        }
        if(i == x.length-1){
            isValid = 0;
        }
    }

    return isValid;
}

var congregationPreset;
var getPresetRequest;
var presetJson;
if (!presetJson){
    presetJson = {};
}

function congregationChange(){
    var form_elements = document.getElementById('configForm').elements;
    var congregation = form_elements['congregationSel'].value;
    fetchCongregationPreset(congregation);
}

function fetchCongregationPreset(congregation){
    getPresetRequest = new XMLHttpRequest();
    var url = "getConfig?congregation=" + congregation;
    getPresetRequest.open("GET",url, true);
    getPresetRequest.send();

    getPresetRequest.addEventListener("readystatechange",
        function (){
            if(getPresetRequest.readyState == 4 && getPresetRequest.status == 200){
                congregationPreset = getPresetRequest.responseText;
                presetJson = JSON.parse(congregationPreset);
                //alert(congregationPreset);
                applyPreset();
            }
    }, false);
}

function applyPreset(){
    switch(presetJson.projLeft){
        case 'on':
            document.getElementById("projLeftOnRadio").checked = true;
            break;
        case 'off':
            document.getElementById("projLeftOffRadio").checked = true;
            break;
        case 'na':
            document.getElementById("projLeftNARadio").checked = true;
            break;
        default:
            alert("projLeft default action");
    }

    switch(presetJson.projRight){
        case 'on':
            document.getElementById("projRightOnRadio").checked = true;
            break;
        case 'off':
            document.getElementById("projRightOffRadio").checked = true;
            break;
        case 'na':
            document.getElementById("projRightNARadio").checked = true;
            break;
        default:
            alert("projRight default action");
    }

    switch(presetJson.tvAnnex){
        case 'on':
            document.getElementById("tvAnnexOnRadio").checked = true;
            break;
        case 'off':
            document.getElementById("tvAnnexOffRadio").checked = true;
            break;
        case 'na':
            document.getElementById("tvAnnexNARadio").checked = true;
            break;
        default:
            alert("tvAnnex default action");
    }
    switch(presetJson.tvAnnexInput){
        case 'input':
            document.getElementById("tvAnnexInputDefaultRadio").checked = true;
            break;
        case 'na':
            document.getElementById("tvAnnexInputNARadio").checked = true;
            break;
        default:
            alert("tvAnnexInput default action");
    }

    switch(presetJson.tvReverse){
        case 'on':
            document.getElementById("tvReverseOnRadio").checked = true;
            break;
        case 'off':
            document.getElementById("tvReverseOffRadio").checked = true;
            break;
        case 'na':
            document.getElementById("tvReverseNARadio").checked = true;
            break;
        default:
            alert("tvReverse default action");
    }
    switch(presetJson.tvReverseInput){
        case 'input':
            document.getElementById("tvReverseInputDefaultRadio").checked = true;
            break;
        case 'na':
            document.getElementById("tvReverseInputNARadio").checked = true;
            break;
        default:
            alert("tvReverseInput default action");
    }

    switch(presetJson.tvBalcony){
        case 'on':
            document.getElementById("tvBalconyOnRadio").checked = true;
            break;
        case 'off':
            document.getElementById("tvBalconyOffRadio").checked = true;
            break;
        case 'na':
            document.getElementById("tvBalconyNARadio").checked = true;
            break;
        default:
            alert("tvBalcony default action");
    }
    switch(presetJson.tvBalconyInput){
        case 'input':
            document.getElementById("tvBalconyInputDefaultRadio").checked = true;
            break;
        case 'na':
            document.getElementById("tvBalconyInputNARadio").checked = true;
            break;
        default:
            alert("tvBalconyInput default action");
    }

    switch(presetJson.tvFireplace){
        case 'on':
            document.getElementById("tvFireplaceOnRadio").checked = true;
            break;
        case 'off':
            document.getElementById("tvFireplaceOffRadio").checked = true;
            break;
        case 'na':
            document.getElementById("tvFireplaceNARadio").checked = true;
            break;
        default:
            alert("tvBalcony default action");
    }
    switch(presetJson.tvFireplaceInput){
        case 'input':
            document.getElementById("tvFireplaceInputDefaultRadio").checked = true;
            break;
        case 'na':
            document.getElementById("tvFireplaceInputNARadio").checked = true;
            break;
        default:
            alert("tvFireplaceInput default action");
    }

}