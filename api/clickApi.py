from datetime import datetime
from flask import Blueprint, request
from sqlalchemy import select
from functions.json import json

from util.flask import io

from util.session import Session
from models.db.click import Click as DbClick
from models.db.clickBeaconConnections import ClickBeaconConnection
from models.db.clicker import Clicker as DbClicker

from models.api.click import Click as ApiClick
from models.api.clicker import Clicker as ApiClicker
from models.api.beacon import Beacon as ApiBeacon

from functions.clickerFunctions import getClickerByUid
from functions.beaconFunctions import getBeaconByUid, getBeaconIdsByClickId, getBeacon, getBeaconsByClickId

from api.clickerApi import getClickerById

app = Blueprint("click", __name__)

@app.route("")
def getAll():
    session = Session()
    res = select(DbClick).order_by(DbClick.click_time)
    arr = []
    for click in session.scalars(res):
        tempClick: ApiClick = ApiClick.fromDb(click)
        tempClick.clicker = ApiClicker.fromDb(session.query(DbClicker).filter(DbClicker.id == click.clicker_id).first())
        beaconIds = getBeaconsByClickId(click.id)
        for dbBeacon in beaconIds:
            beaconArray = []
            beaconArray.append({
                "beacon": ApiBeacon.fromDb(dbBeacon["beacon"]),
                "distance": dbBeacon["distance"]})
            tempClick.click_beacons = beaconArray
            
        arr.append(tempClick.toJSON())
    session.close()
    return json(arr), 200

@app.route("", methods=["POST"])
def create():
    jsonData = request.get_json()
    print(jsonData)
    
    try:
        clicker_uid = jsonData["clicker_id"]
        click_time_string = jsonData["click_time"]
        beacons = jsonData["beacons"]
        click_time = datetime.fromisoformat(click_time_string)
    
    except KeyError:
        return "Model is invalid", 400
    
    except ValueError:
        return "Time is not in valid ISO format", 400
    
    clicker = getClickerByUid(clicker_uid)

    session = Session()
    click = DbClick.new(click_time, clicker.id)
    
    session.add(click)

    for uid, time in beacons.items():
        print(uid, time)
        beacon = getBeaconByUid(uid)
        clickBeaconConnection = ClickBeaconConnection.new(click.id, beacon.id, time)

        session.add(clickBeaconConnection)

    session.commit()

    res: ApiClick = ApiClick.fromDb(click)
    res.clicker = ApiClicker.fromDb(session.query(DbClicker).filter(DbClicker.id == click.clicker_id).first())
    beaconIds = getBeaconsByClickId(click.id)
    for dbBeacon in beaconIds:
        beaconArray = []
        beaconArray.append({
            "beacon": ApiBeacon.fromDb(dbBeacon["beacon"]),
            "distance": dbBeacon["distance"]})
        res.click_beacons = beaconArray

    io.emit('data', res.toJSON())
    session.close()


    return "", 200