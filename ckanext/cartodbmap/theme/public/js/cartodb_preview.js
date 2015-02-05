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
	
	  self.el.append($('<div style="position:absolute;bottom:1px;left:70px;z-index:999">'
						+ '<a id="go_to_cartodb_vis" target="_blank" href="' + options.cartodbVisUrl.replace('api/v2/','').replace('/viz.json','/map') + '" class="btn btn-link">'
						+	'Edit'
						+ '</a></div>'))
	
      self.el.append($('<div style="position:absolute;bottom:9px;left:115px;z-index:999">'
						+ ' <a id="get_the_data" href="' + options.resourceUrl + '" target="_blank">'
						+ '<img height=10 style="vertical-align:-24px;" src="https://raw.githubusercontent.com/betanyc/getDataButton/master/png/80x15.png">'
						+ '</img></a>'
						+ '</div>'))
	
      }
}
});
