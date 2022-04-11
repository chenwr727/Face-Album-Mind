from sqlalchemy import (BLOB, FLOAT, VARCHAR, Column, DateTime, ForeignKey,
                        Integer)
# from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class Group(Base):
    __tablename__ = "t_group"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    group_name = Column(VARCHAR(100), index=True)
    det_threshold = Column(FLOAT)
    rec_threshold = Column(FLOAT)
    pitch_threshold = Column(FLOAT)
    yaw_threshold = Column(FLOAT)
    roll_threshold = Column(FLOAT)
    create_time = Column(DateTime(timezone=True), server_default=func.now())

    # pictures = relationship("Picture", back_populates="group")
    # labels = relationship("Label", back_populates="group")


class Picture(Base):
    __tablename__ = "t_picture"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    picture_name = Column(VARCHAR(100))
    group_id = Column(Integer, ForeignKey("t_group.id"))
    create_time = Column(DateTime(timezone=True), server_default=func.now())

    # group = relationship("Group", back_populates="pictures")
    # faces = relationship("Face", back_populates="picture")


class Face(Base):
    __tablename__ = "t_face"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    face_index = Column(Integer)
    det_score = Column(FLOAT)
    pitch = Column(FLOAT)
    yaw = Column(FLOAT)
    roll = Column(FLOAT)
    bbox = Column(BLOB)
    embedding = Column(BLOB)
    picture_id = Column(Integer, ForeignKey("t_picture.id"))
    create_time = Column(DateTime(timezone=True), server_default=func.now())

    # picture = relationship("Picture", back_populates="faces")
    # label = relationship("Face_Label", back_populates="face")


class Label(Base):
    __tablename__ = "t_label"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    label_name = Column(VARCHAR(100))
    group_id = Column(Integer, ForeignKey("t_group.id"))
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # group = relationship("Group", back_populates="labels")
    # face = relationship("Face_Label", back_populates="label")


class Face_Label(Base):
    __tablename__ = "t_face_label"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    face_id = Column(Integer, ForeignKey("t_face.id"))
    label_id = Column(Integer, ForeignKey("t_label.id"))
    create_time = Column(DateTime(timezone=True), server_default=func.now())

    # face = relationship("Face", back_populates="label")
    # label = relationship("Label", back_populates="face")
