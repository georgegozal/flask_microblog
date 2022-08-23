from flask import Blueprint, render_template, request, flash ,redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm
from .models import Users



auth = Blueprint('auth',__name__,template_folder='templates/auth')

# Create Login Page
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfully",category="success")
                return redirect(url_for('view.dashboard'))
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
    return redirect(url_for('view.login'))

# Create Dashboard Page
@auth.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    user = Users.query.get_or_404(id)
    if request.method == 'POST':
        print(request.form)
        user.name = request.form['name']
        user.email = request.form['email']
        user.favorite_color = request.form['favorite_color']
        user.username = request.form['username']
        user.about_author = request.form['about_author']
        # get uploaded file/image
        #user.profile_pic = request.files['profile_pic'] 
        # Gram Image Name
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
            form.profile_pic.data.save(f'static/images/{pic_name}')
            # user.profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER']))
            # save pic name in user model
            user.profile_pic = pic_name
        try:
            db.session.commit()
            flash('User Updated Successfully!',category='success')
            return render_template(
                'dashboard.html',
                user=user,
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
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        try:
            user = Users.query.filter_by(username=username).first()
            if user:
                flash('Username Already is used',category='error')
            user1 = Users.query.filter_by(email=email).first()
            if user1:
                flash('Email Already is used',category='error')
        except Exception as e:
            print(e)
            user = None
            user1 = None
        if user is None and user1 is None:
            user = Users(
                username = username,
                name = form.name.data,
                email = form.email.data,
                favorite_color = form.favorite_color.data,
                password_hash = generate_password_hash(form.password_hash.data, 'sha256')
                )
            # user.password(form.password_hash.data)
            try:
                db.session.add(user)
                db.session.commit()
                flash("User Added Successfully!")
                return redirect('/user/add')
            except:
                flash('Error',category='error')
    try:
        # our_users = Users.query.all()#.order_by(Users.date_added)#.all()
        our_users = Users.query.order_by(Users.id.desc()).all()
    except:
        our_users = ''
    return render_template(
            'add_user.html',
            form=form,
            our_users=our_users)
