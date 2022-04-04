import random, json
from flask import render_template, Blueprint, request, url_for, current_app as app, \
    redirect, flash, session
from hashlib import sha256
from app.md_helpers import manual_reserve, force_reserve, cancel_reserve, password_hash, check_admin
from app.sessionChecker import sessionChecker

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


@back_office.route(
    '/force_form/id=<request_id>&first_name=<first_name>&last_name=<last_name>&num_id=<num_id>&type_id=<type_id>',
    methods=methods)
@sessionChecker()
def force_reserve_form(request_id, first_name, last_name, num_id, type_id):
    app.logger.info(session['data'])
    return render_template('force_reserve_form.html', request_id=request_id, first_name=first_name,
                           last_name=last_name, num_id=num_id, type_id=type_id)


@back_office.route('/force', methods=methods)
@sessionChecker()
def force_reservation():
    try:
        request_id = request.form.get('reservation_request_id')
        oc_ticket_num = request.form.get('oc_ticket_num')
        oc_new_solde = request.form.get('oc_new_solde')
        if not oc_ticket_num or not oc_new_solde:
            if 'data' in session:
                session.pop('data')
            flash('Please go step by step', category='error')
            return render_template('login.html')
        app.logger.info(session['data'])
        data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                    reservation_request_id=request_id,
                    app_id=int(session['data']['app_id']), oc_ticket_num=oc_ticket_num,
                    oc_new_solde=float(oc_new_solde))

        data_json = json.dumps(data)

        data_dict = force_reserve(data_json)
        if "code_time_out" not in data_dict:
            data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                        app_id=int(session['data']['app_id']))
            data_json_manual = json.dumps(data)
            ams = manual_reserve(data_json_manual)
            if "code_time_out" not in ams:
                app.logger.info(ams)
                flash(data_dict['message'], category="success")
                return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'], )
            if "code_time_out" in ams:
                app.logger.info(ams)
                return render_template('time_out.html')
        if "code_time_out" in data_dict:
            app.logger.info(data_dict)
            return render_template('time_out.html')
    except Exception as e:
        app.logger.info(e)
        return render_template('time_out.html')


@back_office.route(
    '/solde_ind/id=<request_id>&first_name=<first_name>&last_name=<last_name>&num_id=<num_id>&type_id=<type_id>',
    methods=methods)
@sessionChecker()
def solde_indisponible_form(request_id, first_name, last_name, num_id, type_id):
    app.logger.info(session['data'])
    return render_template('solde_indisponible.html', request_id=request_id, first_name=first_name,
                           last_name=last_name, num_id=num_id, type_id=type_id)


@back_office.route('/soldeIndisponible', methods=methods)
@sessionChecker()
def cancel_reservation():
    try:
        request_id = request.form.get('reservation_request_id')
        oc_new_solde = request.form.get('oc_new_solde')
        if not request_id or not oc_new_solde:
            if 'data' in session:
                session.pop('data')
            flash('Please go step by step', category='error')
            return render_template('login.html')
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


@back_office.route('/listreservation', methods=methods)
def listreservation():
    if 'data' in session:
        request_id = str(random.randint(99, 10000))
        access_token = sha256((password_hash(session['data']['password']) + request_id).encode('utf-8')).hexdigest()
        data = dict(access_token=access_token.upper(), request_id=str(request_id),
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
            flash('Login Required', category='error')
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
                                       request_id=str(request_id),
                                       password=password)
                app.logger.info(session)
                data = dict(access_token=access_token.upper(), request_id=str(request_id), app_id=int(app_id))
                data_json = json.dumps(data)
                ams = manual_reserve(data_json)
                app.logger.info(ams)
                if "code_time_out" not in ams:
                    return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'], )
                if "code_time_out" in ams:
                    return render_template('time_out.html')


@back_office.route(
    '/reservation_details?id=<request_id>&first_name=<first_name>&last_name=<last_name>&num_id=<num_id>&type_id=<type_id>&montant=<montant>',
    methods=methods)
@sessionChecker()
def reservation_details(request_id, first_name, last_name, num_id, type_id, montant):
    # if 'data' in session:
    app.logger.info(session['data'])
    return render_template('single_reservation.html', request_id=request_id, first_name=first_name, last_name=last_name,
                           num_id=num_id, type_id=type_id, montant=montant)
    # flash('You should be Logged in', category='error')
    # return render_template('login.html')
