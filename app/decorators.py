from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'ADMIN':
            flash('Cần là admin để truy cập trang này.', 'Lỗi')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function