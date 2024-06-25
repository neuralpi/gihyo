// タッチのサポート状況のチェック用変数
var support = {
    pointer: window.navigator.pointerEnabled,
    mspointer: window.navigator.msPointerEnabled,
    touch: 'ontouchstart' in window
};

// タッチの場合わけ。pointer系：IE11以降、MSPointer系：IE10、touch系：android、iPhone、iPad
var touchStart = support.pointer ? 'pointerdown' : 
                 support.mspointer ? 'MSPointerDown' : 'touchstart';
var touchMove  = support.pointer ? 'pointermove' : 
                 support.mspointer ? 'MSPointerMove' : 'touchmove';
var touchEnd   = support.pointer ? 'pointerup' : 
                 support.mspointer ? 'MSPointerUp' : 'touchend';

window.onload = function(){
    // タッチエリアの設定
    var touchArea = document.getElementById("touchArea");

    // タッチイベントのイベントリスナーの登録
    touchArea.addEventListener(touchStart, touchEvent, false);
    touchArea.addEventListener(touchMove, touchEvent, false);
    touchArea.addEventListener(touchEnd, touchEndEvent, false);

    // クリックイベントのイベントリスナーの登録
    touchArea.addEventListener("click", clickEvent, false);
};

var url_base = '/9-4/get/';

// 前に送信したデューティー比を覚えておく
var rate25Prev = 0;
var rate24Prev = 0;

// デューティー比がth (0.0～1.0) 以上変化した時のみ値を送信
var th = 0.1;

// タッチ開始時とタッチ中のイベントリスナー
function touchEvent(e){
    e.preventDefault();

    // タッチ中のイベントのみ捕捉(IE)
    if(support.pointer || support.mspointer){
        if(e.pointerType != 'touch' && e.pointerType != 2){
            return;
        }
    }
    var touch = (support.pointer || support.mspointer) ? e : e.touches[0];
    var width = document.getElementById("touchArea").offsetWidth;

    if(touch.pageX < width/2){
        var rate = 0.7*(width/2-touch.pageX)/(width/2);
        if(Math.abs(rate-rate24Prev) > th){
            var url = url_base + '0/' + String(rate);
            fetch(url);
            rate25Prev = 0;
            rate24Prev = rate;
        }
    }else{
        var rate = 0.7*(touch.pageX-width/2)/(width/2);
        if(Math.abs(rate-rate25Prev) > th){
            var url = url_base + String(rate) + '/0';
            fetch(url);
            rate25Prev = rate;
            rate24Prev = 0;
        }
    }
}

// タッチ終了時のイベントリスナー
function touchEndEvent(e){
    e.preventDefault();

    var url = url_base + '0/0';
    fetch(url);
    rate25Prev = 0;
    rate24Prev = 0;
}

// クリック時のイベントリスナー（主にPC用）
function clickEvent(e){
    e.preventDefault();

    // タッチによるクリックは無視(IE)
    if(support.pointer || support.mspointer){
        if(e.pointerType == 'touch' || e.pointerType == 2){
            return;
        }
    }
    var width = document.getElementById("touchArea").offsetWidth;

    if(e.pageX >= 2*width/5 && e.pageX < 3*width/5){
        var url = url_base + '0/0';
        fetch(url);
        rate25Prev = 0;
        rate24Prev = 0;
    }else if(e.pageX < width/2){
        var rate = 0.7*(width/2-e.pageX)/(width/2);
        var url = url_base + '0/' + String(rate);
        fetch(url);
        rate25Prev = 0;
        rate24Prev = rate;
    }else{
        var rate = 0.7*(e.pageX-width/2)/(width/2);
        var url = url_base + String(rate) + '/0';
        fetch(url);
        rate25Prev = rate;
        rate24Prev = 0;
    }
}
