from nittanybookstore import db
import csv
import random
from datetime import datetime

# Begin Relational Database Schema

# keywords, authors, usefulness, trusts, User, Book, Keyword, Order, Author, Rating

# Many-to-Many Tables
keywords = db.Table('keywords',
                    db.Column('ISBN', db.String(15), db.ForeignKey('book.ISBN'), primary_key=True),
                    db.Column('word', db.String(50), db.ForeignKey('keyword.word'), primary_key=True)
                    )

authors = db.Table('authors',
                   db.Column('ISBN', db.String(15), db.ForeignKey('book.ISBN'), primary_key=True),
                   db.Column('authorID', db.Integer, db.ForeignKey('author.authorID'), primary_key=True)
                   )

# Need something else here?
usefulness = db.Table('usefulness',
                      db.Column('logname', db.String(15), db.ForeignKey('user.logname'), primary_key=True),
                      db.Column('ratingID', db.Integer, db.ForeignKey('rating.ratingID'), primary_key=True),
                      db.Column('useScore', db.Integer, nullable=True)
                      )

trusts = db.Table('trusts',
                  db.Column('sender', db.String(15), db.ForeignKey('user.logname'), primary_key=True),
                  db.Column('receiver', db.String(15), db.ForeignKey('user.logname'), primary_key=True),
                  db.Column('trustScore', db.Integer, nullable=True)
                  )


class User(db.Model):
    logname = db.Column(db.String(20), primary_key=True)
    logpass = db.Column(db.String(20), unique=True, nullable=False)
    access = db.Column(db.Integer, nullable=False)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    addr = db.Column(db.String(50))
    title = db.Column(db.String(50))
    orders = db.relationship('Order', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    trust_scored_users = db.relationship('User', secondary=trusts,
                                         primaryjoin=(trusts.c.sender == logname),
                                         secondaryjoin=(trusts.c.receiver == logname),
                                         lazy='subquery',
                                         backref=db.backref('trust_scored_by', lazy=True))


class Book(db.Model):
    ISBN = db.Column(db.String(15), primary_key=True)
    title = db.Column(db.String(400), nullable=False)
    stock = db.Column(db.Integer, nullable=False)  # Need positivity constraint here
    genre = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime)
    orders = db.relationship('Order', backref='book', lazy=True)
    ratings = db.relationship('Rating', backref='book', lazy=True)
    keywords = db.relationship('Keyword', secondary=keywords, lazy='subquery',
                               backref=db.backref('books', lazy=True))
    authors = db.relationship('Author', secondary=authors, lazy='subquery',
                              backref=db.backref('books', lazy=True))


class Keyword(db.Model):
    word = db.Column(db.String(50), primary_key=True)


class Order(db.Model):
    orderID = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DATE, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('user.logname'), nullable=False)
    book_isbn = db.Column(db.String(15), db.ForeignKey('book.ISBN'), nullable=False)


class Author(db.Model):
    authorID = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50))


class Rating(db.Model):
    ratingID = db.Column(db.Integer, primary_key=True)
    ratingScore = db.Column(db.Integer, nullable=False)
    ratingComment = db.Column(db.String(400))
    user_id = db.Column(db.String(20), db.ForeignKey('user.logname'), nullable=False)
    book_isbn = db.Column(db.String(15), db.ForeignKey('book.ISBN'), nullable=False)
    received_use_scores = db.relationship('User', secondary=usefulness, lazy='subquery',
                                          backref=db.backref('sent_use_scores', lazy=True))


'''
# Code for populating database w Books, Keywords, and Authors

genres = {0: 'fantasy', 1: 'sci-fi', 2: 'romance', 3: 'mystery'}
def populate_books():
    db.create_all()
    with open('nittanybookstore/books.csv', newline='') as booksdata:
        r = csv.reader(booksdata, delimiter=',')
        index = 0
        for row in r:
            if index == 0:
                index += 1
            else:
                date = datetime.strptime(row[10],'%m/%d/%Y')
                title = row[1]
                lang = row[6]
                isbn = row[4]
                publisher = row[11]
                genre = genres[random.randint(0, 3)]
                index += 1
                b = Book(ISBN=isbn, stock=100, language=lang, genre=genre, title=title, publisher=publisher, date=date)
                for w in row[2].split(sep='/'):
                    n = w.split(" ")

                    if len(n) == 0:
                        a = Author(lname="NA")
                        recs = Author.query.filter_by(lname="NA").all()
                    elif len(n) == 1:
                        a = Author(lname=n[0])
                        recs = Author.query.filter_by(lname=n[0]).all()
                    elif len(n) == 2:
                        a = Author(fname=n[0], lname=n[1])
                        recs = Author.query.filter_by(fname=n[0], lname=n[1]).all()
                    else:
                        a = Author(fname=n[0], lname=n[-1])
                        recs = Author.query.filter_by(fname=n[0], lname=n[-1]).all()

                    # Add author if is new

                    if len(recs) == 0:
                        b.authors.append(a)
                        db.session.add(a)
                        db.session.commit()
                    else:
                        b.authors.extend(recs)

                for k in title.split(" "):
                    if k.isalpha() and k[0].isupper():
                        recs = Keyword.query.filter_by(word=k).first()
                        word = Keyword(word=k)
                        if recs is None:
                            b.keywords.append(word)
                            db.session.add(word)
                            db.session.commit()
                        elif recs not in b.keywords:
                            b.keywords.append(recs)

                db.session.add(b)
                index += 1

        db.session.commit()
'''
