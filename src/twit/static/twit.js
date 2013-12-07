(function($, _, console) {
    "use strict";
    console.log("spam");

    function render(data){
	var template = $("#twit_box_template").html();
	var rendered = _.template(template, data);
	console.log(rendered);
	$("#twit_box").html(rendered);
    };

    function get_tweets(callback){
	$.getJSON("/search/lonlat/-2.28+53.46", function(data){
	    // $.each(data.tweets, function(index, tweet){
	    // 	console.log(tweet);
	    // });
	    callback(data);
	});
    };

    get_tweets(render);
}(jQuery, _, console));
