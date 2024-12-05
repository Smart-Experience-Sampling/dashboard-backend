from util.setup import Base
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, func, Integer
from util.generateUuid import generateUuid

class Beacon(Base):
    __tablename__ = "beacon"
    id = Column("id", String(36), primary_key=True)
    uid = Column("uid", Integer)

    def create(id: String, uid: Integer):
        self = Beacon()
        self.id = id
        self.uid = uid
        return self

    def new(uid: Integer):
        beacon = Beacon.create(generateUuid(), uid)
        return beacon

    def value(self):
        return {
            "id": self.id,
            "uid": self.uid
        }