var sliderMin = 0;
var sliderMax = 20;
var sliderStep = 1;
var sliderValue0 = sliderMax/2;
var sliderValue1 = sliderMax/2;

var url_base = '/9-5/get/';

// jQuery UIによるスライダの設定
$(function() {
    // スライダを動かしたときに呼ばれるイベントハンドラの設定
    var sliderHandler0 = function(e, ui){
        var ratio = ui.value/sliderMax;
        // サーボモーターを逆向きに回転させたい場合次の行を有効に
        //ratio = 1.0 - ratio;
        var url = url_base + '0/' + String(ratio);
        fetch(url);
    };
    var sliderHandler1 = function(e, ui){
        var ratio = ui.value/sliderMax;
        // サーボモーターを逆向きに回転させたい場合次の行を有効に
        //ratio = 1.0 - ratio;
        var url = url_base + '1/' + String(ratio);
        fetch(url);
    };

    // スライダへ設定を適用
    $( "#slider0_servo" ).slider({
        min: sliderMin,
        max: sliderMax,
        step: sliderStep,
        value: sliderValue0,
        change: sliderHandler0,
        slide: sliderHandler0
    });
    $( "#slider1_servo" ).slider({
        min: sliderMin,
        max: sliderMax,
        step: sliderStep,
        value: sliderValue1,
        change: sliderHandler1,
        slide: sliderHandler1
    });
});

