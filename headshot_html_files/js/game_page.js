var money;
var button = '4';
var answer_time = -1;

$(document).ready(function(){


//    $("#game-slider").slider({
//        range: "min",
//        value: 0.20,
//        min: 0,
//        max: 10,
//        step: 0.05,
//        slide: function(event, ui) {
//            $("#current-user-number-text3").text(ui.value + "\u20ac");
//            money = ui.value;
//        }
//    });
/*    $('.options').click(function(){
        $(this).toggle(function(){
                $(this).attr("src","{{ static_url('images/option-b.png') }}");
            },
            function(){
                $(this).attr("src","{{ static_url('images/option-w.png') }}");
            });
    });*/
});

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}



function setButtonSelected(option){
        console.log(option)
        console.log("answer by user")
    /*console.log("Inside setButtonSelected function");
    $(this).toggle(function(){
        console.log("inside toggle");
            $(option).attr("src","{{ static_url('images/option-b.png') }}");

        },
        function(){

            $(this).attr("src","{{ static_url('images/option-w.png') }}");


        });*/
        var opt_id=option+1;
        $('.options').attr('src',"/static/images/option-w.png");
        $('.options' + option).attr('src','/static/images/option-b.png');
/*
        $('#opt' + opt_id).css('color','#ffffff');
*/
    button = option;
    answer_time = parseInt($("#clock").text());
}

function  getAnswerTime(){
    if(answer_time === -1){
        return answer_time.toString();
        }
    return (10 - answer_time).toString();
}

function  getButtonSelected(){
    console.log("Inside getButtonSelected function");
    return button;
}

// Animation to transfer user hexagon to bottom position
// Accepts id of hexagon to be moved
function startUserSeatAnimation(seat){

    // gets current position class
    var className = $("#"+seat).attr('class');
    // gets position number
    var pos = parseInt(className.toString().slice(8));
    var class1;
    var class2;
    var i = 0;

    // sets number of iterations
    if (pos < 5){
        var n = 4-pos;
    } else if (pos > 5){
        var n = pos-6;
    }

    // if not at bottom most position, move to bottom
    if(pos !== 5) {

        // move at intervals of 1500 ms
        var animation = setInterval(function () {

            // when at bottom, stop and show user hexagon
            if (i >= n) {
                clearInterval(animation);
                console.log("rotation finished "+ seat);
                showCurrentUser(seat);
            }

            // switches each hexagon position to the next
            for (var j = 1; j <= 10; j++) {

                class1 = parseInt($("#seat_" + j).attr('class').toString().slice(8));

                // if on the right side, shifts it to next position class
                if (pos < 5) {

                    if (class1 === 9)
                        class2 = 0;
                    else
                        class2 = class1 + 1;

                // if on the left side, shifts to previous position class
                } else if (pos > 5) {

                    if (class1 === 0)
                        class2 = 9;
                    else
                        class2 = class1 - 1;
                }

                // adjusts position class of background hexagon, profile pic, name and money
                $("#seat_" + j).switchClass("position" + class1, "position" + class2, 1000);
                $("#seat_" + j + "-profile").switchClass("position" + class1 + "-profile", "position" + class2 + "-profile", 1000);
                $("#seat_" + j + "-name").switchClass("position" + class1 + "-name", "position" + class2 + "-name", 1000);
                $("#seat_" + j + "-money").switchClass("position" + class1 + "-money", "position" + class2 + "-money", 1000);
            }
            i++;
        }, 1500);

    // if already at bottom position, displays user hexagon
    }else {
           console.log("position is at 5 "+ seat);
       showCurrentUser(seat);
    }

}

// Transitions from bottom position to bigger user hexagon, calls function to display buttons
function showCurrentUser(seat){
    console.log("inside show current user "+seat);
    // sends bottom hexagon to coordinates of user hexagon and fades it out for animation effect
    $("#"+seat).switchClass("position5","position-user");
    $("#"+seat+"-profile").switchClass("position5-profile","position-user-profile");
    $("#"+seat+"-name").switchClass("position5-name","position-user-name");
    $("#"+seat+"-money").switchClass("position5-money","position-user-money");

    $("#current_user_actions")[0].style.visibility = 'visible';
}

