from flask import Blueprint, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .models import Workout
from .app import db
from sqlalchemy.exc import IntegrityError
from .optimize import repartition_jours, create_workout_session
import jsons 

auth = Blueprint('auth',__name__)

@auth.route('/signup')
def signup():
    return render_template('signup_page_2.html')



@auth.route('/signup', methods =['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    firstname = request.form.get('firstname')
   
    user = User.query.filter_by( email = email).first() 
   
    if user:
        return redirect(url_for('auth.signup'))
    
    new_user = User(email = email, name = name, password = generate_password_hash(password, method='pbkdf2:sha256'), firstname = firstname)
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
 
    return redirect(url_for('auth.login'))


    

@auth.route('/login')
def login():
    return render_template('Login_page_3.html')

@auth.route('/login', methods =['POST'])
def login_post():
    render_template('additional_data.html')
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
   
    user = User.query.filter_by( email = email).first() 


    if not user or not check_password_hash(user.password, password):
        return render_template('signup_page_2.html')
    
    login_user(user, remember=remember)
    
    if user.weight is None:
        return render_template('additional_data.html')
    
    return redirect(url_for('main.profile'))



@auth.route('/add_information', methods = ['POST'])
@login_required
def new_information():
    weight = request.form.get('weight')
    size = request.form.get('size')
    cardio_objective = int(request.form.get('cardio_objective'))
    body_building_objective = int(request.form.get('body_building_objective'))
    freq = int(request.form.get('freq'))
    T_max = int(request.form.get('T_max'))*60
    
    user = User.query.filter_by(id = current_user.id).first_or_404()
    
    user.weight = weight
    user.size = size
    user.cardio_objective = cardio_objective
    user.body_building_objective = body_building_objective
    user.T_max = T_max
    cardio_objective_bool = bool(cardio_objective)
    body_building_objective_bool = bool(body_building_objective)
    Workout_program = repartition_jours(freq, body_building_objective_bool, cardio_objective_bool)
    Workout_session = create_workout_session(Workout_program, T_max)
    lst = Workout_session.tolist()
    json_str = jsons.dumps(lst)
    workout = Workout( Workout_session_list = json_str, comment= "so cool", author = current_user)
    db.session.add(workout)
    
    db.session.commit()
    

    
    return redirect(url_for('main.profile'))


    
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/add_information", methods = ['GET', 'POST'])
@login_required
def update_information(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST' :
        user.weight = request.form['weight']
        user.size = request.form['size']
        user.cardio_objective = request.form['cardio_objective']
        user.body_building_objective = request.form['body_building_objective']
        db.session.commit()
        flash('Your data have been updated')
        return redirect(url_for('main.profile'))
    return render_template('Your-workout-program_2.html', user = user)


@auth.route("/forgot_password_email", methods = ['GET','POST'])
def ask_email():
     return render_template('email_forgot.html')
 

@auth.route("/display_change_password", methods = ['GET','POST'])
def display_change_password():
    email = request.form.get('email')
    user = User.query.filter_by( email = email).first() 
    return render_template('forgot_password.html', user_name = user.name, user_email = user.email)

@auth.route("/change_password/", methods = ['GET','POST'])
def change_password():
    password = request.form.get('password')
    email = request.form.get('user_email')
    user = User.query.filter_by( email = email).first() 
    user.password = generate_password_hash(password, method='pbkdf2:sha256')
    db.session.commit()
    return redirect(url_for('auth.login'))