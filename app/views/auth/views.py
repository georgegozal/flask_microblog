from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from .forms import LoginForm, UserForm, RequestResetForm, ResetPasswordForm
import uuid as uuid
from .models import User
from app.extensions import db, mail
from flask_mail import Message


auth = Blueprint('auth', __name__, template_folder='templates')


# Create Login Page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash("Login Successfully", category="success")
                return redirect(url_for('auth.dashboard'))
            else:
                flash("Wrong Password - Try Again!", category="error")
        else:
            flash("That User Doesn`t Exist! Try Again...", category='error')
    return render_template(
        'auth/login.html',
        form=form
    )


# Create Logout Page
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!")
    return redirect(url_for('auth.login'))


# Create Dashboard Page
@auth.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.username = request.form['username']
        user.about_author = request.form['about_author']
        if form.profile_pic.data:
            try:
                pic_filename = secure_filename(form.profile_pic.data.filename)
            except AttributeError:
                pic_filename = '_'.join(user.profile_pic.split('_')[1:])
            # Check if user has not a profile_pic or
            # uploading new pic is not the same as uploaded one
            if not user.profile_pic or '_'.join(
                user.profile_pic.split('_')[1:]) != pic_filename:
                # Set UUID
                # this gives us unique name
                # we need this incase two user uploaded pic with same name
                pic_name = str(uuid.uuid1()) + "_" + pic_filename

                # Save That Image
                form.profile_pic.data.save(f'app/static/uploads/{pic_name}')
                # user.profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER']))
                # save pic name in user model
                user.profile_pic = pic_name
        try:
            db.session.commit()
            flash('User Updated Successfully!', category='success')
            return render_template(
                'auth/dashboard.html',
                user=current_user,
                form=form
            )
        except Exception as e:
            flash(e)
            return render_template(
                'auth/dashboard.html',
                user=user,
                form=form
            )
    else:
        return render_template(
            'auth/dashboard.html',
            user=current_user,
            form=form
        )


# Register New User
@auth.route('/user/add', methods=['GET', 'POST'])
def register():
    form = UserForm()
    # print(request.form)

    if form.validate_on_submit():

        print(request.form)
        email = form.email.data
        username = form.username.data
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username Already is used', category='error')
            user1 = User.query.filter_by(email=email).first()
            if user1:
                flash('Email Already is used', category='error')
        except Exception as e:
            print(e)
            user = None
            user1 = None
        if user is None and user1 is None:
            # Gram Image Name
            try:
                pic_filename = secure_filename(form.profile_pic.data.filename)
                # Set UUID
                # this gives us unique name
                # we need this incase two user uploaded pic with same name
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                # Save That Image
                form.profile_pic.data.save(f'app/static/uploads/{pic_name}')
            except Exception as e:
                pic_name = None
                print(e)

            user = User(
                username=username,
                name=form.name.data,
                email=email,
                profile_pic=pic_name
            )
            user.set_password(form.password_hash.data)
            try:
                db.session.add(user)
                db.session.commit()
                flash("User Added Successfully!")
                login_user(user)
                try:
                    # send email to new user
                    send_mail_after_register(user)
                except Exception as e:
                    print(e)
                return redirect(url_for('auth.dashboard'))
            except Exception as e:
                print(e)
    if form.errors != {}:  # If there are validations errors
        for err_message in form.errors.values():
            flash(f'There was an error with creating a user: \
                {err_message}', category='error')

    return render_template(
            'auth/add_user.html',
            form=form)


def send_mail_after_register(user):
    link = request.url[:-9] + '/login'
    # link = url_for('auth.login')
    msg = Message('"User Added Successfully!"', recipients=[f'{user.email}'])
    msg.body = "Your registration was successful! \n \
        please login here Log In {}"
    msg.html = 'Your registration was successful! \n \
        please login here <a href="{}">Log In</a> '.format(link)
    mail.send(msg)
    print("Message sent!")


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
        sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('auth.reset_token', token=token, _external=True)}

    If you did not make this request then simply
    ignore this email and no changes will be made.
    '''
    mail.send(msg)


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)
