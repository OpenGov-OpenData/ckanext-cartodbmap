import urllib
import json
import pprint
import requests, json
import os
import time

import ckan.lib.helpers as h
import ckan.plugins as plugins

#### CARTODB SETTINGS ####


class CartoDBClient:
    def __init__(self,
                    username=h.config.get('ckanext.cartodbmap.cartodb.username'),
                    api_key=h.config.get('ckanext.cartodbmap.cartodb.key')):
        self.username = username
        self.api_key = api_key
            
        self.cartodb_url = 'https://'+ self.username +'.cartodb.com'
        


    # Private Methods
    def __upload_url_resource(self,resource_url):
        resource_dict = {
            "api_key" : self.api_key,
            "url": resource_url
        }
        endpoint = self.cartodb_url + '/api/v1/imports';
        r = requests.post(endpoint
                        ,data=resource_dict
                        ,headers={
                            "Content-Type" : "application/x-www-form-urlencoded"
                        }
                    )
        return r

    def __get_import_queue(self,item_queue_id):
        resource_dict = {
            "api_key" : self.api_key
        }
        endpoint = self.cartodb_url + '/api/v1/imports/'+item_queue_id;
        
        r = requests.get(endpoint
                        ,data=resource_dict
                        ,headers={
                            "Content-Type" : "application/x-www-form-urlencoded"
                        }
                    )
        return r

    def __get_table_details(self,table_name):
        resource_dict = {
            "api_key" : self.api_key
        }
        endpoint = self.cartodb_url + '/api/v1/tables/'+table_name;   
        r = requests.get(endpoint
                        ,data=resource_dict
                        ,headers={
                            "Content-Type" : "application/x-www-form-urlencoded"
                        }
                    )
        return r

    def __create_visualization_from_table(self,table_vis_id, vis_name):
        resource_dict = {
            "source_visualization_id" : table_vis_id,
            "api_key" : self.api_key,
            "name" : vis_name
        }
        resource_dict = json.dumps(resource_dict)
        endpoint = self.cartodb_url + '/api/v1/viz';
    
        r = requests.post(endpoint
                        ,data=resource_dict
                        ,headers={
                            "Content-Type" : "application/json"
                        }
                    )
        return r 

    
    # Public Methods
    def create_cartodb_resource_view(self,resource_url):
        reason = "Check your API Parameters"
        try:
            r = self.__upload_url_resource(resource_url)
            item_queue_id = r.json().get("item_queue_id")
            if(item_queue_id):
                state = ""
                while(state != 'complete' and  state != 'failure'):
                    r = self.__get_import_queue(item_queue_id)
                    state = r.json().get("state")
                    time.sleep(.5)
                table_name =  r.json().get("table_name")
                if(table_name):
                    print "**** " + item_queue_id
                    r = self.__get_table_details(table_name)
                    table_vis_id = r.json().get("table_visualization",{}).get("id")
                    r = self.__create_visualization_from_table(table_vis_id, table_name + " CKAN")
                    vis_id = r.json().get('id')
                    if(vis_id):
                        print "**** " + vis_id
                        return self.cartodb_url+ "/api/v2/viz/" + vis_id + "/viz.json"
                    else:
                        reason = "Failed Creating Visualization"
                else:
                    reason = "Failed Creating Table. Make sure your package is public."
            else:
                reason = "Failed Importing Data"
            message = plugins.toolkit._('Unable to create visualization - ' + reason)
            raise plugins.toolkit.Invalid(message)
        except:
            message = plugins.toolkit._('Unable to create visualization - ' + reason)
            raise plugins.toolkit.Invalid(message)
            
            
    