from flask import Flask, render_template, Response, request, redirect, session
import cv2
import sqlite3
import time
import os

from emotion_detector import detect_emotion
from task_recommender import recommend_task

app = Flask(__name__)
app.secret_key = "secret123"

camera = cv2.VideoCapture(0)

emotion = "Neutral"
last_detection_time = 0

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def init_db():

    if not os.path.exists("database"):
        os.makedirs("database")

    conn = sqlite3.connect("database/users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

def gen_frames():

    global emotion, last_detection_time

    while True:

        success, frame = camera.read()

        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        current_time = time.time()

        for (x,y,w,h) in faces:

            face = frame[y:y+h, x:x+w]

            if current_time - last_detection_time > 5:

                face_small = cv2.resize(face,(224,224))

                emotion = detect_emotion(face_small)

                last_detection_time = current_time

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            cv2.putText(frame, emotion, (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database/users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username,password))

    user = c.fetchone()

    conn.close()

    if user:
        session["user"]=username
        return redirect("/dashboard")

    return "Invalid Login"

@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database/users.db")
    c = conn.cursor()

    c.execute("INSERT INTO users(username,password) VALUES (?,?)",
              (username,password))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html")

@app.route("/video")
def video():

    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/task")
def task():

    task = recommend_task(emotion)

    return {"task":task}

@app.route("/logout")
def logout():

    session.pop("user",None)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)