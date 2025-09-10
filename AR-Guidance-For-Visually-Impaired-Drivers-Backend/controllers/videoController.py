from flask import request, jsonify
from models import User
from yolo.yolov8_08_front_end_img_process import detected_objects_from_front_end
from PIL import Image
import cv2
import numpy as np
from database import Session
from datetime import datetime
from models.UserLog import UserLog
import os

def process_video():
    try:
        session = Session()
        PROCESSED_IMAGES_DIR = "detected_images"
        if not os.path.exists(PROCESSED_IMAGES_DIR):
            os.makedirs(PROCESSED_IMAGES_DIR)

        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        video = request.files['file']
        user_id = int(request.form['user_id'])
        camera_mode = int(request.form['camera_mode'])

        video_filename = f"uploaded_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
        video_path = os.path.join("uploaded_videos", video_filename)
        if not os.path.exists("uploaded_videos"):
            os.makedirs("uploaded_videos")
        video.save(video_path)

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        interval = int(fps * 2)  # every 2 seconds

        frame_idx = 0
        all_detections = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % interval == 0:
                processed_image, detected_data = detected_objects_from_front_end(frame)

                if detected_data:
                    processed_image_filename = f"detected_image_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.jpg"
                    processed_image_path = os.path.join(PROCESSED_IMAGES_DIR, processed_image_filename)
                    cv2.imwrite(processed_image_path, processed_image)

                    for obj in detected_data:
                        alert = obj["text"] if obj["detected_object"] in ["textsignboard", "speed"] else (
                            "Stop" if obj["detected_object"] == "red" else "Detected an object"
                        )

                        user_log = UserLog(
                            user_id=user_id,
                            detected_object=obj['detected_object'],
                            alert=alert,
                            distance=obj['distance'],
                            date=datetime.now().date(),
                            time=datetime.now().time(),
                            img_path=processed_image_path,
                            camera_mode=camera_mode,
                            islatest=True
                        )
                        session.add(user_log)

                    all_detections.append({
                        "frame": frame_idx,
                        "detected_objects": detected_data,
                        "processed_image_url": f'http://127.0.0.1:5000/detected_images/{processed_image_filename}',
                        "camera_mode": camera_mode
                    })

            frame_idx += 1

        session.commit()
        cap.release()
        session.close()

        return jsonify({
            "message": "Video processed successfully!",
            "detections": all_detections
        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500
