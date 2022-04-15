import os
import pickle

import pandas as pd
import streamlit as st
from insightface.app import FaceAnalysis
from sklearn.neighbors import KNeighborsClassifier

from modules import crud, database, models, schemas
from utils.tools import (
    draw_image_with_boxes,
    read_image_bytes,
    read_image_file,
    save_image_bytes,
)

models.Base.metadata.create_all(bind=database.engine)
st.set_page_config(page_title="智能相册")


def main():
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox(
        "Choose the app mode", ["Show exists groups", "Add new group"]
    )
    if app_mode == "Show exists groups":
        st.sidebar.title("Select a group")
        rows = crud.get_group_name(db)
        group_dict = {}
        options = []
        for row in rows:
            options.append(row[0])
            group_dict[row[0]] = row[1:]
        group_name = st.sidebar.selectbox("Choose the group", options)
        if group_name:
            (
                group_id,
                det_threshold,
                rec_threshold,
                pitch_threshold,
                yaw_threshold,
                roll_threshold,
            ) = group_dict[group_name]
            st.sidebar.markdown(
                f"> det_threshold: `{det_threshold}`  \n  > rec_threshold: `{rec_threshold}`  \n  > pitch_threshold: `{pitch_threshold}`  \n  > yaw_threshold: `{yaw_threshold}`  \n  > roll_threshold: `{roll_threshold}`"
            )
            run_the_app(
                group_id,
                det_threshold,
                rec_threshold,
                pitch_threshold,
                yaw_threshold,
                roll_threshold,
            )
    elif app_mode == "Add new group":
        st.sidebar.title("Input a new group")
        (
            det_threshold,
            rec_threshold,
            pitch_threshold,
            yaw_threshold,
            roll_threshold,
        ) = object_detector_ui()
        group_name = st.sidebar.text_input(
            "group name",
            value=f"det{det_threshold}_rec{rec_threshold}_pitch{pitch_threshold}_yaw{yaw_threshold}_roll{roll_threshold}",
        )
        if st.sidebar.button("Add"):
            if group_name:
                rows = crud.get_id_by_group_name(db, group_name)
                if rows:
                    st.sidebar.error("Group exists")
                else:
                    group_base = schemas.GroupBase(
                        group_name=group_name,
                        det_threshold=det_threshold,
                        rec_threshold=rec_threshold,
                        pitch_threshold=pitch_threshold,
                        yaw_threshold=yaw_threshold,
                        roll_threshold=roll_threshold,
                    )
                    crud.create_group(db, group_base)
                    st.sidebar.success("Group added")


def object_detector_ui():
    st.sidebar.markdown("### Model Config")
    det_threshold = st.sidebar.slider("Detection threshold", 0.5, 1.0, 0.75, 0.01)
    rec_threshold = st.sidebar.slider("Recognition threshold", 0.0, 1.0, 0.6, 0.01)
    pitch_threshold = st.sidebar.slider("Pitch threshold", 0, 90, 30, 1)
    yaw_threshold = st.sidebar.slider("Yaw threshold", 0, 90, 30, 1)
    roll_threshold = st.sidebar.slider("Roll threshold", 0, 90, 30, 1)
    return det_threshold, rec_threshold, pitch_threshold, yaw_threshold, roll_threshold


