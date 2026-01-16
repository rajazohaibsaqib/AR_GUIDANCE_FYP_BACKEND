# AR Guidance For Visually Impaired Drivers

Welcome to the **Backend Repository** for the "AR Guidance for Partially Visually Impaired Drivers" project. This backend powers real-time processing and data management for an innovative application designed to assist drivers with partial visual impairments—specifically **peripheral vision issues**, **distance vision problems**, and **color blindness**. Using advanced computer vision and OCR, it delivers tailored guidance through object detection, text extraction, and voice alert generation.

## Project Overview

The backend drives the AR Guidance system by processing real-time data from the frontend (built with React Native) to provide actionable assistance. It employs **YOLOv8** for detecting objects on the road (e.g., vehicles, traffic signs) and **EasyOCR** for extracting text (e.g., road signs, speed limits), which are then transformed into AR overlays and voice alerts. This enhances safety and accessibility for visually impaired drivers.

### Key Features
- **Real-Time Object Detection**: Powered by YOLOv8, identifies road objects like vehicles and traffic signs with high accuracy.
- **Text Extraction**: Utilizes EasyOCR to read and interpret text from road signs, speed limits, and other visual cues.
- **User Data Management**: Stores and processes user profiles, including their specific visual impairments, in a MySQL database.
- **Real-Time Processing**: Delivers fast and reliable data to the frontend for AR HUD displays and voice alerts.
- **API Integration**: Exposes Flask-based endpoints for the frontend to fetch detection results, text data, and alerts.

## Tech Stack
- **Python**: Core language for backend logic and computer vision tasks.
- **YOLOv8**: State-of-the-art model for real-time object detection.
- **EasyOCR**: Lightweight OCR tool for extracting text from images.
- **Flask**: Lightweight web framework for building the API server.
- **SQLAlchemy**: ORM for interacting with the MySQL database.
- **MySQL**: Relational database for storing user data and configurations.

## How It Works
1. **User Authentication**: Validates user credentials from the frontend and retrieves their impairment profile from MySQL.
2. **Real-Time Input**: Receives live video/image feeds from the frontend (e.g., via camera stream).
3. **Object Detection**: YOLOv8 processes the feed to detect and classify objects like vehicles and traffic signs in real-time.
4. **Text Extraction**: EasyOCR extracts readable text from detected signs or objects.
5. **Data Processing**: Combines detection and text data, tailoring it to the user’s impairment (e.g., emphasizing audio for color blindness).
6. **Response Delivery**: Sends processed data (objects, text, alerts) back to the frontend via Flask API for AR rendering and voice output.

## Installation & Setup
To set up the backend locally:
1. Clone this repository:
   ```bash
   git clone https://github.com/rajazohaibsaqib/AR_GUIDANCE_FYP_BACKEND.git
   ```
2. Navigate to the project directory:
   ```bash
   cd your-backend-repo-name
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install core dependencies:
   ```bash
   pip install requirements.txt
   ```
5. Configure the MySQL database:
   - Set up a MySQL database (e.g., via phpMyAdmin or CLI):
     ```sql
     CREATE DATABASE ar_guidance_db;
     ```
   - Update the SQLAlchemy URI in your configuration file (e.g., `config.py`):
     ```python
     DATABASE_URI = "mysql+pymysql://yourusername:yourpassword@localhost:3306/ar_guidance_db"
     ```
6. Start the Flask server:
   ```bash
   python app.py
   ```


## Frontend Repository
This backend pairs with the frontend, built in FLutter Dart. Check it out here:  
[**Frontend Repository Link**](https://github.com/rajazohaibsaqib/AR_GUIDANCE_FYP.git)

## Future Enhancements
- Optimize YOLOv8 for faster inference on mobile devices.
- Add support for multilingual text extraction and voice alerts.
- Integrate with external APIs (e.g., traffic data) for richer guidance.

## Why This Project Matters
By powering real-time object detection and text extraction, this backend enables the AR Guidance system to deliver actionable insights to partially visually impaired drivers. It bridges advanced AI with accessibility, promoting safer and more independent driving experiences.

## License
This project is licensed under the [MIT License](LICENSE) – feel free to use, modify, and distribute it as needed.

---

### Notes
- **Database Credentials**: Replace `yourusername` and `yourpassword` in the MySQL URI with your actual MySQL credentials.



