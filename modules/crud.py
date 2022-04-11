import pickle

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas


def get_group_name(db: Session):
    return db.query(
        models.Group.group_name,
        models.Group.id,
        models.Group.det_threshold,
        models.Group.rec_threshold,
        models.Group.pitch_threshold,
        models.Group.yaw_threshold,
        models.Group.roll_threshold,
    ).all()


def get_id_by_group_name(db: Session, group_name: str):
    return (
        db.query(models.Group.id).filter(models.Group.group_name == group_name).first()
    )


def get_label_count_by_group_id(db: Session, group_id: int):
    return (
        db.query(func.count(models.Label.id))
        .filter(models.Label.group_id == group_id)
        .scalar()
    )


def get_picture_count_by_group_id(db: Session, group_id: int):
    return (
        db.query(func.count(models.Picture.id))
        .filter(models.Picture.group_id == group_id)
        .scalar()
    )


def get_face_count_by_group_id(db: Session, group_id: int, det_threshold: float):
    return (
        db.query(func.count(models.Face.id))
        .join(models.Picture)
        .filter(models.Picture.group_id == group_id)
        .scalar()
    )


def get_label_name_by_group_id(db: Session, group_id: int):
    return (
        db.query(models.Label.label_name)
        .filter(models.Label.group_id == group_id)
        .distinct()
        .order_by(models.Label.id)
        .all()
    )


def get_picture_name_by_group_id(db: Session, group_id: int):
    return (
        db.query(models.Picture.picture_name, models.Picture.id)
        .filter(models.Picture.group_id == group_id)
        .distinct()
        .order_by(models.Picture.id)
        .all()
    )


def get_label_id_by_group_id_label_name(db: Session, group_id: int, label_name: str):
    return (
        db.query(models.Label.id)
        .filter(
            (models.Label.group_id == group_id)
            & (models.Label.label_name == label_name)
        )
        .all()
    )


def get_picture_face_by_label_id(db: Session, label_id: int):
    return (
        db.query(
            models.Picture.id,
            models.Picture.picture_name,
            models.Face.det_score,
            models.Face.pitch,
            models.Face.yaw,
            models.Face.roll,
            models.Face.bbox,
        )
        .join(models.Face, models.Face_Label)
        .filter(models.Face_Label.label_id == label_id)
        .all()
    )


def get_picture_face_by_picture_id(db: Session, picture_id: int, det_threshold: float):
    return (
        db.query(
            models.Face.det_score,
            models.Face.pitch,
            models.Face.yaw,
            models.Face.roll,
            models.Face.bbox,
        )
        .join(models.Picture)
        .filter(
            (models.Picture.id == picture_id) & (models.Face.det_score >= det_threshold)
        )
        .all()
    )


def get_picture_face_by_group_id(db: Session, group_id: int):
    query = db.query(models.Picture.id, models.Picture.picture_name).filter(
        models.Picture.group_id == group_id
    )
    subquery = db.query(models.Face.picture_id).join(models.Face_Label)
    return query.filter(models.Picture.id.notin_(subquery)).all()


def get_embedding_label_by_group_id(db: Session, group_id: int):
    embeddings = []
    label_names = []
    label_ids = []
    rows = (
        db.query(
            models.Face.embedding, models.Face_Label.label_id, models.Label.label_name
        )
        .join(models.Picture, models.Face_Label, models.Label)
        .filter(models.Picture.group_id == group_id)
    )
    for row in rows:
        embedding, label_id, label_name = row
        embeddings.append(pickle.loads(embedding).tolist())
        label_names.append(label_name)
        label_ids.append(label_id)
    return embeddings, label_names, label_ids


def create_group(db: Session, group: schemas.GroupBase):
    db_group = models.Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group.id


def create_picture(db: Session, picture: schemas.PictureBase):
    db_picture = models.Picture(**picture.dict())
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    return db_picture.id


def create_face(db: Session, face: schemas.FaceBase):
    db_face = models.Face(**face.dict())
    db.add(db_face)
    db.commit()
    db.refresh(db_face)
    return db_face.id


def create_label(db: Session, label: schemas.LabelBase):
    db_label = models.Label(**label.dict())
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label.id


def create_face_label(db: Session, face_label: schemas.FaceLabelBase):
    db_face_label = models.Face_Label(**face_label.dict())
    db.add(db_face_label)
    db.commit()
    db.refresh(db_face_label)
    return db_face_label.id


def update_label_name_by_label_id(db: Session, label_id: int, label_name: str):
    db.query(models.Label).filter(models.Label.id == label_id).update(
        {"label_name": label_name}
    )
    db.commit()
    return None
