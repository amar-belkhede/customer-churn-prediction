from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from churnprediction.models import User

class ChurnForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    gender = SelectField(u'Gender', choices=[('0', 'Female'), ('1', 'Male') ])
    seniorCitizen = SelectField(u'Senior Citizen', choices=[('0', 'No'), ('1', 'Yes') ])
    partner = SelectField(u'Partner', choices=[('0', 'No'), ('1', 'Yes') ])
    dependents = SelectField(u'Dependents', choices=[('0', 'No'), ('1', 'Yes') ])
    tenure = IntegerField(u'Tenure', [NumberRange(min=0, max=72)],  render_kw={"placeholder": "0 years to 72 years"})
    phoneService = SelectField(u'Phone Service', choices=[('0', 'No'), ('1', 'Yes') ])
    multipleLines = SelectField(u'Multiple Lines', choices=[('0', 'No'), ('1', 'No phone serive'), ('2', 'Yes') ])
    internetService = SelectField(u'Internet Service', choices=[('0', 'DSL'), ('1', 'Fiber Optic'), ('2', 'No') ])
    onlineSecurity = SelectField(u'Online Security', choices=[('0', 'No'), ('1', 'No internet service'), ('2', 'Yes') ])
    onlineBackup = SelectField(u'Online Backup', choices=[('0', 'No'), ('1', 'No internet service'), ('2', 'Yes') ])
    deviceProtection = SelectField(u'Device Protection', choices=[('0', 'No'), ('1', 'No internet service'), ('2', 'Yes') ])
    techSupport = SelectField(u'Tech Support', choices=[('0', 'No'), ('1', 'No internet service'), ('2', 'Yes') ])
    streamingTV = SelectField(u'Streaming TV', choices=[('0', 'No'), ('1', 'No internet service'), ('2', 'Yes') ])
    streamingmovies = SelectField(u'Streaming movies', choices=[('0', 'No'), ('1', 'No internet service'), ('2', 'Yes') ])
    contract = SelectField(u'Contract', choices=[('0', 'Month-to-month'), ('1', 'One year'), ('2', 'Two year') ])
    paperlessBilling = SelectField(u'Paperless Billing', choices=[('0', 'No'), ('1', 'Yes') ])
    paymentMethod = SelectField(u'Payment Method', choices=[('0', 'Bank Transfer (automatic)'), ('1', 'Credit card (automatic)'), ('2', 'Electronic Check'), ('3', 'Mailed Check') ])
    monthlyCharges = IntegerField(u'Monthly Charges', [NumberRange(min=0, max=120)],  render_kw={"placeholder": "$0 to $120"})
    totalcharges = IntegerField(u'Total charges', [NumberRange(min=1, max=8700)],  render_kw={"placeholder": "$1 to $8700"})
    
    submit = SubmitField('Predict')


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')