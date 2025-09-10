import cv2
import numpy as np
from ultralytics import YOLO
import easyocr
import os


# Initialize YOLOv8 model
def load_yolov8_model(model_path='best_5.pt'):
    model = YOLO(model_path)
    return model


# Initialize EasyOCR reader
def initialize_easyocr(languages=['en']):
    reader = easyocr.Reader(languages)
    return reader


# Process image for text signboard detection and recognition
def process_image(image_path, output_path, yolo_model, ocr_reader, confidence_threshold=0.5):
    """
    Process image to detect text signboards and recognize text using YOLOv8 and EasyOCR.

    Args:
        image_path: Path to input image file
        output_path: Path to save output image
        yolo_model: Loaded YOLOv8 model
        ocr_reader: Initialized EasyOCR reader
        confidence_threshold: Minimum confidence for detection
    """
    # Read image
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image at {image_path}")
        return

    # Create copy of original for drawing
    output_frame = frame.copy()

    # Initialize list to store text results
    text_results = []

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
            if roi.size == 0 or roi.shape[0] < 5 or roi.shape[1] < 5:
                continue

            # Convert ROI to grayscale for better OCR
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # Use EasyOCR to recognize text
            ocr_results = ocr_reader.readtext(roi_gray)

            # Process OCR results
            detected_text = ' '.join(
                [res[1] for res in ocr_results if res[2] > 0.3])  # confidence threshold for OCR

            # Store result if text detected
            if detected_text:
                # Add to results list
                result_entry = {
                    "bbox": (x1, y1, x2, y2),
                    "detection_confidence": float(conf),
                    "detected_text": detected_text,
                    "ocr_details": [(res[1], float(res[2])) for res in ocr_results if res[2] > 0.3]
                }
                text_results.append(result_entry)

                # Draw bounding box and text
                color = (0, 255, 0)  # green
                cv2.rectangle(output_frame, (x1, y1), (x2, y2), color, 2)

                # Put class label and confidence
                label = f"Signboard: {conf:.2f}"
                cv2.putText(output_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Put detected text
                cv2.putText(output_frame, detected_text, (x1, y2 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Save output image
#    cv2.imwrite(output_path, output_frame)
    print(f"Output image saved to: {output_path}")

    # Display text results on console
    print("\nText Detection Results:")
    if not text_results:
        print("No text signboards detected")
    else:
        for i, result in enumerate(text_results, 1):
            x1, y1, x2, y2 = result["bbox"]
            print(f"\nSignboard {i}:")
            print(f"  Bounding Box: ({x1}, {y1}) to ({x2}, {y2})")
            print(f"  Detection Confidence: {result['detection_confidence']:.4f}")
            print(f"  Detected Text: '{result['detected_text']}'")

            if result["ocr_details"]:
                print("  OCR Details:")
                for j, (text, conf) in enumerate(result["ocr_details"], 1):
                    print(f"    Line {j}: '{text}' (confidence: {conf:.4f})")
            else:
                print("  No OCR details available")

    print("\nProcessing complete")

    # Display result
    cv2.imshow('Text Signboard Detection', output_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Load models
    print("Loading YOLOv8 model...")
    yolo_model = load_yolov8_model('best_5.pt')  # Replace with your trained model

    print("Initializing EasyOCR...")
    ocr_reader = initialize_easyocr(languages=['en'])  # Add more languages if needed

    # Process image
    input_image = r'C:\Users\works\Desktop\Test_ocr\new (3).jpeg'  # Update with your image path
    output_image = 'result0.PNG'  # Output filename

    print(f"Processing image: {input_image}")
    process_image(input_image, output_image, yolo_model, ocr_reader)