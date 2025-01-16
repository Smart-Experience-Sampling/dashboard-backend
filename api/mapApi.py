from models.api.beacon import Beacon as ApiBeacon
from models.api.click import Click as ApiClick
from models.api.clickBeacon import ClickBeacon

MAX_BEACON_COUNT = 50

def generateIndecesArray(beaconAmount: int):
    beaconAmount = min(beaconAmount, MAX_BEACON_COUNT)
    if beaconAmount < 3:
        return []
    arr = []
    for i in range(beaconAmount):
        if i < 2:
            continue
        for j in range(i):
            if j < 1:
                continue
            for k in range(j):
                arr.append([k,j,i])
    print(arr)
    return arr


def displayMap(beacons: ApiBeacon, clicks: list[ApiClick]):
    for click in clicks:
        clickBeacons = click.click_beacons
        clickBeacons.sort(returnOrder)

        if len(clickBeacons) < 3:
            continue

        for set in generateIndecesArray(len(clickBeacons)):
            beacon1 = clickBeacons[set[0]]
            beacon2 = clickBeacons[set[1]]
            beacon3 = clickBeacons[set[2]]

            A = -2 * beacon1.beacon.x + 2 * beacon2.beacon.x
            B = -2 * beacon1.beacon.y + 2 * beacon2.beacon.y
            C = beacon1.distance ** 2 - beacon2.distance ** 2 - beacon1.beacon.x ** 2 + beacon2.beacon.x ** 2 - beacon1.beacon.y ** 2 + beacon2.beacon.y ** 2

            D = -2 * beacon2.beacon.x + 2 * beacon3.beacon.x
            E = -2 * beacon2.beacon.y + 2 * beacon3.beacon.y
            F = beacon2.distance ** 2 - beacon3.distance ** 2 - beacon2.beacon.x ** 2 + beacon3.beacon.x ** 2 - beacon2.beacon.y ** 2 + beacon3.beacon.y ** 2
            
            clickX = (C * E - F * B) / (E * A - D * B)
            clickY = (C * D - A * F) / (B * D - A * E)




def returnOrder(beacon: ClickBeacon):
    return beacon.distance
