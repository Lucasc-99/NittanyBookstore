from flask import render_template, url_for, flash, redirect, request
from sqlalchemy import text
import datetime

from nittanybookstore.forms import LoginForm, RegistrationForm, SearchBarForm, RateForm
from nittanybookstore import app, bcrypt
from nittanybookstore.models import *
from flask_login import login_user, current_user, login_required, logout_user


def get_user_avg_trust_rating(id):
    u = User.query.filter_by(id=id).first()

@app.route('/homepage', methods=['GET', 'POST'])
@login_required
def home():
    s_form = SearchBarForm()

    # Query builder for book search
    books = []
    if s_form.validate_on_submit():
        order = ""
        sub = ""
        if s_form.order_by_field.data == "avgscore":
            order = "ORDER BY rateavg DESC"
            sub = """
                LEFT OUTER JOIN (SELECT b.ISBN AS isbn, AVG(r.ratingScore) as rateavg FROM book b, rating r 
                WHERE b.ISBN = r.book_isbn 
                GROUP BY b.ISBN 
                ) rateavgs ON rateavgs.isbn = b.ISBN 
            """
        elif s_form.order_by_field.data == "date":
            order = "ORDER BY datetime(b.date)"

        query_txt = f"""
            SELECT DISTINCT b.ISBN 
            FROM book b {sub}, authors aut, author a 
            WHERE 
                b.ISBN = aut.ISBN AND 
                a.authorID = aut.authorID AND 
                (a.fname || ' ' || a.lname) LIKE '%{s_form.author_field.data}%' AND 
                b.publisher LIKE '%{s_form.publisher_field.data}%' AND 
                b.title LIKE '%{s_form.title_field.data}%' AND 
                b.language LIKE '%{s_form.language_field.data}%'  
                 {order} 
                LIMIT 100     
        """
        query_txt = text(query_txt)
        q = db.session.execute(query_txt)
        for row in q:
            books.append(Book.query.filter_by(ISBN=row[0]).first())

    return render_template('homepage.html', form=s_form, books=books)


@app.route('/about')
@login_required
def about():
    return render_template('aboutpage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        record = User.query.filter_by(logname=form.username.data).first()
        if record and bcrypt.check_password_hash(record.logpass, form.password.data):
            login_user(record)
            flash(f'Successful Login for {form.username.data}', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Incorrect Username or Password', 'danger')
    return render_template('loginpage.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user_profile/<userid>', methods=['GET', 'POST'])
@login_required
def profile(userid):
    if userid is None:
        userid = current_user.id
    img = url_for('static', filename="pictures/default_user_profile.jpg")
    u = User.query.filter_by(id=userid).first()
    return render_template('profilepage.html', image_file=img, b=Book, u=u)


@app.route('/recommended_page')
@login_required
def recommended():
    return render_template('recommendedpage.html')


@app.route('/order_history')
@login_required
def order_history():
    return render_template('orderhistorypage.html')


@app.route('/book/<book_isbn>', methods=['GET', 'POST'])
@login_required
def book(book_isbn):
    img = url_for('static', filename="pictures/books.png")
    b = Book.query.filter_by(ISBN=book_isbn).first()
    r_form = RateForm()

    if b:
        if r_form.validate_on_submit():
            rec = Rating.query.filter_by(user_id=current_user.id, book_isbn=book_isbn).first()
            print(type(r_form.rate_score_field.data))
            if rec is None:
                if r_form.rate_comment_field != "":
                    r = Rating(ratingScore=r_form.rate_score_field.data, ratingComment=r_form.rate_comment_field.data,
                               book_isbn=book_isbn, user_id=current_user.id)
                else:
                    r = Rating(ratingScore=r_form.rate_score_field.data, book_isbn=book_isbn, user_id=current_user.id)

                db.session.add(r)
                db.session.commit()
                flash(f'Thank you for your review!', 'success')
            else:
                flash(f'You have already reviewed this book', 'danger')
        return render_template('bookpage.html', b=b, u=User, image_file=img, form=r_form)
    else:
        return redirect(url_for('home'))
