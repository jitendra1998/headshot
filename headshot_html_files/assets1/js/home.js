jQuery(document).ready(function(event){
	// jQuery(".y_video").css("width","100%");
	// jQuery(".y_video").css("height","100%");
	offset_correction=300;
	is_scrolling=false;
	jQuery(".site_menu_item a").on('click',function(event){
		is_scrolling=true;
		event.preventDefault();
		id=jQuery(this).attr("href");
		offset=jQuery(id).offset();
		jQuery("html").animate({scrollTop:offset.top-offset_correction},1000,"swing",function(){
			is_scrolling=false;
		});
	});
	references=jQuery(".site_menu_item a");
	jQuery(references[0]).focus();
	jQuery(window).scroll(function(){
		if(!is_scrolling){
			for(i=0; i<references.length; i++){
				id=jQuery(references[i]).attr("href");
				if(jQuery(id).length){
					offset=jQuery(id).offset();
					if((offset.top-offset_correction+1<jQuery(this).scrollTop())&&(!jQuery(references[i]).is(":focus"))){
						jQuery(references[i]).focus();
					}}
			}
		}
	});
});
function saveMesssage(){
	jQuery.ajax({
		type:"POST",
		url:"http://52.163.123.180:9080/saveMesssage/",
		data:jQuery('.contact_us_form').serialize(),
		success:function(response){
			jQuery('.contact_us_form .success').css("display","block");
		},
		error:function(xhr,status,error){
			console.log(status);
			console.log(error);
		}
	});
}

var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
	player = new YT.Player('player', {
		height: '390',
		width: '640',
		videoId: 'NP4pFRhalf4',
		events: {
			'onReady': onPlayerReady,
			'onStateChange': onPlayerStateChange
		}
	});
}

function onPlayerReady(event) {
	// event.target.playVideo();
}

function onPlayerStateChange(event) {
	if (event.data == YT.PlayerState.PLAYING) {
		jQuery('#cquiz_carousel').carousel('pause');
	} else {
		jQuery('#cquiz_carousel').carousel('cycle');
	}
}
function stopVideo() {
	player.stopVideo();
}