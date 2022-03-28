import requests, random, json
from flask import render_template, Blueprint, request, url_for, current_app as app, session, \
    redirect, flash
from hashlib import sha256
from .models import User
from . import db
from flask_login import login_required, login_user, logout_user, current_user

back_office = Blueprint('back_office', __name__)

methods = ['GET', 'POST']

with open('./config.json') as config:
    config_data = json.load(config)


@back_office.route('/', methods=methods)
def auth_login():
    return render_template('login.html')


@back_office.route('/logout', methods=methods)
@login_required
def logout():
    if 'data' in session:
        session.pop('data')
    logout_user()
    return redirect(url_for('back_office.auth_login'))


def manual_reserve(data_json):
    headers = {'content-type': 'application/json'}
    try:
        # response = requests.request(url='http://35.158.69.207:5000/manualReserve', headers=headers, method='POST',
        #                             data=data_json)
        response = requests.request(url=config_data['manual_reserve'], headers=headers, method='POST',
                                    data=data_json)
    except Exception as e:
        print(e)
        return render_template('time_out.html')
    print(response.content)
    data_dict = json.loads(response.content)
    return data_dict


@back_office.route('/listreservation', methods=methods)
def create_session():
    if 'data' in session:
        request_id = str(random.randint(99, 10000))
        access_token = sha256((session['data']['password'] + request_id).encode('utf-8')).hexdigest()
        data = dict(access_token=access_token.upper(), request_id=str(request_id),
                    app_id=int(session['data']['app_id']))
        data_json = json.dumps(data)
        ams = manual_reserve(data_json)
        if ams['code'] == "0000":
            # login_user(current_user, remember=True)
            return render_template('reservation.html', reservations=ams['reservation'], user=current_user)
        if ams['code'] != "0000":
            # return render_template('fault.html', error=ams)
            flash(ams['message'], category="error")
            return render_template('login.html', error=ams)

    if 'data' not in session:
        # try:
        app_id = request.form.get('app_id')
        password = str(request.form.get('password'))
        # =====================================================================
        request_id = str(random.randint(99, 10000))
        access_token = sha256((password + request_id).encode('utf-8')).hexdigest()
        user = User.query.filter_by(mobidot_access=app_id).first()
        if user:
            login_user(user, remember=True)

            session['data'] = dict(app_id=int(app_id), access_token=access_token.upper(),
                                   request_id=str(request_id),
                                   password=password)
            data = dict(access_token=access_token.upper(), request_id=str(request_id), app_id=int(app_id))
            data_json = json.dumps(data)
            ams = manual_reserve(data_json)
            if ams['code'] == "0000":
                login_user(user, remember=True)
                return render_template('reservation.html', reservations=ams['reservation'], user=current_user)
            if ams['code'] != "0000":
                # return render_template('fault.html', error=ams)
                flash(ams['message'], category="error")
                return render_template('login.html', error=ams)

        if not user:
            data = {'password': password}
            headers = {'content-type': 'application/json'}
            try:
                # response = requests.request(url='http://35.158.69.207:5000/checkBackOfficeToken', headers=headers,
                #                             data=json.dumps(data), method='POST')
                response = requests.request(url=config_data['check_token'], headers=headers,
                                            data=json.dumps(data), method='POST')
                app.logger.info(response)
            except Exception as e:
                print('==============')
                return render_template('time_out.html')
            # print(response.content)
            data_dict = json.loads(response.content)

            if data_dict['code'] == "0000":
                session['data'] = dict(app_id=int(app_id), access_token=access_token.upper(),
                                       request_id=str(request_id),
                                       password=password)
                new_user = User(mobidot_access=app_id, access_token=access_token.upper())
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)

                data = dict(access_token=access_token.upper(), request_id=str(request_id), app_id=int(app_id))
                data_json = json.dumps(data)
                ams = manual_reserve(data_json)
                if ams['code'] == "0000":
                    # login_user(new_user, remember=True)
                    return render_template('reservation.html', reservations=ams['reservation'], user=current_user)
                if ams['code'] != "0000":
                    flash(ams['message'], category="success")
                    return render_template('fault.html', error=ams)

        if data_dict['code'] == "0008":
            flash("Check your password", category="error")
            print('mmmmmmm==============')
            return render_template('login.html')

        # except Exception as e:
        #     print(str(e))
        #     return render_template('time_out.html')


