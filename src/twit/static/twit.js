(function($, _) {
    "use strict";

    if (typeof window.console == "undefined" || typeof window.console.log == "undefined"){
        var console = {log: function(){}};
    } else {
        var console = window.console;
    }

    var template = $("#twit_box_template").html();
    var container = $("#twit_box");

    var lon;
    var lat;
    var web_sock = null;

    function render_all(data){
        var rendered = "";
        _.each(data.tweets, function(tweet){
            rendered = rendered+_.template(template, tweet);
        });
        if (data.tweets.length == 0){
            rendered = "<ul id='quiet'>People in your area are unusually quiet!</ul>";
        }
        $("#twit_box").html(rendered);
    };

    function get_tweets(callback, forever){
        console.log(lon);
        $.getJSON("/search/lonlat/"+lon+"+"+lat, function(data){
            callback(data);
        });
        if (forever){
            console.log(get_tweets);
            _.delay(get_tweets, 10000, callback, forever);
        }
    };

    function get_location() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(with_position);
        }
        console.log("geolocation is not supported");
    }

    function main() {
        console.log([lon, lat]);
        get_tweets(render_all);
        if (web_sock !== null){
            web_sock.close();
        }
        web_sock = new WebSocket("ws://"+window.location.hostname+":8001/"+lon+";"+lat+";.3");
        web_sock.onmessage = function(evt) {
            var tweet = $(_.template(template, $.parseJSON(evt.data)))
            tweet.hide().prependTo(container).fadeIn();
            $(".tweet", container).slice(30).remove();
            $("#quiet").remove();
        };
    };

    function with_position(position){
        lon = position.coords.longitude;
        lat = position.coords.latitude;
        main(lon, lat);
    }

    function manual_position(){
        lon = parseFloat($("#m_lon").val());
        lat = parseFloat($("#m_lat").val());
        main(lon, lat);
    }


    // get_tweets(render_all);
    get_location();
    $("#m_butt").click(manual_position);


}(jQuery, _));
