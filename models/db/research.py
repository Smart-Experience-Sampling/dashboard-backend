from sqlalchemy import Column, String, DateTime, func
from util.generateUuid import generateUuid
from util.setup import Base
from datetime import datetime

class Research(Base):
    __tablename__ = "research"
    id = Column("id", String(36), primary_key=True)
    question = Column("question", String(255), nullable=False)
    created_time = Column("created_time", DateTime(timezone=True), default=func.now())
    start_time = Column("start_time", DateTime(timezone=True), nullable=False)
    end_time = Column("end_time", DateTime(timezone=True), nullable=False)

    def create(id: String, question: String, created_time: datetime, start_time: datetime, end_time: datetime):
        research = Research()
        research.id =id
        research.question = question
        research.created_time = created_time
        research.start_time = start_time
        research.end_time = end_time
        return research

    def new(question: String, start_time: datetime, end_time: datetime):

        research = Research.create(generateUuid(), question, datetime.now(), start_time, end_time)
        return research

    def value(self):
        return {
            "id": self.id if self.id else "00000000-0000-0000-0000-000000000000",
            "question": self.question if self.question else "",
            "created_time": datetime.isoformat(self.created_time) if self.created_time else "",
            "start_time": datetime.isoformat(self.start_time) if self.start_time else "",
            "end_time": datetime.isoformat(self.end_time) if self.start_time else ""
        }