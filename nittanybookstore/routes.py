from flask import render_template, url_for, flash, redirect
from nittanybookstore.forms import LoginForm, RegistrationForm
from nittanybookstore import app


@app.route('/')
@app.route('/homepage')
def home():
    return render_template('homepage.html')


@app.route('/about')
def about():
    return render_template('aboutpage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Registered for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('registerpage.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'adminpassword':
            flash(f'Successful Login for {form.username.data}', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Incorrect Username or Password', 'danger')
    return render_template('loginpage.html', form=form)

# End Flask App Code
