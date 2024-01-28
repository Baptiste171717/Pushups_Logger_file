from .app import db 
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
<<<<<<< HEAD
    firstname = db.Column(db.String(100))
    weight = db.Column(db.Integer)
    size = db.Column(db.Integer)
    cardio_objective = db.Column(db.Integer)
    body_building_objective = db.Column(db.Integer)
    T_max = db.Column(db.Integer)
=======
    weight = db.Column(db.Integer)
    size = db.Column(db.Integer)
    test_test = db.Column(db.Integer)
>>>>>>> 9ea77226bddb10263d79a65aac5909147be49669
    workouts = db.relationship('Workout', backref = 'author', lazy=True)
    
    
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Workout_session_list = db.Column(db.JSON, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    comment = db.Column(db.Text, nullable =False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
<<<<<<< HEAD
=======
    
    
class Workout_program(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    biceps = db.Column(db.Integer, nullable = True)
    chest = db.Column(db.Integer, nullable = True)
    cardio = db.Column(db.Integer, nullable = True)
>>>>>>> 9ea77226bddb10263d79a65aac5909147be49669
