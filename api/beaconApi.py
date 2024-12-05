from flask import Blueprint, request
from util.session import Session
from models.db.beacon import Beacon

import json

from sqlalchemy import func, select, or_, and_


app = Blueprint("beacon", __name__)

@app.route("")
def getAllBeacons():
    session = Session()
    request = select(Beacon)
    arr = []
    print(request)
    for beacon in session.scalars(request):
        arr.append(beacon.value())
    return json.dumps(arr), 200

@app.route("/location/<location_id>")

@app.route("/<beacon_id>")
def getBeaconById(beacon_id):
    session = Session()
    request = session.query(Beacon).filter(Beacon.id == beacon_id).first()

    if (request == None):
        return json.dumps(Beacon().value()), 200
    return json.dumps(request.value()), 200

@app.route("/register/<beacon_uid>", methods=["POST"])
def registerBeacon(beacon_uid):
    session = Session()
    newBeacon = Beacon.new(beacon_uid)
    print(newBeacon.value())
    session.add(newBeacon)
    session.commit()

    return json.dumps(newBeacon.value()), 200