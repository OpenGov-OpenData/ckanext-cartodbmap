// Spinner
var spinner_opts = {
  lines: 13, // The number of lines to draw
  length: 0, // The length of each line
  width: 13, // The line thickness
  radius: 38, // The radius of the inner circle
  corners: 1, // Corner roundness (0..1)
  rotate: 30, // The rotation offset
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: $('#use_your_own_cartodb').css('color'), // #rgb or #rrggbb or array of colors
  speed: 1, // Rounds per second
  trail: 66, // Afterglow percentage
  shadow: false, // Whether to render a shadow
  hwaccel: false, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
};

$("button[name='save'],button[name='preview'],button[name='delete']").click(function () {
	$("#loading").fadeIn('100');
	var spinnerTarget = document.getElementById('loading-spinner'),
	spinner = new Spinner(spinner_opts).spin(spinnerTarget);
});


$("input[name='cartodb_vis_url']").blur(function() {
	if(!$(this).val()) {
		$("input[name='cartodb_account']").prop('disabled', false);
		$("input[name='cartodb_key']").prop('disabled', false);
	}
	else {
		$("input[name='cartodb_account']").prop('disabled', true);
		$("input[name='cartodb_account']").val('')
		$("input[name='cartodb_key']").prop('disabled', true);
		$("input[name='cartodb_key']").val('')
	}
})

// Spinner End


/*
var marker_style = {
	radius:5,
	stroke:true,
	weight:1.7,
	opacity:1,
	color:"black",
	fill:true,
	fillColor:"#b2a1b3",
	fillOpacity:1,
	clickable:false,
}
*/
var marker_style = L.icon({
	iconUrl: 'fanstatic/cartodbmap/vendor/cartodb/img/location_pin.png',
    iconSize: [24,34],
	iconAnchor: [12,32]
});
var locate_zoom_level = 13;
var marker;


// cartodb preview module
ckan.module('cartodb_preview', function (jQuery, _) {
  return {
    initialize: function () {
      var self = this;
	  self.el.empty();
      var map_elem = self.el.append($("<div></div>").attr("id","map"));
      options = self.options,
      
      cartodb.createVis('map', options.cartodbVisUrl.replace(/https?:/,""))
    		.on('done', function(vis,layers) {
    			    var map_attr = map_elem.append($("<div></div>").attr("id","cartodb-map-attribution"));
      				map_attr.append($("<a href='" + options.cartodbVisUrl+"' target='_blank>Go to this visualization</a>"))
      				$(self.el).find('#map').find('.cartodb-tiles-loader').before('<div class="opendatacity-locate" style="display: block;"><a></a></div>')
      				
      				map = vis.getNativeMap();
      				function detectUserLocation(){
	 					if (navigator.geolocation) {
	  						var timeoutVal = 10 * 1000 * 1000;
	   						navigator.geolocation.getCurrentPosition(function(position) {
	   								//mapToPosition(position);
	   								
	 								lon = position.coords.longitude;
	 								lat = position.coords.latitude;
	   								map.setView(new L.LatLng(lat,lon), locate_zoom_level);
	   								if(marker){
	 									marker.setLatLng([lat,lon]);
	 								}
	 								else {
	 									marker = new L.marker([lat,lon], { icon: marker_style });
	 									marker.addTo(map);
	 								}
	     						}, 	
								alertError,
								{ enableHighAccuracy: true, timeout: timeoutVal, maximumAge: 0 }
	   						);
	 					}
	 					else {
	  						alert("Geolocation is not supported by this browser");
	 					}
	 
					 	function alertError(error) {
	   						var errors = { 
	     						1: 'Permission denied',
	     						2: 'Position unavailable',
	     						3: 'Request timeout'
	   						};
	   						alert("Error: " + errors[error.code]);
	 					}
					}		
					
      				$('.opendatacity-locate').click(function() {
	  					detectUserLocation();
	  				})
	    	}).on('error', function() {
    	  		//log the error
    		});
	  self.el.append($('<div style="position:absolute;bottom:8px;left:86px;z-index:999">'
						+ ' <a id="get_the_data" href="http://www.opendata.city" target="_blank">'
						+ '<img height=10 style="vertical-align:-24px;" src="//catalog.opendata.city/base/images/opendatacity_icon_sm.png">'
						+ '</img></a>'
						+ '</div>'))
	  
	  var button_box_html = '<div class="map-button-div" style="left:147px;">'
	  					+ '&nbsp;'
	  
	  
	  // Add Data button	
	  button_box_html	+= '<a id="go_to_data" target="_blank" href="' + options.resourceUrl.split('/download/')[0] + '" class="btn btn-link map-button">'
						+	'Data'
						+ '</a> '
	  
	  // Add Edit button
	  button_box_html	+= '| <a id="go_to_cartodb_vis" target="_blank" href="' + options.cartodbVisUrl.replace('api/v2/','').replace('/viz.json','/map') + '" class="btn btn-link map-button">'
						+	'Edit'
						+ '</a> '
	  // Add Talk button				
	  if(options.discourseUrl && options.discourseUrl != 'None') {
			button_box_html += '| <a id="go_to_discourse" target="_blank" href="' + options.discourseUrl + '" class="btn btn-link map-button">'
							+	'Talk'
							+ '</a>'
	  }
	  button_box_html += '&nbsp;</div>'
	  self.el.append($(button_box_html))	
	  //if ( window.location === window.parent.location ) {
	  		  map_elem.height(map_elem.parent().parent().parent().height())
  	  //}	
	  
    }
}
});
