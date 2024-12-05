import json
from flask import Blueprint, request
from sqlalchemy import select
from functions.locationFunctions import getLocation
from util.session import Session

from models.db.location import Location as DbLocation
from models.api.location import Location as ApiLocation

from models.api.location import Relationships

app = Blueprint("location", __name__)

@app.route("")
def getAllLocations():
    session = Session()
    res = session.query(DbLocation).all()
    tempArr = ApiLocation.fromDbs(res, Relationships.ALL, Relationships.ALL)
    arr = []
    for location in tempArr:
        arr.append(location)
    session.close()
    return json.dumps(
            arr,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4), 200

@app.route("root")
def getRootLocations():
    session = Session()
    res = session.query(DbLocation).filter(DbLocation.parent_id == None).all()
    tempArr = ApiLocation.fromDbs(res, Relationships.NONE, Relationships.ALL)
    arr = []
    for location in tempArr:
        arr.append(location)
    session.close()
    return json.dumps(
            arr,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4), 200

@app.route("", methods=["POST"])
def create():
    session = Session()
    jsonData = request.json
    force = request.args.get('force')
    print(force)
    try:
        name = jsonData["name"]
    except KeyError:
        return "Model is invalid", 400
    
    try:
        parent_id = jsonData["parent_id"]
    except KeyError:
        parent_id = None
    
    dbLocation = DbLocation.new(name, parent_id)
    session.add(dbLocation)
    session.commit()
    
    location = ApiLocation.fromDb(getLocation(dbLocation.id), Relationships.ALL, Relationships.ALL)
    
    return location.toJSON(), 200