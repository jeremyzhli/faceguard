import cv2
import face_recognition
import os
import numpy
import smtplib, ssl
from datetime import datetime

def register_faces():
    registered_faces = []
    registered_names = []

    user_email = input("Enter your email: ")
    
    directory = r"C:\Users\Jermy\Documents\Facialrec\face_references"
    for image in os.listdir(directory):
        load_img = face_recognition.load_image_file(f"{directory}/{image}")
        encode_img = face_recognition.face_encodings(load_img)[0]

        registered_faces.append(encode_img)
        registered_names.append(image.split(".")[0])

    return registered_faces, registered_names, user_email

def display_frame(frame, face_locations, names):
    for (top, right, bottom, left), name in zip(face_locations, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (255, 0, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 5, bottom - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Video Frame", frame)

def recognise(registered_faces, registered_names, user_email):
    capture_obj = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    face_locations = []
    face_encodings = []
    delay = 0
    alert_delay = 0

    while True:
        ret, frame = capture_obj.read()
        
        if delay < 3:
            delay += 1
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        names = []
        for face in face_encodings:
            matches = face_recognition.compare_faces(registered_faces, face)
            
            face_confidence = face_recognition.face_distance(registered_faces, face)
            match_index = numpy.argmin(face_confidence)
            if matches[match_index]:
                names.append(registered_names[match_index])
            else:
                alert_delay += 1
                names.append("Face not recognised")

        if alert_delay > 30:
            email_alert(user_email)
            alert_delay = 0

        delay = 0
        display_frame(frame, face_locations, names)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

def email_alert(user_email):
    context = ssl.create_default_context()
    sender_email = "facelogalerts@gmail.com"
    password = "iowj wkfc kpip sewp"
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M")
    message = f"""\
Subject: FaceLog Security Alert

        
One or more unauthorised faces have been detected near your device at {time_now}.
Please take appropriate action to secure your device."""

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, user_email, message)

if __name__ == "__main__":
    registered_faces, registered_names, user_email = register_faces()
    recognise(registered_faces, registered_names, user_email)