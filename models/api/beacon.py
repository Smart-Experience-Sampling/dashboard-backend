from models.db.beacon import Beacon as DbBeacon

class Beacon:
    id: str
    uid: str

    def fromDb(dbBeacon: DbBeacon):
        beacon = Beacon()
        beacon.id = dbBeacon.id
        beacon.uid = dbBeacon.uid

        return beacon