def run_the_app(
    group_id,
    det_threshold,
    rec_threshold,
    pitch_threshold,
    yaw_threshold,
    roll_threshold,
):
    st.sidebar.markdown("# Upload")
    uploaded_files = st.sidebar.file_uploader(
        "Upload a jpg file", type=["jpg"], accept_multiple_files=True
    )
    if st.sidebar.button("Upload"):
        if uploaded_files:
            X, y, z = crud.get_embedding_label_by_group_id(db, group_id)
            n_uploaded_files = len(uploaded_files)
            status_text = st.sidebar.empty()
            progress_widget = st.sidebar.progress(0)
            for p, uploaded_file in enumerate(uploaded_files):
                bytes_data = uploaded_file.getvalue()
                image = read_image_bytes(bytes_data)
                if image is None:
                    continue
                picture_name = uploaded_file.name
                picture_base = schemas.PictureBase(
                    picture_name=picture_name, group_id=group_id
                )
                picture_id = crud.create_picture(db, picture_base)
                save_image_bytes(
                    os.path.join(DATA_PATH_ROOT, f"{picture_id}.jpg"), bytes_data
                )
                faces = app.get(image)
                if y:
                    neigh = KNeighborsClassifier(
                        n_neighbors=min(N_NEIGHBORS, len(y)), metric="cosine"
                    )
                    neigh.fit(X, y)
                else:
                    neigh = None
                for i, face in enumerate(faces):
                    if (
                        face.det_score >= det_threshold
                        and abs(face.pose[0]) <= pitch_threshold
                        and abs(face.pose[1]) <= yaw_threshold
                        and abs(face.pose[2]) <= roll_threshold
                    ):
                        face_base = schemas.FaceBase(
                            face_index=i,
                            det_score=float(face.det_score),
                            pitch=float(face.pose[0]),
                            yaw=float(face.pose[1]),
                            roll=float(face.pose[2]),
                            bbox=face.bbox.dumps(),
                            embedding=face.normed_embedding.dumps(),
                            picture_id=picture_id,
                        )
                        face_id = crud.create_face(db, face_base)
                        if neigh is not None:
                            neigh_dist, neigh_ind = neigh.kneighbors(
                                [face.normed_embedding.tolist()]
                            )
                            df = pd.DataFrame(
                                {
                                    "dist": neigh_dist[0],
                                    "label_name": [y[i] for i in neigh_ind[0]],
                                    "label_id": [z[i] for i in neigh_ind[0]],
                                }
                            )
                            df = df[df["dist"] <= 1 - rec_threshold]
                            if not df.empty:
                                label_name = df["label_name"].value_counts().index[0]
                                label_id = int(
                                    df.loc[df["label_name"] == label_name, "label_id"]
                                    .value_counts()
                                    .index[0]
                                )
                                face_label_base = schemas.FaceLabelBase(
                                    face_id=face_id,
                                    label_id=label_id,
                                )
                                crud.create_face_label(db, face_label_base)
                                X.append(face.normed_embedding.tolist())
                                y.append(label_name)
                                z.append(label_id)
                                continue
                        n_labels = crud.get_label_count_by_group_id(db, group_id)
                        label_name = "label_%03d" % (n_labels + 1)
                        label_base = schemas.LabelBase(
                            label_name=label_name, group_id=group_id
                        )
                        label_id = crud.create_label(db, label_base)
                        face_label_base = schemas.FaceLabelBase(
                            face_id=face_id,
                            label_id=label_id,
                        )
                        crud.create_face_label(db, face_label_base)
                        X.append(face.normed_embedding.tolist())
                        y.append(label_name)
                        z.append(label_id)
                progress_widget.progress((p + 1) / n_uploaded_files)
                status_text.text("%.0f%% Complete" % ((p + 1) * 100 / n_uploaded_files))
            # progress_widget.empty()
    show_cluster(group_id, det_threshold)


def show_cluster(group_id, det_threshold):
    st.subheader("Summary")
    n_pictures = crud.get_picture_count_by_group_id(db, group_id)
    n_faces = crud.get_face_count_by_group_id(db, group_id, det_threshold)
    lables = crud.get_label_name_by_group_id(db, group_id)
    st.markdown(
        f"> `{n_pictures}` pictures found.  \n  > `{n_faces}` faces found.  \n  > `{len(lables)}` labels found."
    )
    st.subheader("What to do")
    app_mode = st.selectbox("Choose what to show", ["Show labels", "Show pictures"])
    if app_mode == "Show labels":
        show_labels_mode(group_id, lables)
    elif app_mode == "Show pictures":
        show_pictures_mode(group_id, det_threshold)


