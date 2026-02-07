from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth',__name__)

USER_CREDENTIAL = {
    'username':'aadi',
    'password':'7764'
}

@auth_bp.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('task.view_tasks'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET' , 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USER_CREDENTIAL['username'] and password == USER_CREDENTIAL['password']:
            session['user'] = username
            flash('Login successful','success')
            return redirect(url_for('task.view_tasks'))
        else:
            flash('invalid username or password', 'danger')    

    return render_template('login.html')        

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out','info')
    return redirect(url_for('auth.login'))






