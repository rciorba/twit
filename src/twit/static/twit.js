(function($, _) {
    "use strict";

    if (typeof window.console == "undefined" || typeof window.console.log == "undefined"){
        var console = {log: function(){}};
    } else {
        var console = window.console;
    }

    var template = $("#twit_box_template").html();
    var container = $("#twit_box");

    function render_all(data){
	var rendered = "";
	_.each(data.tweets, function(tweet){
	    rendered = rendered+_.template(template, tweet);
	});
    	$("#twit_box").html(rendered);
    };

    function get_tweets(callback, forever){
	$.getJSON("/search/lonlat/-2.28+53.46", function(data){
	    callback(data);
	});
	if (forever){
	    console.log(get_tweets);
	    _.delay(get_tweets, 10000, callback, forever);
	}
    };

    get_tweets(render_all);

    var web_sock = new WebSocket("ws://localhost:8001/-2.28;53.46;.3");
    web_sock.onmessage = function(evt) {
	var tweet = $(_.template(template, $.parseJSON(evt.data)))
    	tweet.hide().prependTo(container).fadeIn();
	$(".tweet", container).slice(30).remove();
    };

}(jQuery, _));
