from sqlalchemy import Column, String, Float, ForeignKey, DateTime, func

from util.setup import Base
from util.generateUuid import generateUuid

from functions.beaconFunctions import getBeacon

class Location(Base):
    __tablename__ = "location"
    id = Column("id", String(36), primary_key=True)
    name = Column("name", String(255))
    parent_id = Column("parent_id", String(36))

    def create(id: String, name: String, parent_id: String | None):
        self = Location()
        self.id = id
        self.name = name
        self.parent_id = parent_id
        return self

    def new(name: String, parent_id: String | None):
        location = Location.create(generateUuid(), name, parent_id)
        print(location.id)
        print(location.name)
        print(location.parent_id)
        return location