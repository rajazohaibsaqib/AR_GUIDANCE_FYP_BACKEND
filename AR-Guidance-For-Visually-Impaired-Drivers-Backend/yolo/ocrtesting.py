import cv2
import numpy as np
from ultralytics import YOLO
import easyocr
from collections import defaultdict


# Initialize YOLOv8 model
def load_yolov8_model(model_path='best_5.pt'):
    """
    Load YOLOv8 model from the specified path.
    You should train or download a model specifically for text signboard detection.
    """
    model = YOLO(model_path)
    return model


# Initialize EasyOCR reader
def initialize_easyocr(languages=['en']):
    """
    Initialize EasyOCR reader with specified languages.
    Add more languages if needed for your use case.
    """
    reader = easyocr.Reader(languages)
    return reader


# Process video for text signboard detection and recognition
def process_video(video_path, output_path, yolo_model, ocr_reader, confidence_threshold=0.5):
    """
    Process video to detect text signboards and recognize text using YOLOv8 and EasyOCR.

    Args:
        video_path: Path to input video file
        output_path: Path to save output video
        yolo_model: Loaded YOLOv8 model
        ocr_reader: Initialized EasyOCR reader
        confidence_threshold: Minimum confidence for detection
    """
    # Open video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Track text across frames
    text_tracker = defaultdict(lambda: {'count': 0, 'text': ''})
    track_id = 0

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        print(f"Processing frame {frame_count}/{total_frames}")

        # Run YOLOv8 inference
        results = yolo_model(frame, conf=confidence_threshold)

        # Process detections
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)

            for box, conf, cls_id in zip(boxes, confidences, class_ids):
                x1, y1, x2, y2 = map(int, box)

                # Extract ROI (Region of Interest)
                roi = frame[y1:y2, x1:x2]

                # Skip if ROI is too small
                if roi.size == 0:
                    continue

                # Convert ROI to grayscale for better OCR (optional)
                roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                # Use EasyOCR to recognize text
                ocr_results = ocr_reader.readtext(roi_gray)

                # Process OCR results
                detected_text = ' '.join(
                    [res[1] for res in ocr_results if res[2] > 0.3])  # confidence threshold for OCR

                if detected_text:
                    # Assign tracking ID (simple approach - in production use proper tracking)
                    track_id += 1

                    # Draw bounding box and text
                    color = (0, 255, 0)  # green
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                    # Put class label and confidence
                    label = f"Signboard: {conf:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    # Put detected text
                    cv2.putText(frame, detected_text, (x1, y2 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Write frame to output video
        out.write(frame)

        # Display (optional)
        cv2.imshow('Text Signboard Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Processing completed.")


if __name__ == "__main__":
    # Load models
    print("Loading YOLOv8 model...")
    yolo_model = load_yolov8_model('best_5.pt')  # Replace with your trained model

    print("Initializing EasyOCR...")
    ocr_reader = initialize_easyocr(languages=['en'])  # Add more languages if needed

    # Process video
    input_video = r'C:\Users\works\Desktop\test3.mp4 '
    output_video = 'output_video.mp4'

    print(f"Processing video: {input_video}")
    process_video(input_video, output_video, yolo_model, ocr_reader)

    print(f"Output saved to: {output_video}")