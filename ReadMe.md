
<h1> Nittany Bookstore: a Flask/SQL Web App </h1>


This project was made using Flask and Bootstrap. The backend was made using Flask-Sqlalchemy as well as raw SQLite. 

To run this project, make sure all the requirements (found in requirements.txt) are installed. Note that there may be some missing requirements depending on your system.
Next, find and execute the run.py file to launch the website. The address should be 127.0.0.1:5000. The Pycharm virtual environment I used is also included along with this project.

![Loginpage](/res/loginpage.png)

Once running, navigate to the register page via the navbar or use one of the following accounts:

Admin:
Log = admin
Pass = adminpass

User:
Log = Bot1
Pass = password


![bookexample](/res/bookexample.png)

Directories:

In the nittanybookstore directory, the models, forms and routes files can be found. Forms contains classes for every form that was used in the website (made with FlaskForm). Models contains the ORM structure of the database. Routes contains the application routes for every page, along with all of the raw and slqalchemy query code. Large raw queries are documented with comments for easier reading.

In the nittanybookstore/templates folder, there are all of the HTML files. These files contain Jinja2 code that loads data passed in from routes

There is an additional css page called home.css in the static folder, this file is a template from the internet.
