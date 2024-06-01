from sqlalchemy import Column, Integer, String, ForeignKey, Date

from app.database import Base

class Studies(Base):
    __tablename__ = 'studies'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    file_hash = Column(String, nullable=False)
    mask_file_link = Column(String, nullable=False)
    study_date = Column(Date, nullable=False)