from util.session import Session
from models.db.beacon import Beacon
from models.db.clickBeaconConnections import ClickBeaconConnection as CBC


def getBeaconByUid(uid):
    session = Session()
    return session.query(Beacon).filter(Beacon.uid == uid).first()

def getBeacon(id):
    session = Session()
    return session.query(Beacon).filter(Beacon.id == id).first()

def getBeaconIdsByClickId(click_id):
    session = Session()
    beaconClicks = session.query(CBC).filter(CBC.click_id == click_id)
    beaconIds = []
    for beaconClick in beaconClicks:
        beaconIds.append(beaconClick.beacon_id)

    return beaconIds

def getBeaconsByClickId(click_id):
    session = Session()
    beaconClicks = session.query(CBC).filter(CBC.click_id == click_id)
    beaconIds = []
    for beaconClick in beaconClicks:
        beaconIds.append({
            "beacon": session.query(Beacon).filter(Beacon.id == beaconClick.beacon_id).first(),
            "distance": beaconClick.distance})

    return beaconIds