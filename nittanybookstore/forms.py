from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class RateForm(FlaskForm):
    rate_score_field = IntegerField('Score/10', validators=[DataRequired(), NumberRange(0, 10)])
    rate_comment_field = TextAreaField('Comment', validators=[Length(max=400)])
    submit = SubmitField('Submit')


class SearchBarForm(FlaskForm):
    choices = [('avgscore', 'Highest Rated'),
                ('date', 'Publish Date'),
               ('avgtrustedscore', 'Highest Trusted Ratings')]

    title_field = StringField('Title')
    author_field = StringField('Author')
    publisher_field = StringField('Publisher')
    language_field = StringField('Language')
    order_by_field = SelectField('Order By', choices=choices)
    submit = SubmitField('Search')


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=20)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    address = StringField('Address', validators=[Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=2, max=20)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Sign In')
