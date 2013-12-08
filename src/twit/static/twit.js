(function($, _) {
    "use strict";

    if (typeof window.console == "undefined" || typeof window.console.log == "undefined"){
        var console = {log: function(){}};
    } else {
        var console = window.console;
    }

    function render(data){
	var template = $("#twit_box_template").html();
	var rendered = _.template(template, data);
	$("#twit_box").html(rendered);
    };

    function get_tweets(callback, forever){
	console.log("getting tweets");
	$.getJSON("/search/lonlat/-2.28+53.46", function(data){
	    // $.each(data.tweets, function(index, tweet){
	    // 	log(tweet);
	    // });
	    callback(data);
	});
	if (forever){
	    console.log(get_tweets);
	    _.delay(get_tweets, 10000, callback, forever);
	}
    };

    get_tweets(render, true);
}(jQuery, _));
