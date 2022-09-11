from flask import Blueprint, render_template, request, flash ,redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from .forms import LoginForm,UserForm
import uuid as uuid
from .models import User
from app import db



auth = Blueprint('auth',__name__,template_folder='templates/auth')

# Create Login Page
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        print(user)
        # print(check_password_hash(user.password_hash, form.password.data))
        # print(user.password_hash)
        print(form.password.data)
        if user:
            # Check the hash
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash("Login Successfully",category="success")
                return redirect(url_for('auth.dashboard'))
            else:
                flash("Wrong Password - Try Again!",category="error")
        else:
            flash("That User Doesn`t Exist! Try Again...", category='error')
    return render_template(
        'login.html',
        form=form
    )

# Create Logout Page
@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!")
    return redirect(url_for('auth.login'))

# Create Dashboard Page
@auth.route('/dashboard',methods=['GET','POST'])
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


            # Check if user has not a profile_pic or  uploading new pic is not the same as uploaded one
            if not user.profile_pic or '_'.join(user.profile_pic.split('_')[1:]) != pic_filename:
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
            flash('User Updated Successfully!',category='success')
            return render_template(
                'dashboard.html',
                user=current_user,
                form=form
            )
        except:
            flash('Error!')
            return render_template(
                'dashboard.html',
                user=user,
                form=form
            )
    else:
        return render_template(
            'dashboard.html',
            user=current_user,
            form=form
        )

# Register New User
@auth.route('/user/add',methods=['GET','POST'])
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
                flash('Username Already is used',category='error')
            user1 = User.query.filter_by(email=email).first()
            if user1:
                flash('Email Already is used',category='error')
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
                username = username,
                name = form.name.data,
                email = email,
                profile_pic = pic_name
                )
            user.set_password(form.password_hash.data)
            # user.password(form.password_hash.data)
            try:
                db.session.add(user)
                db.session.commit()
                flash("User Added Successfully!")
                login_user(user)
                #send_email_after_register(email) # sent email 
                return redirect(url_for('auth.dashboard'))
            except:
                flash('Error',category='error')
    if form.errors != {}: #If there are not errors from the validations
        for err_message in form.errors.values():
            flash(f'There was an error with creating a user: {err_message}', category='error')

    return render_template(
            'add_user.html',
            form=form)

def send_email_after_register(email_to):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import datetime
    now = datetime.datetime.now()

    SERVER = 'smtp.gmail.com' # "your smtp server"
    PORT = 587 # your port number
    FROM =  'microblog@gmail.com' # "your from email id"
    TO = email_to # "your to email ids"  # can be a list
    PASS = '***********' # "your email id's password"

    message = MIMEMultipart()
    message['Subject'] = 'Registration Success Message - [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)

    message['From'] = FROM
    message['To'] = TO

    text = 'Your registration to our blog has been successed, Welcome!'
    message.attach(MIMEText(text))
    print('Initiating Server...')

    server = smtplib.SMTP(SERVER, PORT)
    #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    #server.ehlo
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, message.as_string())

    print('Email Sent...')

    server.quit()