import requests, json
from flask import current_app as app


def force_reserve(data_json):
    headers = {'content-type': 'application/json'}
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
    headers = {'content-type': 'application/json'}
    try:
        # try:
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
    headers = {'content-type': 'application/json'}
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
