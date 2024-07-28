var sliderMin = 0;
var sliderMax = 20;
var sliderStep = 1;
var sliderValue = 0;

var url_base = '/9-3/get/';

// jQuery UIによるスライダの設定
$(function(){
    // スライダを動かしたときに呼ばれるイベントハンドラの設定
    var sliderHandler1 = function(e, ui){
        var ratio = ui.value/sliderMax;
        // 共通アノードの場合次の行を有効に
        //ratio = 1.0 - ratio;
        var url = url_base + '25/' + String(ratio);
        fetch(url);
    };
    var sliderHandler2 = function(e, ui){
        var ratio = ui.value/sliderMax;
        // 共通アノードの場合次の行を有効に
        //ratio = 1.0 - ratio;
        var url = url_base + '24/' + String(ratio);
        fetch(url);
    };
    var sliderHandler3 = function(e, ui){
        var ratio = ui.value/sliderMax;
        // 共通アノードの場合次の行を有効に
        //ratio = 1.0 - ratio;
        var url = url_base + '23/' + String(ratio);
        fetch(url);
    };

    // 3つのスライダへ設定を適用
    $( "#slider1" ).slider({
        min: sliderMin,
        max: sliderMax,
        step: sliderStep,
        value: sliderValue,
        change: sliderHandler1,
        slide: sliderHandler1
    });
    $( "#slider2" ).slider({
        min: sliderMin,
        max: sliderMax,
        step: sliderStep,
        value: sliderValue,
        change: sliderHandler2,
        slide: sliderHandler2
    });
    $( "#slider3" ).slider({
        min: sliderMin,
        max: sliderMax,
        step: sliderStep,
        value: sliderValue,
        change: sliderHandler3,
        slide: sliderHandler3
    });
});
