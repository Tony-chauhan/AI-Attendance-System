import cv2
import face_recognition
import numpy as np
import os

class VideoCamera(object):
    def __init__(self):
        # Open default camera. 0 is the laptop webcam
        self.video = cv2.VideoCapture(0)
        self.known_face_encodings = []
        self.known_face_names = []
        
        # Load sample pictures and learn how to recognize them.
        dataset_path = 'dataset'
        if os.path.exists(dataset_path):
            for file in os.listdir(dataset_path):
                if file.endswith(('jpg', 'png', 'jpeg')):
                    name = os.path.splitext(file)[0]
                    img_path = os.path.join(dataset_path, file)
                    image = face_recognition.load_image_file(img_path)
                    try:
                        encoding = face_recognition.face_encodings(image)[0]
                        self.known_face_encodings.append(encoding)
                        self.known_face_names.append(name.capitalize())
                    except IndexError:
                        print(f"Warning: No face found in {file}")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return None, []
            
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = []
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                # Use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

            face_names.append(name)

        # Draw rects
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            # Draw a label with a name below the face
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes(), [n for n in set(face_names) if n != "Unknown"]
