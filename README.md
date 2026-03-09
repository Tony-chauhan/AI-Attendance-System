# 👁️ AI-Attendance-System

An automated, real-time attendance tracking system powered by facial recognition and computer vision. This project eliminates the need for manual roll calls by identifying individuals through a camera feed and automatically logging their presence in a secure database.

## 🚀 Features

* **Real-Time Facial Recognition:** Detects and identifies faces accurately using live video feeds.
* **Anti-Spoofing Capabilities:** (Optional/Planned) Liveness detection to prevent spoofing via photos or videos.
* **Web Dashboard:** An intuitive frontend interface for administrators to view attendance records, manage users, and export data.
* **Automated Reporting:** Generates daily, weekly, and monthly attendance reports in CSV/PDF formats.
* **Scalable Database:** Efficiently stores user encodings and timestamped attendance logs.

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (React / Vanilla JS)
* **Backend:** Python (Flask / FastAPI / Django) or Node.js
* **Computer Vision / AI:** OpenCV, `face_recognition` library, Dlib
* **Database:** PostgreSQL / MongoDB / MySQL

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
* Python 3.8+ or Node.js (depending on your backend choice)
* A working webcam or IP camera stream
* CMake (required for building Dlib)

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/AI-Attendance-System.git](https://github.com/your-username/AI-Attendance-System.git)
   cd AI-Attendance-System

```

2. **Set up a virtual environment (Python):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Initialize the Database:**
```bash
python manage.py migrate # If using Django
# OR run your specific database creation scripts

```



## 💻 Usage

1. **Register Users:** Navigate to the `/register` endpoint or use the admin dashboard to upload clear images of the individuals. The system will extract and store their facial encodings.
2. **Start the Recognition Engine:**
```bash
python run_camera.py

```


3. **View Attendance:** Open the web dashboard at `http://localhost:5000` to view the live attendance logs being populated.

## 🚧 Challenges & Known Limitations

* **Lighting Sensitivity:** Detection accuracy may drop in severely backlit or low-light environments.
* **Hardware Requirements:** Continuous video processing is CPU/GPU intensive.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://www.google.com/search?q=link-to-issues).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```
