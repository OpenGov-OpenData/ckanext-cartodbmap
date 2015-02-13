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

// cartodb preview module
ckan.module('cartodb_preview', function (jQuery, _) {
  return {
    initialize: function () {
      var self = this;
	  self.el.empty();
      var map_elem = self.el.append($("<div></div>").attr("id","map"));
      options = self.options,
      
      cartodb.createVis('map', options.cartodbVisUrl)
    		.on('done', function(vis,layers) {
    			    var map_attr = map_elem.append($("<div></div>").attr("id","cartodb-map-attribution"));
      				map_attr.append($("<a href='" + options.cartodbVisUrl +"' target='_blank>Go to this visualization</a>"))
	    	}).on('error', function() {
    	  		//log the error
    		});
	  self.el.append($('<div style="position:absolute;bottom:8px;left:80px;z-index:999">'
						+ ' <a id="get_the_data" href="http://www.opendata.city" target="_blank">'
						+ '<img height=10 style="vertical-align:-24px;" src="http://catalog.opendata.city/base/images/opendatacity_icon_sm.png">'
						+ '</img></a>'
						+ '</div>'))
	  
	  self.el.append($('<div style="position:absolute;bottom:1px;left:144px;z-index:999;">'
						+ '<a id="go_to_cartodb_vis" target="_blank" href="' + options.resourceUrl.split('/download/')[0] + '" class="btn btn-defualt map-button">'
						+	'Data'
						+ '</a></div>'))
	  
	  self.el.append($('<div style="position:absolute;bottom:1px;left:187px;z-index:999;">'
						+ '<a id="go_to_cartodb_vis" target="_blank" href="' + options.cartodbVisUrl.replace('api/v2/','').replace('/viz.json','/map') + '" class="btn btn-defualt map-button">'
						+	'Edit'
						+ '</a></div>'))
					
	  
	  
      }
}
});
