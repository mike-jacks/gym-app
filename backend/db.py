import json
from decouple import config
from sqlmodel import SQLModel, create_engine, Session, select
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy import event, inspect, Engine
from models.relationship_merge import (
    ExerciseLog, Exercise, ExerciseSpecificMuscleLink, WorkoutExercise, Workout, User, 
    WorkoutCategory, MovementCategory, BandColor, MajorMuscle, SpecificMuscle,
    Equipment, UserRoleLink, Role
)
        
def setup_database(engine: Engine):
    if not inspect(engine).get_table_names():
        SQLModel.metadata.create_all(engine)
        populate_initial_category_items(engine)
        populate_exercise_data(engine)

def populate_initial_category_items(engine: Engine):
    with open("exercise_json/new_exercise_json.json", 'r') as file:
        exercise_data = json.load(file)
    with Session(engine) as session:
        # Bulk insert setup data if not exists
        for model, key in [(WorkoutCategory, "workoutCategory"), (MovementCategory, "movementCategory"), 
                           (MajorMuscle, "majorMuscle"), (Equipment, "equipment")]:
            existing_items = {item.name: item for item in session.exec(select(model)).all()}
            new_items = set(exercise[key].title() for exercise in exercise_data)
            for item in new_items:
                if item not in existing_items:
                    session.add(model(name=item))
        for model, key in [(SpecificMuscle, "specificMuscles")]:
            existing_items = {item.name: item for item in session.exec(select(model)).all()}
            new_items = set(specific_muscle.title() for exercise in exercise_data for specific_muscle in exercise[key])
            for item in new_items:
                if item not in existing_items:
                    session.add(model(name=item))
        roles = {"User", "Admin"}
        for role in roles:
            if not session.exec(select(Role).where(Role.name == role)).first():
                session.add(Role(name=role)) 
        band_colors = {"Yellow", "Red", "Green", "Black", "Purple", "Green", "Orange", "Gray"}  # Use set for uniqueness
        existing_colors = {color.name for color in session.exec(select(BandColor))}
        session.add_all(BandColor(name=color) for color in band_colors if color not in existing_colors)
        
        session.commit()

def populate_exercise_data(engine: Engine):
    with open("exercise_json/new_exercise_json.json", 'r') as file:
        exercise_data = json.load(file)
    with Session(bind=engine) as session:
        for exercise in exercise_data:
            if session.exec(select(Exercise).where(Exercise.name == exercise["name"].title())).first():
                break
            name = exercise["name"].title()
            description = " ".join(exercise["description"])
            image_url = exercise.get("gifUrl", None)
            
            workout_category_name = exercise.get("workoutCategory", "").title()
            movement_category_name = exercise.get("movementCategory", "").title()
            major_muscle_name = exercise.get("majorMuscle", "").title()
            equipment_name = exercise.get("equipment", "").title()
            specific_muscles = exercise.get("specificMuscles", [])
            
            workout_category_id = session.exec(select(WorkoutCategory).where(WorkoutCategory.name == workout_category_name)).first().id
            movement_category_id = session.exec(select(MovementCategory).where(MovementCategory.name == movement_category_name)).first().id
            major_muscle_id = session.exec(select(MajorMuscle).where(MajorMuscle.name == major_muscle_name)).first().id
            equipment_id = session.exec(select(Equipment).where(Equipment.name == equipment_name)).first().id
            specific_muscles = [specific_muscle.title() for specific_muscle in specific_muscles]
            
            new_exercise = Exercise.model_validate({"name":name, "description":description, "image_url":image_url, "workout_category_id":workout_category_id, "movement_category_id":movement_category_id, "major_muscle_id":major_muscle_id, "equipment_id":equipment_id})
            session.add(new_exercise)
            session.commit()
            session.refresh(new_exercise)
            for specific_muscle in specific_muscles:
                specific_muscle_id = session.exec(select(SpecificMuscle.id).where(SpecificMuscle.name == specific_muscle)).first()
                session.add(ExerciseSpecificMuscleLink(exercise_id=new_exercise.id, specific_muscle_id=specific_muscle_id))
            session.commit()

# Engine setting and event listening setup

postgres_url = config("POSTGRES_URL")
engine = create_engine(postgres_url, echo=False)

setup_database(engine)




def get_db():
    with Session(bind=engine) as session:
        yield session

            