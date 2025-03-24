"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports activities
    "Basketball Team": {
        "description": "Competitive basketball team with regular games and tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "kevin@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swimming training and competitions",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["lisa@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Competitive soccer team with regular matches and tournaments",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["david@mergington.edu", "lucas@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis training and friendly matches",
        "schedule": "Tuesdays and Thursdays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["anna@mergington.edu", "mark@mergington.edu"]
    },
    # Art activities
    "Drama Club": {
        "description": "Theater productions and acting workshops",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["emily@mergington.edu", "noah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing and mixed media art workshops",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn photography techniques and participate in photo walks",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["mia@mergington.edu", "liam@mergington.edu"]
    },
    "Music Band": {
        "description": "Practice and perform in a school band",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["chloe@mergington.edu", "jack@mergington.edu"]
    },
    # Intellectual activities
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills through competitions",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 16,
        "participants": ["sarah@mergington.edu", "jacob@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for and compete in science-based academic competitions",
        "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["ethan@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging math problems and prepare for math competitions",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["nathan@mergington.edu", "grace@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Build and program robots for competitions",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["oliver@mergington.edu", "ava@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validar se o aluno já está inscrito
    if email in activity["participants"]:
        raise HTTPException(
            status_code=409, 
            detail=f"Student {email} is already signed up for {activity_name}"
        )
    
    # Verificar se atingiu o máximo de participantes
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(
            status_code=409,
            detail=f"The activity {activity_name} has reached maximum capacity"
        )
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