// This function shows current user buttons at the bottom
function showUserButtons(){


    $("#current-user-button-1").show().switchClass("position-user-profile","position-user-button-1",500);

    $("#current-user-button-2").show().switchClass("position-user-profile","position-user-button-2",500);

    $("#current-user-button-3").show().switchClass("position-user-profile","position-user-button-3",500);

    $("#current-user-button-4").show().switchClass("position-user-profile","position-user-button-4",500);

    $("#current-user-text1").show().switchClass("position-user-profile","position-user-text1",500);

    $("#current-user-text2").show().switchClass("position-user-profile","position-user-text2",500);

    $("#current-user-text3").show().switchClass("position-user-profile","position-user-text3",500);

    $("#game-slider").switchClass("position-user-profile","position-game-slider",500);
    $("#game-slider").show();

    $("#current-user-number-text3").show().switchClass("position-user-profile","position-user-number-text3",500);

    $("#current-user-text4").show().switchClass("position-user-profile","position-user-text4",500);

    $("#call-amount").show().switchClass("position-user-profile","position-user-call-amount",500);
    $("#countdown_timer").show();

}

// This function hides the current user buttons
function hideUserButtons(){

    $("#current-user-button-1").switchClass("position-user-button-1","position-user-profile",100);
    $("#current-user-button-1").fadeOut(10);

    $("#current-user-button-2").switchClass("position-user-button-2","position-user-profile",100);
    $("#current-user-button-2").fadeOut(10);

    $("#current-user-button-3").switchClass("position-user-button-3","position-user-profile",100);
    $("#current-user-button-3").fadeOut(10);

    $("#current-user-button-4").switchClass("position-user-button-4","position-user-profile",100);
    $("#current-user-button-4").fadeOut(10);

    $("#current-user-text1").switchClass("position-user-text1","position-user-profile",100);
    $("#current-user-text1").fadeOut(10);

    $("#current-user-text2").switchClass("position-user-text2","position-user-profile",100);
    $("#current-user-text2").fadeOut(10);

    $("#current-user-text3").switchClass("position-user-text3","position-user-profile",100);
    $("#current-user-text3").fadeOut(10);

    $("#game-slider").hide();
    $("#game-slider").switchClass("position-game-slider","position-user-profile",100);

    $("#current-user-number-text3").switchClass("position-user-number-text3","position-user-profile",100);
    $("#current-user-number-text3").fadeOut(10);

    $("#current-user-text4").switchClass("position-user-text4","position-user-profile",100);
    $("#current-user-text4").fadeOut(10);

    $("#call-amount").switchClass("position-user-call-amount","position-user-profile",100);
    $("#call-amount").fadeOut(10);
    $("#countdown_timer").hide();

}

function getSliderValue(){
    return money;
}

// This function animates the center image to popup when hint arrives
function animateHint(){

    $("#hint-box").switchClass("hint-box-display","hint-box-animate",500);
    $("#hint-number").switchClass("hint-number-display","hint-number-animate",500);
    $("#hint-text").switchClass("hint-text-display","hint-text-animate",500);

    setTimeout(function () {
        $("#hint-box").switchClass("hint-box-animate","hint-box-display",500);
        $("#hint-number").switchClass("hint-number-animate","hint-number-display",500);
        $("#hint-text").switchClass("hint-text-animate","hint-text-display",500);
    },10);
}

function changeCSS(className, classValue) {
    // we need invisible container to store additional css definitions
    var cssMainContainer = $('#css-modifier-container');
    if (cssMainContainer.length == 0) {
        var cssMainContainer = $('<div id="css-modifier-container"></div>');
        cssMainContainer.hide();
        cssMainContainer.appendTo($('body'));
    }

    // and we need one div for each class
    classContainer = cssMainContainer.find('div[data-class="' + className + '"]');
    if (classContainer.length == 0) {
        classContainer = $('<div data-class="' + className + '"></div>');
        classContainer.appendTo(cssMainContainer);
    }

    // append additional style
    classContainer.html('<style>' + className + ' {' + classValue + '}</style>');
}

//Scrolls to log board base
function updateScroll(){
/*    var element = document.getElementById("log-body");
    element.scrollTop = element.scrollHeight;*/
    var wtf = $('#log-body');
    var height = wtf[0].scrollHeight;
    wtf.scrollTop(height);
    console.log("Inside Update Scroll.");
    $('#log-body').animate({scrollTop: $('#log-body').prop("scrollHeight")}, 500);

}

