from datetime import datetime
from flask import Blueprint, request
from sqlalchemy import func, select, or_, and_
import json

from util.session import Session
from models.db.research import Research

app = Blueprint("research", __name__)

@app.route("/active")
def getActiveResearch():
    return getActiveResearchAtTime(datetime.isoformat(datetime.now()))

@app.route("/active/<time>")
def getActiveResearchAtTime(time):
    session = Session()
    req = session.query(Research).filter(Research.start_time < time).filter(Research.end_time > time).first()
    if (req == None):
        return json.dumps(Research().value()), 200
    return json.dumps(req.value()), 200

@app.route("")
def getAll():
    session = Session()
    request = select(Research)
    arr = []
    print(request)
    for research in session.scalars(request):
        arr.append(research.value())
    return json.dumps(arr), 200

@app.route("", methods=["POST"])
def create():
    session = Session()
    jsonData = request.json
    force = request.args.get('force')
    print(force)
    try:
        question = jsonData["question"]
        start_time_string: datetime = jsonData["startTime"]
        start_time = datetime.fromisoformat(start_time_string)
        end_time_string = jsonData["endTime"]
        end_time = datetime.fromisoformat(end_time_string)
    except KeyError:
        return "Model is invalid", 400
    except ValueError:
        return "Time is not in valid ISO format", 400
    
    numActiveResearches = session.query(
        func.count(Research.id)
        ).filter(and_(Research.end_time > start_time, Research.start_time < end_time))
    
    print(numActiveResearches.scalar())
    # TODO:
    # if another research is already happening at that time, cancel and tell user to use force flag
    # if force flag is used, allow
    
    research = Research.new(question, start_time, end_time)
    session.add(research)
    session.commit()
    
    return json.dumps(research.value()), 200