import requests
import json

base_url = 'https://tukulsa-new-test.herokuapp.com/'

def post_user(line_id, display_name):
    json_data = {
        'line_id': line_id,
        'display_name': display_name
    }
    url = base_url + 'users'
    headers = {'content-type' : 'application/json'}

    data = requests.post(url, json = json_data, headers = headers).text
    parsed = json.loads(data)
    return parsed

def get_chat_info(line_id):
    json_data = {
        'line_id': line_id
    }
    url = base_url + 'users/chat'
    headers = {'content-type' : 'application/json'}

    data = requests.get(url, json = json_data, headers = headers).text
    parsed = json.loads(data)
    return parsed

def update_number(line_id, number, number_status, operator):
    json_data = {
        'line_id': line_id,
        'phone_number': number,
        'status_number': number_status,
        'operator': operator
    }
    url = base_url + 'users/chat'
    headers = {'content-type' : 'application/json'}

    data = requests.put(url, json = json_data, headers = headers).text
    parsed = json.loads(data)
    return parsed

def update_nominal(line_id, nominal, nominal_status):
    json_data = {
        'line_id': line_id,
        'nominal': nominal,
        'status_nominal': nominal_status
    }
    url = base_url + 'users/chat'
    headers = {'content-type' : 'application/json'}

    data = requests.put(url, json = json_data, headers = headers).text
    parsed = json.loads(data)
    return parsed

def update_all(line_id, number, nominal, number_status, nominal_status, operator):
    json_data = {
        'line_id': line_id,
        'phone_number': number,
        'nominal': nominal,
        'status_nominal': nominal_status,
        'status_number': number_status,
        'operator': operator
    }
    url = base_url + 'users/chat'
    headers = {'content-type' : 'application/json'}

    data = requests.put(url, json = json_data, headers = headers).text
    parsed = json.loads(data)
    return parsed
