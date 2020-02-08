import requests
import json
import os

base_url = os.getenv('BASE_URL', None)

def post_user(line_id, display_name):
    """
    Post User's LINE info into TUKULSA database
    
    Parameters
    ---------
        line_id : User's LINE ID as a string.
        display_name : User's LINE Display Name as a string.

    Return
    ------
        parsed response from TUKULSA Backend
    """
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
    """
    GET User's LINE Chat info from TUKULSA Database
    
    Parameters
    ---------
        line_id : User's LINE ID as a string.

    Return
    ------
        parsed response from TUKULSA Backend
    """
    json_data = {
        'line_id': line_id
    }
    url = base_url + 'users/chat'
    headers = {'content-type' : 'application/json'}

    data = requests.get(url, json = json_data, headers = headers).text
    parsed = json.loads(data)
    return parsed

def update_number(line_id, number, number_status, operator):
    """
    UPDATE User's LINE Chat info into TUKULSA backend / database
    
    Parameters
    ---------
        line_id : User's LINE ID as a string.
        number : User's Phone Number based on LINE Chat as a string.
        number_status : User's Phone Number Status based on LINE Chat as a boolean.
        operator : User's provider based on Phone Number as a string.

    Return
    ------
        parsed response from TUKULSA Backend
    """
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
    """
    UPDATE User's LINE Chat info into TUKULSA backend / database
    
    Parameters
    ---------
        line_id : User's LINE ID as a string.
        nominal : User's asked nominal based on LINE Chat as a string.
        nominal_status : User's asked nominal status based on LINE Chat as a boolean.

    Return
    ------
        parsed response from TUKULSA Backend
    """
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
    """
    UPDATE User's LINE Chat info into TUKULSA backend / database
    
    Parameters
    ---------
        line_id : User's LINE ID as a string.
        number : User's Phone Number based on LINE Chat as a string.
        nominal : User's asked nominal based on LINE Chat as a string.
        number_status : User's Phone Number Status based on LINE Chat as a boolean.
        nominal_status : User's asked nominal status based on LINE Chat as a boolean.
        operator : User's provider based on Phone Number as a string

    Return
    ------
        parsed response from TUKULSA Backend
    """
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

def get_product_by(operator):
    """
    GET Product with filter by specific provider / operator
    
    Parameters
    ---------
        operator : User's Selected operator / provider as string

    Return
    ------
        parsed response from TUKULSA Backend
    """
    json_data = {
        'operator' : operator   
    }
    url = base_url + 'users/product/filterby'
    headers = {'content-type' : 'application/json'}

    data = requests.post(url, json = json_data, headers = headers).text
    parsed = json.loads(data)
    return parsed

def get_midtrans_url(line_id, number, product_code):
    """
    GET midtrans url as a payment url from backend
    
    Parameters
    ---------
        line_id : User's LINE ID to specifiy the order as string.
        number : User's Phone Number as string.
        product_code : Product or Pulsa that will be buy from User as string.

    Return
    ------
        parsed response from TUKULSA Backend as midtrans url
    """
    json_data = {
        "line_id": line_id,
        "phone_number": number,
        "product_code": product_code,
    }
    url = base_url + "users/transaction"
    headers = {'content-type' : 'application/json'}

    data = requests.post(url, json=json_data, headers=headers).text
    parsed = json.loads(data)
    return parsed

def get_alltransactions_by(line_id):
    """
    GET All User's transactions
    
    Parameters
    ---------
        line_id : User's LINE ID to specifiy the order as string.

    Return
    ------
        parsed response from TUKULSA Backend
    """
    json_data = {
        'line_id': line_id
    }
    url = base_url + 'users/transactions/filterby'
    headers = {'content-type' : 'application/json'}

    data = requests.post(url, json=json_data, headers=headers).text
    parsed = json.loads(data)
    return parsed

def get_latesttransaction_by(line_id):
    """
    GET Latest User's transactions
    
    Parameters
    ---------
        line_id : User's LINE ID to specifiy the order as string.

    Return
    ------
        parsed response from TUKULSA Backend
    """
    json_data = {
        'line_id': line_id
    }
    url = base_url + 'users/transactions/newest'
    headers = {'content-type' : 'application/json'}

    data = requests.post(url, json=json_data, headers=headers).text
    parsed = json.loads(data)
    return parsed

def get_security_code(line_id):
    """
    GET Security Code for Admin to Login
    
    Parameters
    ---------
        line_id : User's LINE ID to authenticate Admin as string.

    Return
    ------
        parsed response from TUKULSA Backend (security code)
    """
    url = base_url + 'admin/securitycode?line_id=' + line_id
    headers = {'content-type' : 'application/json'}

    data = requests.post(url, headers=headers).text
    parsed = json.loads(data)
    return parsed

def get_transaction_by(line_id, order_id):
    """
    GET Detail Transaction by order_id and line_id

    Parameters
    ----------
        line_id : User's LINE ID as string
        order_id : User's specific order_id as string

    Return
    ------
        parsed response from TUKULSA Backend (Detail Transaction)
    """
    url = base_url + 'users/transactions/edit'
    json_data = {
        'line_id': line_id,
        'order_id': order_id
    }
    headers = {'content-type' : 'application/json'}
    data = requests.put(url, json=json_data, headers=headers).text
    parsed = json.loads(data)
    return parsed