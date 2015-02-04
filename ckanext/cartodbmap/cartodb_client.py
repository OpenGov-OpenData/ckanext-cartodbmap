import urllib
import json
import pprint
import requests, json
import slugify
import os
import time

import ckan.lib.helpers as h

#### CARTODB SETTINGS ####
username = h.config.get('ckanext.cartodbmap.cartodb.username')
api_key = h.config.get('ckanext.cartodbmap.cartodb.key')
cartodb_url = 'https://'+ username +'.cartodb.com'

def upload_url_resource(resource_url):
    resource_dict = {
        "api_key" : api_key,
        "url": resource_url
    }
    endpoint = cartodb_url + '/api/v1/imports';
    
    r = requests.post(endpoint
                        ,data=resource_dict
                        ,headers={
                            "Content-Type" : "application/x-www-form-urlencoded"
                        }
                    )
    return r

def get_import_queue(item_queue_id):
    resource_dict = {
        "api_key" : api_key
    }
    endpoint = cartodb_url + '/api/v1/imports/'+item_queue_id;
    
    r = requests.get(endpoint
                        ,data=resource_dict
                        ,headers={
                            "Content-Type" : "application/x-www-form-urlencoded"
                        }
                    )
    return r

def get_table_details(table_name):
    resource_dict = {
        "api_key" : api_key
    }
    endpoint = cartodb_url + '/api/v1/tables/'+table_name;   
    r = requests.get(endpoint
                        ,data=resource_dict
                        ,headers={
                            "Content-Type" : "application/x-www-form-urlencoded"
                        }
                    )
    return r

def create_visualization_from_table(table_vis_id, vis_name):
    resource_dict = {
        "source_visualization_id" : table_vis_id,
        "api_key" : api_key,
        "name" : vis_name
    }
    resource_dict = json.dumps(resource_dict)
    endpoint = cartodb_url + '/api/v1/viz';
    
    r = requests.post(endpoint
                        ,data=resource_dict
                        ,headers={
                            "Content-Type" : "application/json"
                        }
                    )
    return r 




def create_cartodb_resource_view(resource_url):
    r = upload_url_resource(resource_url)
    item_queue_id = r.json().get("item_queue_id")
    if(item_queue_id):
        state = ""
        while(state != 'complete' and  state != 'failure'):
            r = get_import_queue(item_queue_id)
            state = r.json().get("state")
            time.sleep(.5)
        table_name =  r.json().get("table_name")
        if(table_name):
            print "**** " + item_queue_id
            r = get_table_details(table_name)
            table_vis_id = r.json().get("table_visualization",{}).get("id")
            r = create_visualization_from_table(table_vis_id, table_name + " CKAN")
            vis_id = r.json().get('id')
            if(vis_id):
                print "**** " + vis_id
                return "http://pediacities.cartodb.com/api/v2/viz/" + vis_id + "/viz.json" 
    return
    
    