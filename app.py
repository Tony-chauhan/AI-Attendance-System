from flask import Flask, render_template, Response, request, jsonify
import cv2
import sqlite3
import datetime
import os
from camera import VideoCamera

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame, names = camera.get_frame()
        # Log attendance for names detected
        if names:
            conn = sqlite3.connect('attendance.db')
            cursor = conn.cursor()
            for name in names:
                # Check if already logged in the last hour to prevent spamming
                cursor.execute('''
                    SELECT * FROM attendance 
                    WHERE name=? AND timestamp >= datetime('now', '-1 hour')
                ''', (name,))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO attendance (user_id, name) VALUES (?, ?)
                    ''', (name.lower(), name))
            conn.commit()
            conn.close()
            
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/attendance')
def get_attendance():
    """API for the dashboard to fetch attendance records."""
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, timestamp FROM attendance ORDER BY timestamp DESC LIMIT 20')
    records = [{'name': row[0], 'timestamp': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
