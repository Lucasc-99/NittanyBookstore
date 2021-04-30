from flask import render_template, url_for, flash, redirect, request
from sqlalchemy import text
import datetime

from nittanybookstore.forms import LoginForm, RegistrationForm, SearchBarForm, RateForm, \
    OrderForm, TrustForm, UsefulnessForm, TopNRatingsForm
from nittanybookstore import app, bcrypt
from nittanybookstore.models import *
from flask_login import login_user, current_user, login_required, logout_user


@app.route('/homepage', methods=['GET', 'POST'])
@login_required
def home():
    s_form = SearchBarForm()

    # Query builder for book search
    books = []
    if s_form.validate_on_submit():
        order = ""
        sub = ""
        ratings_sub = "rating r"

        if s_form.order_by_field.data == 'avgtrustedscore':
            ratings_sub = f"""
                (SELECT book_isbn, ratingScore
                FROM (Rating r INNER JOIN User u ON r.user_id = u.id) INNER JOIN trusts t ON t.receiver = u.id 
                GROUP BY u.id
                HAVING SUM(t.trustScore) > 0) AS r
            """

        if s_form.order_by_field.data == "avgscore" or s_form.order_by_field.data == 'avgtrustedscore':
            order = "ORDER BY rateavg DESC"
            sub = f"""
                LEFT OUTER JOIN (SELECT b.ISBN AS isbn, AVG(r.ratingScore) as rateavg FROM book b, {ratings_sub} 
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
                b.ISBN = aut.ISBN AND a.authorID = aut.authorID AND 
                ((a.fname || ' ' || a.lname) LIKE '%{s_form.author_field.data}%')  AND 
                b.publisher LIKE '%{s_form.publisher_field.data}%' AND 
                b.title LIKE '%{s_form.title_field.data}%' AND 
                b.language LIKE '%{s_form.language_field.data}%'  
                 {order} 
                LIMIT 100     
        """

        if s_form.half_separation.data == 'enabled' and s_form.author_field.data != "":
            half_sub = f"""(
                        SELECT a1.authorID as a1id, a2.authorID as a2id,
                                (a2.fname||' '||a2.lname) as a2name
                        FROM authors aut1 LEFT JOIN author a1 ON aut1.authorID = a1.authorID,
                            authors aut2 LEFT JOIN author a2 ON aut2.authorID = a2.authorID
                        WHERE 
                            a1.authorID != a2.authorID
                        LIMIT 100
                        ) AS collabs """

            authors_sub_q = f"""
                (SELECT DISTINCT a.authorID 
                FROM author a, {half_sub}
                WHERE 
                ((a.fname || ' ' || a.lname) LIKE '%{s_form.author_field.data}%') OR
                (a.authorID = collabs.a1id AND collabs.a2name LIKE '%{s_form.author_field.data}%') 
                LIMIT 100
                )
                
            """
            query_txt = f"""
                SELECT DISTINCT b.ISBN
                FROM   book b {sub} INNER JOIN authors aut ON b.ISBN = aut.ISBN  
                    INNER JOIN
                    {authors_sub_q} a ON aut.authorID = a.authorID
                WHERE
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
    t_form = TrustForm()

    if current_user != userid and t_form.validate_on_submit():
        t_score = None
        if t_form.trust_field.data == 'trust_user':
            t_score = 1
        elif t_form.trust_field.data == 'distrust_user':
            t_score = -1

        if u in current_user.trust_scored_users:
            db.session.query(trusts).filter_by(sender=current_user.id, receiver=u.id).update(dict(trustScore=t_score))
        else:
            ins = trusts.insert().values(sender=current_user.id, receiver=u.id, trustScore=t_score)
            db.session.execute(ins)
        db.session.commit()

    agg_t_score = 0
    received_t_scores = db.session.query(trusts).filter_by(receiver=u.id).all()
    for s in received_t_scores:
        if s.trustScore:
            agg_t_score += s.trustScore

    rec = db.session.query(trusts).filter_by(sender=current_user.id, receiver=u.id).first()
    prompt_text = 'Trust this User?'
    if rec is None:
        pass
    elif rec.trustScore == 1:
        prompt_text = 'You trust this user'
    elif rec.trustScore == -1:
        prompt_text = 'You do not trust this user'

    return render_template('profilepage.html', image_file=img, b=Book, u=u, t=trusts,
                           form=t_form, prompt_text=prompt_text, agg_t_score=agg_t_score)


@app.route('/recommended_page', methods=['GET', 'POST'])
@login_required
def recommended():
    recs = None
    text = ""
    if len(current_user.orders) != 0:
        recs = []
        text = "Order a book to receive recommendations"
    else:
        q = f""""""
    return render_template('recommendedpage.html', recs=recs)


@app.route('/order_history')
@login_required
def order_history():
    return render_template('orderhistorypage.html', b=Book)


@app.route('/book/<book_isbn>', methods=['GET', 'POST'])
@login_required
def book(book_isbn):
    img = url_for('static', filename="pictures/books.png")
    b = Book.query.filter_by(ISBN=book_isbn).first()
    c = db.session.query(costs).filter_by(book_isbn=book_isbn).first()
    r_form = RateForm()
    o_form = OrderForm()
    f_form = TopNRatingsForm()
    ratings_list = []

    if b:
        if f_form.validate_on_submit():
            n = str(f_form.n.data)
            q = f"""
                SELECT DISTINCT r.ratingID 
                FROM rating r LEFT OUTER JOIN
                    (SELECT AVG(u.useScore) AS avguscore, r.ratingID AS ratingID FROM rating r, usefulness u
                        WHERE r.ratingID = u.ratingID
                        GROUP BY r.ratingID
                    ) u ON r.ratingID = u.ratingID
                WHERE r.book_isbn = "{b.ISBN}"
                ORDER BY u.avguscore DESC
                LIMIT {n}
            """
            query_txt = text(q)

            q_list = db.session.execute(query_txt)
            for row in q_list:
                ratings_list.append(Rating.query.filter_by(ratingID=row[0]).first())

        elif r_form.validate_on_submit():
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
        elif o_form.validate_on_submit():
            if b.stock - o_form.quantity_field.data > 0:
                order = Order(price=c.cost * o_form.quantity_field.data, time=datetime.now(),
                              amount=o_form.quantity_field.data, user_id=current_user.id, book_isbn=book_isbn)
                db.session.add(order)
                b.stock = b.stock - o_form.quantity_field.data
                db.session.commit()
                flash(f'Thank you for your order!', 'success')
            else:
                flash(f'That order cannot be satisfied with our current stock', 'danger')
        elif request.method == 'POST':
            flash(f'Make sure you are filling out your order or rating correctly', 'danger')
        if not f_form.validate_on_submit():
            ratings_list = b.ratings
        return render_template('bookpage.html', f_form=f_form,
                               ratings_list=ratings_list, b=b, c=c, u=User,
                               image_file=img, form=r_form, form_order=o_form)
    else:
        return redirect(url_for('home'))


@app.route('/rating/<rating_id>', methods=['GET', 'POST'])
@login_required
def rating_page(rating_id):
    r = Rating.query.filter_by(ratingID=rating_id).first()
    b = Book.query.filter_by(ISBN=r.book_isbn).first()
    u = User

    form = UsefulnessForm()

    if current_user.id != r.user_id and form.validate_on_submit():
        use_score = None
        if form.use_field.data == 'useless':
            use_score = -1
        elif form.use_field.data == 'useful':
            use_score = 1
        elif form.use_field.data == 'very_useful':
            use_score = 2

        if current_user in r.received_use_scores:
            db.session.query(usefulness).filter_by(ratingID=r.ratingID, id=current_user.id).update(
                dict(useScore=use_score))
        else:
            ins = usefulness.insert().values(id=current_user.id, ratingID=r.ratingID, useScore=use_score)
            db.session.execute(ins)
        db.session.commit()

    elif current_user.id != r.user_id and form.validate_on_submit():
        flash('You cannot score your own review!', 'danger')

    agg_u_score = 0
    received_scores = db.session.query(usefulness).filter_by(ratingID=r.ratingID).all()
    for s in received_scores:
        if s.useScore:
            agg_u_score += s.useScore

    return render_template('rating_page.html', agg_u_score=agg_u_score, form=form, r=r, b=b, u=u)
