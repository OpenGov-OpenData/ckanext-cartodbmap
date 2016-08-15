=============
ckanext-cartodbmap (CKAN CartoDB ResourceView)
=============

Use CartoDB as a more powerful/performant way to visualize geospatial data in CKAN.  And not just visualize, but actually start telling stories as well with round-tripping support with CartoDB editor.

---------------
Config Settings
---------------
Add following in config settings::

    ckanext.cartodbmap.cartodb.username = <CartoDB Username Here> 
    ckanext.cartodbmap.cartodb.key = <API Key here> 


The following can also be optionally added::

Set a limit for DataStore resources. Resources with a row count higher than the limit will not have a view created, the default value is 100000::

    ckanext.cartodbmap.datastore.limit = 100000


Remove geojson_preview from ckan.plugins list

Disable current default geojson view (removes geojson from the list)::
		
	ckan.preview.json_formats = json gjson



------------------------
Development Installation
------------------------

To install ckanext-cartodbmap for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/Ontodia/ckanext-cartodbmap.git
    cd ckanext-cartodbmap
    python setup.py develop
    pip install -r dev-requirements.txt
