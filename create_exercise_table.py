"""
this file allows to transform the excel tables which containted 
all the workout exercices into a sqllite database
"""


import csv
from dateutil.parser import parse
from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///Workout_excel.sqlite3", echo=True)


Base = declarative_base()


class Workout_table(Base):
    __tablename__ = "Workout_table"
    id = Column(Integer, primary_key=True)
    Exercise = Column(String(200))
    Cardio_Intensity = Column(Integer)
    Trapezius = Column(Integer)
    Shoulders = Column(Integer)
    Biceps = Column(Integer)
    Triceps = Column(Integer)
    Forearm = Column(Integer)
    Latissimus_dorsi = Column(Integer)
    Chest = Column(Integer)
    Abs = Column(Integer)
    Glutes = Column(Integer)
    Quadriceps = Column(Integer)
    Calves = Column(Integer)
    Reps = Column(Integer)
    Last_review = Column(Date, nullable=True)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def parse_none(dt):
    try:
        return parse(dt)
    except Exception as e:
        print(e)
        return None


def prepare_listing(row):
    row["Last_review"] = parse_none(row["Last_review"])
    return Workout_table(**row)


with open("TDLOG_exercises_2.csv", encoding="utf-8", newline="") as csv_file:
    csvreader = csv.DictReader(csv_file, quotechar='"')
    listings = [prepare_listing(row) for row in csvreader]
    session = Session()
    session.add_all(listings)
    session.commit()
