import urllib
import json
import pprint
import requests, json
import os
import time

import ckan.lib.helpers as h

#### CARTODB SETTINGS ####


def url_exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

class CartoDBClient:
    def __init__(self, username="", api_key=""):
        self.username = username
        self.api_key = api_key
        
        self.cartodb_url = 'https://'+ self.username +'.carto.com'
        
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
        cartodb_obj = {
            'success' : None,
            'request' : {
                'resource_url' : resource_url,
                'cartodb_base' : self.cartodb_url,
                'username' : self.username,
                'api_key' : self.api_key
            },
            'response' : {
                'item_queue_id' : None,
                'table_name' : None,
                'table_vis_id' : None,
                'vis_id' : None,
                'cartodb_vis_url' : None,
            },
            'messages' : {
                'user_message' : "Check your API Parameters.",
                'error_message' : None              
            }
        }
        
        
        if not url_exists(resource_url):
            cartodb_obj['success'] = False
            cartodb_obj['messages']['error_message'] = "URL doesn't exist: \'" + resource_url + "\'"
            cartodb_obj['messages']['user_message'] = "URL doesn't exist: \'" + resource_url + "\'"
            return cartodb_obj
        
        r = {'text': 'Uninitialized'}
        try:
            r = self.__upload_url_resource(resource_url)
            cartodb_obj['response']['item_queue_id'] = r.json().get('item_queue_id')
            if(cartodb_obj['response']['item_queue_id']):
                state = ""
                while(state != 'complete' and  state != 'failure'):
                    r = self.__get_import_queue(cartodb_obj['response']['item_queue_id'])
                    state = r.json().get("state")
                    time.sleep(.5)
                cartodb_obj['response']["table_name"] =  r.json().get("table_name")
                if(cartodb_obj['response']["table_name"]):
                    r = self.__get_table_details(cartodb_obj['response']["table_name"] )
                    cartodb_obj['response']["table_vis_id"] = r.json().get("table_visualization",{}).get("id")
                    r = self.__create_visualization_from_table(cartodb_obj['response']["table_vis_id"], cartodb_obj['response']["table_name"] + " - Created by Carto CKAN Extension")
                    cartodb_obj['response']["vis_id"] = r.json().get('id')
                    if(cartodb_obj['response']["vis_id"]):
                        cartodb_obj['response']["cartodb_vis_url"] = self.cartodb_url+ "/api/v2/viz/" + cartodb_obj['response']["vis_id"] + "/viz.json"
                        cartodb_obj['success'] = True
                        return cartodb_obj
                    else:
                        cartodb_obj['messages']['user_message'] = "Failed Creating Visualization."
                else:
                    cartodb_obj['messages']['user_message'] = "Failed Creating Table."
            else:
                cartodb_obj['messages']['user_message'] = "Failed Importing Data."             
        except:
            # Dummy exception Handling
            cartodb_obj['messages']['user_message'] = "Check your API Parameters."
            
        cartodb_obj['success'] = False
        cartodb_obj['messages']['error_message'] = r.json()
        return cartodb_obj
