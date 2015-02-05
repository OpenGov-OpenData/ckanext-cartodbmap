import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import cartodb_client
import ckan.lib.helpers as h

ignore_missing = plugins.toolkit.get_validator('ignore_missing')

CARTODB_FORMATS = ['csv','tsv','kml','kmz','xls', 'xlsx', 'geojson', 'gpx', 'osm', 'bz2', 'ods', 'zip']

# Create New Cartodb Client
cc = cartodb_client.CartoDBClient()

def set_cartodb_account(username):
    if not username:
        username = h.config.get('ckanext.cartodbmap.cartodb.username')
    cc.username = username
    cc.cartodb_url = 'https://'+ cc.username +'.cartodb.com'
    return
      
def set_cartodb_key(key):
    if not key:
        key = h.config.get('ckanext.cartodbmap.cartodb.key')
    cc.api_key = key
    return

def vis_from_resource(url,context):
    # Create new CartoDB Vis is url field is empty
    if not url:
        # Get resource url
        resource_id = plugins.toolkit.c.__getattr__("resource_id")
        resource = toolkit.get_action('resource_show')(context,{'id': resource_id})
        resource_url = resource["url"]
        resoruce_format_lower = resource["format"].lower()
        print "***** " + resource_url
        
        # Check if CartoDB accepts current file format
        if not (resoruce_format_lower in CARTODB_FORMATS):
            message = plugins.toolkit._('Unsupported CartoDB file format: ' + resoruce_format_lower)
            raise plugins.toolkit.Invalid(message)
        return cc.create_cartodb_resource_view(resource_url)
    return url

class CartodbmapPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)
  
    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'theme/templates')
        toolkit.add_resource('theme/public', 'cartodbmap')
        
    # IResourceView
    def info(self):
        schema  ={
            'cartodb_account': [ignore_missing,set_cartodb_account],
            'cartodb_key'    : [ignore_missing,set_cartodb_key],
            'cartodb_vis_url': [ignore_missing,vis_from_resource],    
        }

        return {'name': 'cartodb-map',
                'title': 'CartoDB Map',
                'icon': 'map-marker',
                'schema': schema,
                'iframed': False}
    
    def can_view(self, data_dict):
        return True
    
    def setup_template_variables(self, context, data_dict):
        resource = data_dict['resource']
        resource_view = data_dict['resource_view']
        resource_url = data_dict['resource']['url']
        return {'resource': resource,
                'resource_view': resource_view,
                }
    
    def view_template(self, context, data_dict):
        return 'cartodbmap_view.html'

    def form_template(self, context, data_dict):
        return 'cartodbmap_form.html'
    