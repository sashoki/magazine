$(document).ready(function() {
    $("body").css("background", "#DEDEDE");
    $("footer, .top-bar, .top-bar ul").css("background", "#DEDEDE");
    $(".callout").css("background", "#2BBB23");

    $(".thumb").attr("src", "/static/images/pythonfon.jpeg");


});

$(document).ready(function() {

    $("#menu").click(function(){ $("#list").slideToggle(1000)});
    $("#menu").mouseout(function(){ $("#menu").css("background-color", "#DEDEDE")});
    $("#menu").mouseover(function(){ $("#menu").css("background-color", "#777777")});


    $("#menu1").click(function(){ $("#list1").slideToggle(1000)});
    $("#menu1").mouseover(function(){ $("#menu1").css("background-color", "#DEDEDE")});
    $("#menu1").mouseout(function(){ $("#menu1").css("background-color", "#777777")});

});




