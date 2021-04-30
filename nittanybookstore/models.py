from flask_login import UserMixin

from nittanybookstore import db, login_manager
import csv
import random
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Tables List:
# keywords, authors, usefulness, trusts, User, Book, Keyword, Order, Author, Rating

# Many-to-Many Tables

# Maps keywords to books
keywords = db.Table('keywords',
                    db.Column('ISBN', db.String(15), db.ForeignKey('book.ISBN'), primary_key=True),
                    db.Column('word', db.String(50), db.ForeignKey('keyword.word'), primary_key=True)
                    )

# For authorship
authors = db.Table('authors',
                   db.Column('ISBN', db.String(15), db.ForeignKey('book.ISBN'), primary_key=True),
                   db.Column('authorID', db.Integer, db.ForeignKey('author.authorID'), primary_key=True)
                   )

# For Usefulness Ratings
usefulness = db.Table('usefulness',
                      db.Column('id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('ratingID', db.Integer, db.ForeignKey('rating.ratingID'), primary_key=True),
                      db.Column('useScore', db.Integer, nullable=True)
                      )
# Maps user trust ratings
trusts = db.Table('trusts',
                  db.Column('sender', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                  db.Column('receiver', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                  db.Column('trustScore', db.Integer, nullable=True)
                  )
# Maps books to price
costs = db.Table('costs',
                 db.Column('book_isbn', db.String(15), db.ForeignKey('book.ISBN'), primary_key=True),
                 db.Column('cost', db.Integer))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    logname = db.Column(db.String(20), unique=True)
    logpass = db.Column(db.String(20), nullable=False)
    access = db.Column(db.Integer, nullable=False)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    addr = db.Column(db.String(50))
    title = db.Column(db.String(50))
    orders = db.relationship('Order', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    trust_scored_users = db.relationship('User', secondary=trusts,
                                         primaryjoin=(trusts.c.sender == id),
                                         secondaryjoin=(trusts.c.receiver == id),
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_isbn = db.Column(db.String(15), db.ForeignKey('book.ISBN'), nullable=False)


class Author(db.Model):
    authorID = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50))


class Rating(db.Model):
    ratingID = db.Column(db.Integer, primary_key=True)
    ratingScore = db.Column(db.Integer, nullable=False)  # must be 0-10
    ratingComment = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_isbn = db.Column(db.String(15), db.ForeignKey('book.ISBN'), nullable=False)
    received_use_scores = db.relationship('User', secondary=usefulness, lazy='subquery',
                                          backref=db.backref('sent_use_scores', lazy=True))