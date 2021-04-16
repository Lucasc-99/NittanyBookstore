from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b971f3a241822da6c85d7954f8a0b146'


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


if __name__ == '__main__':
    app.run(debug=True)
