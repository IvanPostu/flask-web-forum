import face_recognition


class FacesNotFoundException(Exception):
    pass


def compare_faces_from_imagefiles(filepath_a: str, filepath_b: str):
    face_A = face_recognition.load_image_file(filepath_a)
    face_A_encodings = face_recognition.face_encodings(face_A)
    if len(face_A_encodings) == 0:
        raise FacesNotFoundException()
    face_A_encodings = face_A_encodings[0]

    face_B = face_recognition.load_image_file(filepath_b)
    face_B_encodings = face_recognition.face_encodings(face_B)
    if len(face_B_encodings) == 0:
        raise FacesNotFoundException()
    face_B_encodings = face_B_encodings[0]

    matches = face_recognition.compare_faces(
        [face_A_encodings], face_B_encodings)

    return matches[0]
