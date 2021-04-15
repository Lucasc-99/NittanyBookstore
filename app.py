from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b971f3a241822da6c85d7954f8a0b146'


@app.route('/')
@app.route('/homepage')
def hello():
    return "<h1>Home Page</h1>"


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('registerpage.html', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('loginpage.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
