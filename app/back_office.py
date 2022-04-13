import random, json
from flask import render_template, Blueprint, request, url_for, current_app as app, \
    redirect, flash, session
from hashlib import sha256
from app.md_helpers import manual_reserve, force_reserve, cancel_reserve, password_hash, check_admin, redirect_url
from app.sessionChecker import sessionChecker
from app.methodChecker import methodChecker
back_office = Blueprint('back_office', __name__)

methods = ['GET', 'POST']


@back_office.route('/', methods=methods)
def auth_login():
    return render_template('login.html')


@back_office.route('/logout', methods=methods)
@sessionChecker()
def logout():
    session.pop('data')
    return redirect(url_for('back_office.auth_login'))


@back_office.route('/force', methods=methods)
@methodChecker()
@sessionChecker()
def force_reservation():
    try:
        request_id = request.form.get('reservation_request_id')
        oc_ticket_num = request.form.get('oc_ticket_num')
        oc_new_solde = request.form.get('oc_new_solde')
        app.logger.info(session['data'])
        data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                    reservation_request_id=request_id,
                    app_id=int(session['data']['app_id']), oc_ticket_num=oc_ticket_num,
                    oc_new_solde=float(oc_new_solde))

        data_json = json.dumps(data)
        data_dict = force_reserve(data_json)
        app.logger.info(data_dict)
        if "code_time_out" not in data_dict:
            data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                        app_id=int(session['data']['app_id']))
            data_json_manual = json.dumps(data)
            ams = manual_reserve(data_json_manual)
            app.logger.info(ams)
            if "code_time_out" not in ams:
                flash(data_dict['message'], category="success")
                return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'], )
            if "code_time_out" in ams:
                return render_template('time_out.html')
        if "code_time_out" in data_dict:
            return render_template('time_out.html')
    except Exception as e:
        app.logger.info(e)
        return render_template('time_out.html')


@back_office.route('/soldeIndisponible', methods=methods)
@methodChecker()
@sessionChecker()
def cancel_reservation():
    try:
        request_id = request.form.get('reservation_request_id')
        oc_new_solde = request.form.get('oc_new_solde')
        data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                    reservation_request_id=request_id, app_id=int(session['data']['app_id']),
                    oc_new_solde=float(oc_new_solde))

        data_json = json.dumps(data)
        data_dict = cancel_reserve(data_json)
        app.logger.info(data_dict)
        if "code_time_out" not in data_dict:
            data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                        app_id=int(session['data']['app_id']))
            data_json_manual = json.dumps(data)
            ams = manual_reserve(data_json_manual)
            app.logger.info(ams)
            if "code_time_out" not in ams:
                flash(data_dict['message'], category='success')
                return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'], )
            if "code_time_out" in ams:
                return render_template('time_out.html', error=ams)
        if "code_time_out" in data_dict:
            return render_template('time_out.html', error=data_dict)
    except Exception as e:
        app.logger.info(e)
        return render_template('time_out.html')


@back_office.route('/reservation_details', methods=methods)
@sessionChecker()
def reservation_details():
    app.logger.info(session['data'])
    if request.method != 'POST':
        return redirect(redirect_url())
    return render_template('single_reservation.html', request_id=request.form.get('request_id'),
                           first_name=request.form.get('first_name'), last_name=request.form.get('last_name'),
                           num_id=request.form.get('num_id'), type_id=request.form.get('type_id'),
                           montant=request.form.get('montant'), dotation_code=request.form.get('dotation_code'),
                           dotation_libelle=request.form.get('dotation_libelle'))


@back_office.route('/listreservation', methods=methods)
def listreservation():
    if 'data' in session:
        data = dict(access_token=session['data']['access_token'], request_id=session['data']['request_id'],
                    app_id=int(session['data']['app_id']))
        data_json = json.dumps(data)
        ams = manual_reserve(data_json)
        app.logger.info(ams)
        app.logger.info(session)
        if "code_time_out" not in ams:
            return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'], )
        if "code_time_out" in ams:
            return render_template('time_out.html')
    if 'data' not in session:
        app_id = request.form.get('app_id')
        password = request.form.get('password')
        if not password or not app_id:
            flash('Connexion requise', category='error')
            return render_template('login.html')
        lg_data = dict(access_id=int(app_id), password=password_hash(password))
        login_data = json.dumps(lg_data)
        check_dict = check_admin(login_data)
        app.logger.info(check_dict)
        if "code_time_out" in check_dict:
            return render_template('time_out.html')
        if "code_time_out" not in check_dict:
            if check_dict['code'] != "0000":
                flash('Access Denied', category="error")
                return render_template('login.html')
            if check_dict['code'] == "0000":
                request_id = str(random.randint(99, 10000))
                access_token = sha256((password_hash(password) + request_id).encode('utf-8')).hexdigest()
                session['data'] = dict(app_id=int(app_id), access_token=access_token.upper(),
                                       request_id=str(request_id), )
                data = dict(access_token=access_token.upper(), request_id=str(request_id), app_id=int(app_id))
                data_json = json.dumps(data)
                ams = manual_reserve(data_json)
                app.logger.info(ams)
                if "code_time_out" not in ams:
                    return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'], )
                if "code_time_out" in ams:
                    return render_template('time_out.html')