@back_office.route('/ts/<request_id>/<first_name>/<last_name>', methods=methods)
@login_required
def force_reserve_form(request_id, first_name, last_name):
    if 'data' not in session:
        return render_template('login.html')
    if 'data' in session:
        return render_template('force_reserve_form.html', request_id=request_id, first_name=first_name,
                               last_name=last_name, user=current_user)


@back_office.route('/force', methods=methods)
@login_required
def force_reservation():
    try:
        request_id = request.form.get('reservation_request_id')
        oc_ticket_num = request.form.get('oc_ticket_num')
        oc_new_solde = request.form.get('oc_new_solde')
        oc_solde_id = 0
        if request.form.get('oc_solde_id') != '':
            oc_solde_id = request.form.get('oc_solde_id')

        app.logger.info(request_id)
        data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                    reservation_request_id=request_id,
                    app_id=int(session['data']['app_id']), oc_ticket_num=oc_ticket_num,
                    oc_new_solde=float(oc_new_solde),
                    oc_solde_id=(oc_solde_id))

        data_json = json.dumps(data)

        headers = {'content-type': 'application/json'}
        try:
            # response = requests.request(url='http://35.158.69.207:5000/forceReservationOCSolde', headers=headers,
            #                             method='POST', data=data_json)
            response = requests.request(url=config_data['force_reserve'], headers=headers,
                                        method='POST', data=data_json)
        except Exception as e:
            app.logger.error(e)
            print('mmmm')
            return render_template('time_out.html')

        data_dict = json.loads(response.content)
        print(data_dict)

        if data_dict['code'] == "0000":
            data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                        app_id=int(session['data']['app_id']))
            data_json_manual = json.dumps(data)
            ams = manual_reserve(data_json_manual)
            if ams['code'] == "0000":
                return render_template('reservation.html', reservations=ams['reservation'], user=current_user)
            if ams['code'] != "0000":
                return render_template('fault.html', error=ams)
        if data_dict['code'] != "0000":
            return render_template('fault.html', error=data_dict)
    except Exception as e:
        app.logger.info(e)
        print(str(e))
        return render_template('time_out.html')


@back_office.route('/solde_ind/<request_id>/<first_name>/<last_name>', methods=methods)
@login_required
def solde_indisponible_form(request_id, first_name, last_name):
    # if 'data' in session:
    return render_template('solde_indisponible.html', request_id=request_id, first_name=first_name,
                               last_name=last_name, user=current_user)
    # return render_template('login.html')


@back_office.route('/soldeIndisponible', methods=methods)
@login_required
def cancel_reservation():
    try:
        request_id = request.form.get('reservation_request_id')
        oc_new_solde = request.form.get('oc_new_solde')

        data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                    reservation_request_id=request_id, app_id=int(session['data']['app_id']),
                    oc_new_solde=float(oc_new_solde))

        data_json = json.dumps(data)

        headers = {'content-type': 'application/json'}
        try:
            # response = requests.request(url='http://35.158.69.207:5000/soldeOCindisponible', headers=headers,
            #                             method='POST', data=data_json)
            response = requests.request(url=config_data['solde_indisponible'], headers=headers,
                                        method='POST', data=data_json)
        except Exception as e:
            app.logger.error(e)
            print('mmmm')
            return render_template('time_out.html')

        data_dict = json.loads(response.content)
        print(data_dict)

        if data_dict['code'] == "0000":
            data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                        app_id=int(session['data']['app_id']))
            data_json_manual = json.dumps(data)
            ams = manual_reserve(data_json_manual)
            if ams['code'] == "0000":
                return render_template('reservation.html', reservations=ams['reservation'], user=current_user)
            if ams['code'] != "0000":
                return render_template('fault.html', error=ams)
        if data_dict['code'] != "0000":
            return render_template('fault.html', error=data_dict)
    except Exception as e:
        app.logger.info(e)
        return render_template('time_out.html')