// This function shows only all in and fold buttons at the bottom
function showAllinButtons(){

    $("#current-user-button-1").show().switchClass("position-user-profile","position-user-button-1",500);
    $("#current-user-button-4").show().switchClass("position-user-profile","position-user-button-2",500);

    $("#current-user-text1").show().switchClass("position-user-profile","position-user-text1",500);
    $("#current-user-text4").show().switchClass("position-user-profile","position-user-text2",500);
    $("#countdown_timer").show();

}

// This function hides the current user buttons
function hideAllinButtons(){

    $("#current-user-button-1").switchClass("position-user-button-1","position-user-profile",100);
    $("#current-user-button-1").fadeOut(10);
    $("#current-user-button-4").switchClass("position-user-button-2","position-user-profile",100);
    $("#current-user-button-4").fadeOut(10);

    $("#current-user-text1").switchClass("position-user-text1","position-user-profile",100);
    $("#current-user-text1").fadeOut(10);
    $("#current-user-text4").switchClass("position-user-text2","position-user-profile",100);
    $("#current-user-text4").fadeOut(10);
    $("#countdown_timer").hide();

}

// This function shows only all in, call and fold buttons at the bottom
function showAllinAndCallButtons(){
    $("#current-user-button-1").show().switchClass("position-user-profile","position-user-button-1",500);
    $("#current-user-button-2").show().switchClass("position-user-profile","position-user-button-2",500);
    $("#current-user-button-4").show().switchClass("position-user-profile","position-user-button-3",500);
    $("#current-user-text1").show().switchClass("position-user-profile","position-user-text1",500);
    $("#current-user-text2").show().switchClass("position-user-profile","position-user-text2",500);
    $("#current-user-text4").show().switchClass("position-user-profile","position-user-text3",500);
    $("#call-amount").show().switchClass("position-user-profile","position-user-call-amount",500);
    $("#countdown_timer").show();

}

// This function hides the current user buttons
function hideAllinAndCallButtons(){

    $("#current-user-button-1").switchClass("position-user-button-1","position-user-profile",100);
    $("#current-user-button-1").fadeOut(10);
    $("#current-user-button-2").switchClass("position-user-button-2","position-user-profile",100);
    $("#current-user-button-2").fadeOut(10);
    $("#current-user-button-4").switchClass("position-user-button-3","position-user-profile",100);
    $("#current-user-button-4").fadeOut(10);

    $("#current-user-text1").switchClass("position-user-text1","position-user-profile",100);
    $("#current-user-text1").fadeOut(10);
    $("#current-user-text2").switchClass("position-user-text2","position-user-profile",100);
    $("#current-user-text2").fadeOut(10);
    $("#current-user-text4").switchClass("position-user-text3","position-user-profile",100);
    $("#current-user-text4").fadeOut(10);
    $("#call-amount").switchClass("position-user-call-amount","position-user-profile",100);
    $("#call-amount").fadeOut(10);
    $("#countdown_timer").hide();

}


function changeView(seat){
    // gets current position class
    var className = $("#"+seat).attr('class');
    // gets position number
    var pos = parseInt(className.toString().slice(8));
    var class1;
    var n = (5 - pos)
    if(n < 0){
        n = n+10;
    }
    // if not at bottom most position, move to bottom
    if(pos !== 5) {
        // switches each hexagon position to the next
        for (var j = 1; j <= 10; j++) {
            class1 = parseInt($("#seat_" + j).attr('class').toString().slice(8));
            // adjusts position class of background hexagon, profile pic, name and money
            $("#seat_" + j).switchClass("position" + class1, "position" + ((class1 + n)%10),0);
            $("#seat_" + j + "-profile").switchClass("position" + class1 + "-profile", "position" + ((class1 + n)%10) + "-profile",0);
            $("#seat_" + j + "-name").switchClass("position" + class1 + "-name", "position" + ((class1 + n)%10) + "-name",0);
            $("#seat_" + j + "-money").switchClass("position" + class1 + "-money", "position" + ((class1 + n)%10) + "-money",0);
            }
    }
    //displays user hexagon
    $("#"+seat).switchClass("position5","position-user");
    $("#"+seat+"-profile").switchClass("position5-profile","position-user-profile");
    $("#"+seat+"-name").switchClass("position5-name","position-user-name");
    $("#"+seat+"-money").switchClass("position5-money","position-user-money");
    $("#current_user_actions")[0].style.visibility = 'visible';

//    showCurrentUser(seat);
}