from flask import render_template, url_for, flash, redirect, request
from nittanybookstore.forms import LoginForm, RegistrationForm
from nittanybookstore import app, bcrypt
from nittanybookstore.models import *
from flask_login import login_user, current_user, login_required, logout_user


@app.route('/homepage', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('homepage.html')


@app.route('/about')
@login_required
def about():
    return render_template('aboutpage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template('homepage.html')
    form = RegistrationForm()
    if form.validate_on_submit():
        record = User.query.filter_by(logname=form.username.data).first()
        if record is None:
            h = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(fname=form.firstname.data, lname=form.lastname.data,
                            phone=form.phone.data, addr=form.address.data,
                            logname=form.username.data,
                            logpass=h, access=0)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account Registered for {form.username.data}', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'Account with username {form.username.data} already exists', 'danger')
    return render_template('registerpage.html', form=form)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('homepage.html')
    form = LoginForm()
    if form.validate_on_submit():
        record = User.query.filter_by(logname=form.username.data).first()
        if record and bcrypt.check_password_hash(record.logpass, form.password.data):
            login_user(record)
            next_page = request.args.get('next')
            flash(f'Successful Login for {form.username.data}', 'success')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            flash(f'Incorrect Username or Password', 'danger')
    return render_template('loginpage.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user_profile')
@login_required
def profile():
    img = url_for('static', filename="pictures/default_user_profile.jpg")
    return render_template('profilepage.html', image_file=img)

@app.route('/recommended_page')
@login_required
def recommended():
    return render_template('recommendedpage.html')