from .app import db
from .models import User
from .models import Workout
from flask import Blueprint, render_template,redirect, request,flash,abort, url_for
from flask_login import login_required, current_user
import jsons 
import numpy as np
from .optimize import interpreter

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('Accueil.html')


@main.route('/add_information')
@login_required
def add_information():
    return render_template('additional_data.html')


@main.route('/add_information')
def add_information():
    return render_template('additional_data.html')

@main.route('/profile')
@login_required
def profile():
    workouts= Workout.query.filter_by( author = current_user ).one()
    Workout_program = workouts.Workout_session_list
    Workout_program =jsons.loads(Workout_program)
    Workout_program = np.array(Workout_program)   
    return render_template('Your-workout-program_2.html', Workout_program = Workout_program, size_session = len(Workout_program))

@main.route("/workout_session/<int:workout_id>/direct", methods = ['GET', 'POST'])
@login_required
def workout_session(workout_id):
    workouts= Workout.query.filter_by( author = current_user ).one()
    Workout_program = workouts.Workout_session_list
    Workout_program =jsons.loads(Workout_program)
    Workout_program = np.array(Workout_program)
    Workout_program_day = Workout_program[workout_id -1]
    Workout_dic = interpreter(Workout_program_day)
    size_workout = len(Workout_dic) 
    return render_template('Workout-Session.html', workout_session_number = workout_id, size_workout = size_workout, Workout_dic = Workout_dic)


"""Here we could display the template which will allow the user to add his/her own exercise into the database"""
# @main.route('/new')
# @login_required
# def new_workout():
#     return render_template('create_workout.html')

# @main.route('/new', methods = ['POST'])
# @login_required
# def new_workout_2():
#     pushups = request.form.get('pushups')
#     comment = request.form.get('comment')
    
#     workout = Workout(pushups =pushups, comment=comment, author = current_user)
#     db.session.add(workout)
#     db.session.commit()
    
#     flash('Your workout has been added!')
    
#     return redirect(url_for('main.index'))


"""This could be used to actually display the database of exercices"""
# @main.route('/all')
# @login_required
# def user_workouts():
#     page = request.args.get('page',1, type =int )
#     user = User.query.filter_by(email=current_user.email).first_or_404()
#     workouts= Workout.query.filter_by( author = user ).paginate(page=page, per_page=3)
#     return render_template('all_workouts.html', workouts = workouts, user = user)


"""these functions were part of the tutorial, they could still used to transform the database with all the workout-exercises"""

# @main.route("/workout/<int:workout_id>/update", methods = ['GET', 'POST'])
# @login_required
# def update_workout(workout_id):
#     workout =Workout.query.get_or_404(workout_id)
#     if request.method == 'POST' :
#         workout.pushups = request.form['pushups']
#         workout.comment = request.form['comment']
#         db.session.commit()
#         flash('Your workout has been updated')
#         return redirect(url_for('main.user_workouts'))

#     return render_template('update_workout.html', workout = workout)

# @main.route("/workout/<int:workout_id>/delete", methods = ['GET', 'POST'])
# @login_required
# def delete_workout(workout_id):
#     workout =Workout.query.get_or_404(workout_id)
#     db.session.delete(workout)
#     db.session.commit()
#     return redirect(url_for('main.user_workouts'))




@main.route('/display_Concept')
def display_concept():
    return render_template('Concept.html')
