from functools import wraps
from flask import session, render_template, flash


def sessionChecker():
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if 'data' not in session:
                flash('You should be Logged in', category='error')
                return render_template('login.html')

            return fn(*args, **kwargs)

        return wrapped

    return wrapper
