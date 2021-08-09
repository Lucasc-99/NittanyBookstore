
<h1> Nittany Bookstore: a Flask/SQL Bookstore Web App </h1>


A final project for the Database Management Systems Course at Penn State (CMPSC 431W)

This project was made using Flask and Bootstrap. The backend was made using Flask-Sqlalchemy as well as raw SQLite.

To run this project, make sure all the requirements (found in requirements.txt) are installed. Note that there may be some missing requirements depending on your system.
Next, find and execute the run.py file to launch the website. The address should be 127.0.0.1:5000. The Pycharm virtual environment I used is also included along with this project.



Once running, navigate to the register page via the navbar or use one of the following accounts:

Admin:
Log = admin
Pass = adminpass

User:
Log = Bot1
Pass = password


Once you have logged in, navigate to the Search Books page at the top left. Here you can search books via conjunctive queries, and use the drop down menus to choose how to order your results and to enable degrees of separation search. Books will appear below the search form after submission. Click on the title of any book to navigate to the page for that book. On this page you can view all the book information, order books, leave a review, and view all ratings given to that book. Once you have ordered a book, you can navigate to the recommended page to view books that were ordered by users that also ordered the book you have just ordered. If no books match this criteria, none will show up.

If you click on the username in any of the ratings, it will take you to the profile page for that user. You can access your own profile page at the top right of the nabber. At this page you can view all relevant user information as well as the users trust score. If you are not viewing your own page you can give the user a trust or a distrust.

If you click on "find this rating useful?" for any rating, you will navigate to the page for that rating where you can view its total usefulness score as well as give it your own usefulness score.

Navigate to Order History at the top right of the page to view your order history.

If you are logged in to the admin account, you can navigate to the manager dashboard. In this dashboard you can add new books, change the stock level of books, promote a user to an admin, and view relevant user/book statistics. 

Click logout at the top right if you would like to logout and sign in to a different account or create a new one.

Directories:

In the nittanybookstore directory, the models, forms and routes files can be found. Forms contains classes for every form that was used in the website (made with FlaskForm). Models contains the ORM structure of the database. Routes contains the application routes for every page, along with all of the raw and slqalchemy query code. Large raw queries are documented with comments for easier reading.

In the nittanybookstore/templates folder, there are all of the HTML files. These files contain Jinja2 code that loads data passed in from routes

There is an additional css page called home.css in the static folder, this file is a template from the internet.
