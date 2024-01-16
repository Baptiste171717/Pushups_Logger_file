from flask import Blueprint, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .app import db
from sqlalchemy.exc import IntegrityError


auth = Blueprint('auth',__name__)

@auth.route('/signup')
def signup():
    
    return render_template('signup.html')



@auth.route('/signup', methods =['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
   
    user = User.query.filter_by( email = email).first() 
   
    if user:
        return redirect(url_for('auth.signup'))
    
    new_user = User(email = email, name = name, password = generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    
    return redirect (url_for('auth.login'))


    

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods =['POST'])
def login_post():
    
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
   
    user = User.query.filter_by( email = email).first() 

    if not user or not check_password_hash(user.password, password):
        return redirect('auth.login')
    
    login_user(user, remember=remember)
    
    if user.weight is None:
        return render_template('additional_data.html')
    
    return redirect(url_for('main.profile'))



@auth.route('/add_information', methods = ['POST'])
@login_required
def new_information():
    weight = request.form.get('weight')
    size = request.form.get('size')
    
    user = User.query.filter_by(email=current_user.email).first_or_404()
    
    user.weight = weight
    user.size = size
    
    db.session.commit()
    
    flash('Your data have been uploaded !')
    
    return redirect(url_for('main.profile'))
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/add_information", methods = ['GET', 'POST'])
@login_required
def update_information(user_id):
    user =User.query.get_or_404(user_id)
    if request.method == 'POST' :
        user.weight = request.form['weight']
        user.size = request.form['size']
        db.session.commit()
        flash('Your data have been updated')
        return redirect(url_for('main.profile'))

    return render_template('profile.html', user = user)