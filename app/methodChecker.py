from functools import wraps
from flask import session, render_template, flash, request


def methodChecker():
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if request.method != 'POST':
                if 'data' in session:
                    session.pop('data')
                flash('Non autorisé', category='error')
                return render_template('login.html')

            return fn(*args, **kwargs)

        return wrapped

    return wrapper
