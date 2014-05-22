(function($, _) {
    "use strict";

    if (typeof window.console == "undefined" || typeof window.console.log == "undefined"){
        var console = {log: function(){}};
    } else {
        var console = window.console;
    }
    console.log("js loaded");

    var template = $("#twit_box_template").html();
    var container = $("#twit_box");

    var lon;
    var lat;
    var web_sock = null;

    function message(msg, data){
        console.log(msg);
        if (data !== undefined){
            console.debug(data);
        }
    }

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
        $.getJSON("search/lonlat/"+lon+"+"+lat, function(data){
            callback(data);
            console.log("got tweets")
        });
        if (forever){
            console.log(get_tweets);
            _.delay(get_tweets, 10000, callback, forever);
        }
    };

    function main(stress) {
        console.log([lon, lat]);
        new_map(lon, lat);
        get_tweets(render_all);
        if (web_sock !== null){
            web_sock.close();
        }
        var ws_url = "ws://"+window.location.hostname+":8001/"+lon+";"+lat;
        console.log(ws_url);
        web_sock = new WebSocket(ws_url);
        web_sock.onmessage = function(evt) {
            var tweet = $(_.template(template, $.parseJSON(evt.data)))
            tweet.hide().prependTo(container).fadeIn();
            $(".tweet", container).slice(30).remove();
            $("#quiet").remove();
        };
    };

    function with_position(position){
        console.log("with_position")
        lon = position.coords.longitude;
        lat = position.coords.latitude;
        main(lon, lat);
    };

    function manual_position(){
        console.log("manual_position")
        lon = parseFloat($("#m_lon").val());
        lat = parseFloat($("#m_lat").val());
        main(lon, lat);
    };

    function fragment_position(){
        var pos = window.location.hash.slice(1).split(';');
        lat = parseFloat(pos[1]);
        lon = parseFloat(pos[0]);
        main(lon, lat);
    }

    function get_location() {
        if (window.location.hash !== "") {
            fragment_position();
        }
        else if ("geolocation" in navigator) {
            console.log("geolocation supported");
            var error_cb = _.partial(message, "geolocation error");
            navigator.geolocation.getCurrentPosition(with_position, error_cb);
        }
        else{
            console.log("geolocation is not supported");
        }
    };

    function new_map(lon, lat){
        $("#map").html("").height("320px");
        var map = new OpenLayers.Map(
            "map", { controls:[new OpenLayers.Control.Navigation(),
                               new OpenLayers.Control.PanZoomBar(),],
                     numZoomLevels: 18,
	           });
        var layer = new OpenLayers.Layer.OSM("Simple OSM Map");
        var markers = new OpenLayers.Layer.Markers("Markers");
        var icon = new OpenLayers.Icon(
            'OpenLayers-2.13.1/img/marker.png',
            OpenLayers.Size(25, 25));
        map.addLayer(layer);
        map.addLayer(markers);
        var center = new OpenLayers.LonLat(lon, lat).transform(
            new OpenLayers.Projection("EPSG:4326"),
            map.getProjectionObject());
        console.log(center);
        map.setCenter(center, 15);
        var marker = new OpenLayers.Marker(center, icon);
        markers.addMarker(marker);
        return map;
    };

    $(".toggle_map .show_map").click(function(){
        $("#map_container").slideDown();
        $(".toggle_map .hide_map").removeClass("hidden")
        $(".toggle_map .show_map").addClass("hidden")
    });
    $(".toggle_map .hide_map").click(function(){
        $("#map_container").slideUp();
        $(".toggle_map .show_map").removeClass("hidden")
        $(".toggle_map .hide_map").addClass("hidden")
    });

    get_location();
    window.get_location = get_location;
    $("#m_butt").click(manual_position);
    $("a.location").click(fragment_position);


}(jQuery, _));
