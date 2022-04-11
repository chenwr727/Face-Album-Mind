from pydantic import BaseModel


class GroupBase(BaseModel):
    group_name: str
    det_threshold: float
    rec_threshold: float
    pitch_threshold: float
    yaw_threshold: float
    roll_threshold: float


class PictureBase(BaseModel):
    picture_name: str
    group_id: int


class FaceBase(BaseModel):
    face_index: int
    det_score: float
    pitch: float
    yaw: float
    roll: float
    bbox: bytes
    embedding: bytes
    picture_id: int


class LabelBase(BaseModel):
    label_name: str
    group_id: int


class FaceLabelBase(BaseModel):
    face_id: int
    label_id: int
