from nittanybookstore import app, db
from nittanybookstore.models import *
import csv

# Only for database init and population
from nittanybookstore import db
from nittanybookstore.models import keywords, authors, usefulness, trusts, User, Book, Keyword, Order, Author, Rating

if __name__ == '__main__':
    app.run(debug=True)
