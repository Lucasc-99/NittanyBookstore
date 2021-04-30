from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class FilterStatisticsForm(FlaskForm):
    m = IntegerField('m', validators=[DataRequired()])
    submit = SubmitField('Filter')

class PromoteUserForm(FlaskForm):
    logname_field = StringField('User Login Name', validators=[DataRequired()])
    submit = SubmitField('Promote')


class StockLevelForm(FlaskForm):
    isbn_field = StringField('ISBN', validators=[DataRequired()])
    stock_change_field = IntegerField('Change in Stock', validators=[DataRequired()])
    submit = SubmitField('Change Stock')


class TrustForm(FlaskForm):
    # Encoding yes:1, no:-1, none:None
    choices = [('no_selection', '...'), ('trust_user', 'Trust'), ('distrust_user', 'Distrust')]
    trust_field = SelectField('trust', choices=choices, validators=[DataRequired()])
    submit = SubmitField('Submit')


class UsefulnessForm(FlaskForm):
    # Encoding useless:-1, useful:1, very useful:2
    choices = [('...', '...'),('useless', 'Useless'), ('useful', 'Useful'), ('very_useful', 'Very Useful')]
    use_field = SelectField('use', choices=choices, validators=[DataRequired()])
    submit = SubmitField('Submit')


class OrderForm(FlaskForm):
    quantity_field = IntegerField('Quantity (max 10 books)', validators=[DataRequired(), NumberRange(1, 10)])
    submit = SubmitField('Order')


class TopNRatingsForm(FlaskForm):
    n = IntegerField('Top n useful ratings:', validators=[DataRequired(), NumberRange(1, 10)])
    submit = SubmitField('Filter')


class RateForm(FlaskForm):
    rate_score_field = IntegerField('Score out of 10', validators=[DataRequired(), NumberRange(0, 10)])
    rate_comment_field = TextAreaField('Comment', validators=[Length(max=400)])
    submit = SubmitField('Submit')


class SearchBarForm(FlaskForm):
    choices = [('avgscore', 'Highest Rated'),
                ('date', 'Publish Date'),
               ('avgtrustedscore', 'Highest Trusted Ratings')]

    title_field = StringField('Title')
    author_field = StringField('Author')
    half_separation = SelectField('1/2 Degree Separation of Authorship',
                                  choices=[('disabled', 'Disabled'), ('enabled', '1-Degree'), ('enabled2', '2-Degree')])
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