def show_labels_mode(group_id, lables):
    def selectbox_change():
        st.session_state.label_id = label_dict[st.session_state.label_name] + 1

    st.subheader("Select a label")
    options = []
    label_dict = {}
    i = 0
    for i, row in enumerate(lables):
        options.append(row[0])
        label_dict[row[0]] = i
    not_label = "No one was found"
    label_dict[not_label] = i + 1
    options.append(not_label)
    col1, col2 = st.columns([3, 2])
    if "label_id" not in st.session_state:
        st.session_state["label_id"] = 1
    col2.number_input(
        "Choose the label id",
        min_value=1,
        max_value=len(options),
        step=1,
        key="label_id",
    )
    label_name = col1.selectbox(
        "Choose the label name",
        options,
        index=st.session_state.label_id - 1,
        key="label_name",
        on_change=selectbox_change,
    )
    rows = crud.get_label_id_by_group_id_label_name(db, group_id, label_name)
    options = []
    for row in rows:
        options.append(row[0])
    label_id = st.selectbox(f"{len(rows)} ids found.", options)
    if label_name != not_label:
        new_name = st.text_input("Rename label name")
        if st.button("Rename"):
            if new_name:
                crud.update_label_name_by_label_id(db, label_id, new_name)
                label_dict[new_name] = label_dict.pop(label_name)
                raise st._RerunException(st._RerunData(""))
        rows = crud.get_picture_face_by_label_id(db, label_id)
    else:
        rows = crud.get_picture_face_by_group_id(db, group_id)
    show_pictures(rows)


def show_pictures_mode(group_id, det_threshold):
    def selectbox_change():
        st.session_state.picture_id = picture_dict[st.session_state.picture_name] + 1

    st.subheader("Select a picture")
    rows = crud.get_picture_name_by_group_id(db, group_id)
    options = []
    picture_dict = {}
    picture2id = {}
    for i, row in enumerate(rows):
        options.append(row[0])
        picture_dict[row[0]] = i
        picture2id[row[0]] = row[1]
    col1, col2 = st.columns([3, 2])
    if "picture_id" not in st.session_state:
        st.session_state["picture_id"] = 1
    col2.number_input(
        "Choose the picture id",
        min_value=1,
        max_value=len(options),
        step=1,
        key="picture_id",
    )
    picture_name = col1.selectbox(
        "Choose the picture name",
        options,
        index=st.session_state.picture_id - 1,
        key="picture_name",
        on_change=selectbox_change,
    )
    picture_id = picture2id[picture_name]
    rows = crud.get_picture_face_by_picture_id(db, picture_id, det_threshold)
    n_rows = len(rows)
    st.markdown(f"detect `{n_rows}` faces.")
    image = read_image_file(os.path.join(DATA_PATH_ROOT, f"{picture_id}.jpg"))
    for row in rows:
        det_score, pitch, yaw, roll, bbox = row
        image = draw_image_with_boxes(
            image, pickle.loads(bbox).tolist(), det_score, pitch, yaw, roll
        )
    st.image(image, caption=picture_name)


def show_pictures(rows):
    st.subheader("Show pictures")
    n_rows = len(rows)
    st.markdown(f"Load `{n_rows}` pictures.")
    progress_widget = st.progress(0)
    for p, row in enumerate(rows):
        if len(row) == 7:
            picture_id, picture_name, det_score, pitch, yaw, roll, bbox = row
            image = draw_image_with_boxes(
                read_image_file(os.path.join(DATA_PATH_ROOT, f"{picture_id}.jpg")),
                pickle.loads(bbox).tolist(),
                det_score,
                pitch,
                yaw,
                roll,
            )
        else:
            picture_id, picture_name = row
            image = read_image_file(os.path.join(DATA_PATH_ROOT, f"{picture_id}.jpg"))
        st.markdown("* {}".format(picture_id))
        st.image(image, caption=picture_name)
        progress_widget.progress((p + 1) / n_rows)
    progress_widget.empty()


@st.experimental_singleton
def load_app():
    app = FaceAnalysis(allowed_modules=["landmark_3d_68", "detection", "recognition"])
    app.prepare(ctx_id=0, det_size=(640, 480))
    return app


@st.experimental_singleton
def init_connection():
    return database.SessionLocal()


DATA_PATH_ROOT = "./pictures"
N_NEIGHBORS = 5

app = load_app()
db = init_connection()

if not os.path.exists(DATA_PATH_ROOT):
    os.mkdir(DATA_PATH_ROOT)


if __name__ == "__main__":
    main()
