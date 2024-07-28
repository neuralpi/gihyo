var url = '/9-2/get';

window.onload = function(){
    getTempPeriodic(2000);
}

// millisミリ秒ごとに温度を取得する関数
function getTempPeriodic(millis){

    fetch(url)
    .then(function(response){
        return response.text();
    })
    .then(function(text){
        document.getElementById("temp_text").value = text;
    });

    // millisミリ秒後に自分自身を呼び出す
    setTimeout(function(){ getTempPeriodic(millis); }, millis);
}
