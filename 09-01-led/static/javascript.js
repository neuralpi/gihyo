var url_base = '/9-1/get/';

function toggleLED(gpio){
    var url = url_base + String(gpio);
    fetch(url)
    .then(function(response){
        return response.text();
    })
    .then(function(text){
        if(Number(text) == 1){
            document.getElementById("gpio25").className = "HIGH";
        }else{
            document.getElementById("gpio25").className = "LOW";
        }
    });
}
