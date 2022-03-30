import requests, json
from flask import current_app as app
from hashlib import sha256

headers = {'content-type': 'application/json'}

def check_admin(data_json):
    try:
        response = requests.request(url='http://127.0.0.1:5000/checkBackOfficeToken', headers=headers,
                                    method='POST', data=data_json)
    except Exception as e:
        app.logger.info(e)
        return dict(code_time_out="0000")
    data_dict = json.loads(response.content)
    return data_dict


def force_reserve(data_json):
    try:
        # response = requests.request(url='http://35.158.69.207:5000/forceReservationOCSolde', headers=headers,
        #                             method='POST', data=data_json)
        response = requests.request(url='http://127.0.0.1:5000/forceReservationOCSolde', headers=headers,
                                    method='POST', data=data_json)
    except Exception as e:
        app.logger.error(e)
        return dict(code_time_out="0000")

    data_dict = json.loads(response.content)
    return data_dict


def manual_reserve(data_json):
    try:
        response = requests.request(url='http://127.0.0.1:5000/manualReserve', headers=headers, method='POST',
                                    data=data_json)
        # response = requests.request(url=config_data['manual_reserve'], headers=headers, method='POST',
        #                             data=data_json)
    except Exception as e:
        app.logger.error(e)
        return dict(code_time_out="0000")

    data_dict = json.loads(response.content)
    return data_dict


def cancel_reserve(data_json):
    try:
        response = requests.request(url='http://127.0.0.1:5000/soldeOCindisponible', headers=headers,
                                    method='POST', data=data_json)
        # response = requests.request(url=config_data['solde_indisponible'], headers=headers,
        #                             method='POST', data=data_json)
    except Exception as e:
        app.logger.error(e)
        return dict(code_time_out="0000")
    data_dict = json.loads(response.content)
    return data_dict


def password_hash(s):
    hash = sha256((s).encode('utf-8')).hexdigest()
    return hash
