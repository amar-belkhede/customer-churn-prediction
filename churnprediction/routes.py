from churnprediction.serializer import serializerJson
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, send_file
from churnprediction import app, db, bcrypt, mail
from churnprediction.forms import (RegistrationForm, LoginForm, UpdateAccountForm, ChurnForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from churnprediction.models import User, Post, Churn
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    churns = Churn.query.order_by(Churn.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('churn_list.html', churns=churns)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/explore")
def explore():
    return render_template('explore.html', title='Explore')

@app.route('/download')
def download_webpage():
    path = "EDA_and_Conclusion.pdf"
    return send_file(path, as_attachment=True)

@app.route("/conclusion")
def conclusion():
    return render_template('conclusion.html', title='Conclusion')

@app.route("/churnprediction", methods=['GET', 'POST'])
def churnprediction():
    form = ChurnForm()
    if form.validate_on_submit():
        churn = Churn(
                    title=form.title.data,
                    content=form.content.data,
                    gender=form.gender.data, 
                    seniorCitizen=form.seniorCitizen.data, 
                    partner=form.partner.data,
                    dependents=form.dependents.data,
                    tenure=form.tenure.data,
                    phoneService=form.phoneService.data,
                    multipleLines=form.multipleLines.data,
                    internetService=form.internetService.data,
                    onlineSecurity=form.onlineSecurity.data,
                    onlineBackup=form.onlineBackup.data,
                    deviceProtection=form.deviceProtection.data,
                    techSupport=form.techSupport.data,
                    streamingTV=form.streamingTV.data,
                    streamingmovies=form.streamingmovies.data,
                    contract=form.contract.data,
                    paperlessBilling=form.paperlessBilling.data,
                    paymentMethod=form.paymentMethod.data,
                    monthlyCharges=form.monthlyCharges.data,
                    totalcharges=form.totalcharges.data,
                    author=current_user
                    )
        print(churn)
        db.session.add(churn)
        db.session.commit()
        serializerJson(form.data)
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('churn_prediction.html', title='Churn Prediction',
                           form=form, legend='Churn Prediction')


@app.route("/churn/<int:churn_id>")
def churn(churn_id):
    churn = Churn.query.get_or_404(churn_id)
    return render_template('churn.html', title=churn.title, churn=churn)

@app.route("/churn/<int:churn_id>/update", methods=['GET', 'POST'])
@login_required
def update_churn(churn_id):
    churn = Churn.query.get_or_404(churn_id)
    if churn.author != current_user:
        abort(403)
    form = ChurnForm()
    if form.validate_on_submit():
        churn.title = form.title.data
        churn.content = form.content.data
        churn.gender = form.gender.data
        churn.seniorCitizen = form.seniorCitizen.data
        churn.partner = form.partner.data
        churn.dependents = form.dependents.data
        churn.tenure = form.tenure.data
        churn.phoneService = form.phoneService.data
        churn.multipleLines = form.multipleLines.data
        churn.internetService = form.internetService.data
        churn.onlineSecurity = form.onlineSecurity.data
        churn.onlineBackup = form.onlineBackup.data
        churn.deviceProtection = form.deviceProtection.data
        churn.techSupport = form.techSupport.data
        churn.streamingTV = form.streamingTV.data
        churn.streamingmovies = form.streamingmovies.data
        churn.contract = form.contract.data
        churn.paperlessBilling = form.paperlessBilling.data
        churn.paymentMethod = form.paymentMethod.data
        churn.monthlyCharges = form.monthlyCharges.data
        churn.totalcharges = form.totalcharges.data
        db.session.commit()
        serializerJson(form.data)
        print(form.data)
        flash('Your churn has been updated!', 'success')
        return redirect(url_for('churn', churn_id=churn.id))
    elif request.method == 'GET':
        form.title.data = churn.title
        form.content.data = churn.content
        form.seniorCitizen.data = churn.seniorCitizen
        form.partner.data = churn.partner
        form.dependents.data = churn.dependents
        form.tenure.data = churn.tenure
        form.phoneService.data = churn.phoneService
        form.multipleLines.data = churn.multipleLines
        form.internetService.data = churn.internetService
        form.onlineSecurity.data = churn.onlineSecurity
        form.onlineBackup.data = churn.onlineBackup
        form.deviceProtection.data = churn.deviceProtection
        form.techSupport.data = churn.techSupport
        form.streamingTV.data = churn.streamingTV
        form.streamingmovies.data = churn.streamingmovies
        form.contract.data = churn.contract
        form.paperlessBilling.data = churn.paperlessBilling
        form.paymentMethod.data = churn.paymentMethod
        form.monthlyCharges.data = churn.monthlyCharges
        form.totalcharges.data = churn.totalcharges
    return render_template('churn_prediction.html', title='Update churn',
                           form=form, legend='Update churn')


@app.route("/churn/<int:churn_id>/delete", methods=['POST'])
@login_required
def delete_churn(churn_id):
    churn = Churn.query.get_or_404(churn_id)
    if churn.author != current_user:
        abort(403)
    db.session.delete(churn)
    db.session.commit()
    flash('Your churn has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)




@app.route("/user/<string:username>")
def user_churns(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    churns = Churn.query.filter_by(author=user)\
        .order_by(Churn.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_churns.html', churns=churns, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)