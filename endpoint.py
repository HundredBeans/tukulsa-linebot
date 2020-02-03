import requests
import json

base_url = 'https://tukulsa-new-test.herokuapp.com/'


def get_chat_info(line_id):
    json_data = {
        'line_id': line_id
    }
    url = base_url + 'users/chat'
    headers = {'content-type' : 'application/json'}

    data = requests.get(url, json = json_data, headers = headers).text
    parsed = json.loads(data)
    return parsed

def update_number(line_id, number, number_status):
    json_data = {
        'line_id': line_id,
        'phone_number': number,
        'status_number': number_status
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

def update_all(line_id, number, nominal, number_status, nominal_status):
    json_data = {
        'line_id': line_id,
        'phone_number': number,
        'nominal': nominal,
        'status_nominal': nominal_status,
        'status_number': number_status
    }
    url = base_url + 'users/chat'
    headers = {'content-type' : 'application/json'}

    data = requests.put(url, json = json_data, headers = headers).text
    parsed = json.loads(data)
    return parsed

print(update_number("daffa", "08159898344", True))
print(get_chat_info("daffa")['phone_number'])