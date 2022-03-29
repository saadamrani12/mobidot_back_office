import random, json
from flask import render_template, Blueprint, request, url_for, current_app as app, session, \
    redirect, flash
from hashlib import sha256
from flask_login import login_required, login_user, logout_user, current_user
from .models import Administrators
from app.md_helpers import manual_reserve, force_reserve, cancel_reserve

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


@back_office.route(
    '/force_form/id=<request_id>&first_name=<first_name>&last_name=<last_name>&num_id=<num_id>&type_id=<type_id>',
    methods=methods)
@login_required
def force_reserve_form(request_id, first_name, last_name, num_id, type_id):
    if 'data' in session:
        return render_template('force_reserve_form.html', request_id=request_id, first_name=first_name,
                               last_name=last_name, num_id=num_id, type_id=type_id, user=current_user)


@back_office.route('/force', methods=methods)
@login_required
def force_reservation():
    try:
        request_id = request.form.get('reservation_request_id')
        oc_ticket_num = request.form.get('oc_ticket_num')
        oc_new_solde = request.form.get('oc_new_solde')
        if not request_id or not oc_new_solde:
            return render_template('login.html')
        app.logger.info(request_id)
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
                flash(data_dict['message'], category="success")
                return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'],
                                       user=current_user)
            if "code_time_out" in ams:
                return render_template('time_out.html')
        if "code_time_out" in data_dict:
            return render_template('time_out.html')
    except Exception as e:
        app.logger.info(e)
        return render_template('time_out.html')


@back_office.route(
    '/solde_ind/id=<request_id>&first_name=<first_name>&last_name=<last_name>&num_id=<num_id>&type_id=<type_id>',
    methods=methods)
@login_required
def solde_indisponible_form(request_id, first_name, last_name, num_id, type_id):
    return render_template('solde_indisponible.html', request_id=request_id, first_name=first_name,
                           last_name=last_name, num_id=num_id, type_id=type_id, user=current_user)


@back_office.route('/soldeIndisponible', methods=methods)
@login_required
def cancel_reservation():
    try:
        request_id = request.form.get('reservation_request_id')
        oc_new_solde = request.form.get('oc_new_solde')
        if not request_id or not oc_new_solde:
            return render_template('login.html')
        data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                    reservation_request_id=request_id, app_id=int(session['data']['app_id']),
                    oc_new_solde=float(oc_new_solde))

        data_json = json.dumps(data)
        data_dict = cancel_reserve(data_json)
        if "code_time_out" not in data_dict:
            data = dict(request_id=session['data']['request_id'], access_token=session['data']['access_token'],
                        app_id=int(session['data']['app_id']))
            data_json_manual = json.dumps(data)
            ams = manual_reserve(data_json_manual)
            if "code_time_out" not in ams:
                flash(data_dict['message'], category='success')
                return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'],
                                       user=current_user)
            if "code_time_out" in ams:
                return render_template('time_out.html', error=ams)
        if "code_time_out" in ams:
            return render_template('time_out.html', error=data_dict)
    except Exception as e:
        app.logger.info(e)
        return render_template('time_out.html')


@back_office.route('listreservation', methods=methods)
def listreservation():
    if 'data' in session:
        request_id = str(random.randint(99, 10000))
        access_token = sha256((session['data']['password'] + request_id).encode('utf-8')).hexdigest()
        data = dict(access_token=access_token.upper(), request_id=str(request_id),
                    app_id=int(session['data']['app_id']))
        data_json = json.dumps(data)
        ams = manual_reserve(data_json)
        if "code_time_out" not in ams:
            return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'],
                                   user=current_user)
        if "code_time_out" in ams:
            return render_template('time_out.html')
    if 'data' not in session:
        app_id = request.form.get('app_id')
        password = request.form.get('password')
        user = Administrators.query.filter_by(mobidot_access=app_id).first()
        if not user:
            flash('Access Denied', category="error")
            return render_template('login.html')
        if user:
            if user.password == password:
                request_id = str(random.randint(99, 10000))
                access_token = sha256((password + request_id).encode('utf-8')).hexdigest()
                session['data'] = dict(app_id=int(app_id), access_token=access_token.upper(),
                                       request_id=str(request_id),
                                       password=password)
                login_user(user, remember=True)
                data = dict(access_token=access_token.upper(), request_id=str(request_id), app_id=int(app_id))
                data_json = json.dumps(data)
                ams = manual_reserve(data_json)
                if "code_time_out" not in ams:
                    return render_template('reservation.html', code=ams['code'], reservations=ams['reservation'],
                                           user=current_user)
                if "code_time_out" in ams:
                    return render_template('time_out.html')
            if password != user.password:
                flash('Wrong Password', category="error")
                return render_template('login.html')


@back_office.route(
    '/reservation_details/id=<request_id>&first_name=<first_name>&last_name=<last_name>&num_id=<num_id>&type_id=<type_id>&montant=<montant>',
    methods=methods)
@login_required
def reservation_details(request_id, first_name, last_name, num_id, type_id, montant):
    return render_template('single_reservation.html', request_id=request_id, first_name=first_name,
                           last_name=last_name, num_id=num_id, type_id=type_id, montant=montant, user=current_user)
