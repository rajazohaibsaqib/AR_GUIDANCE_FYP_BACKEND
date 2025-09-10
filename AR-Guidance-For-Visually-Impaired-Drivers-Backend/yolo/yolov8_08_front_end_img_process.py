import cv2
import numpy as np
from easyocr import Reader
from ultralytics import YOLO
import os

# Global variables to hold loaded models
model = None
reader = None


def load_models():
    global model, reader

    # Load YOLO model
    script_dir = os.path.dirname(__file__)
    model_path = os.path.join(script_dir, 'best_epoch29_new.pt')
    model = YOLO(model_path)

    # Load EasyOCR reader
    reader = Reader(['en'], gpu=False)

    # Warm up models with a dummy inference
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    model.predict(dummy_image)
    reader.readtext(dummy_image)

    print("Models loaded and warmed up")


know_width_cls = {
    "laptop": 0.3302,
    "car": 1.7,
    "bike": 0.7,
    "truck": 2.4,
    "bus": 2.5,
    "unknown": 0
}

def letterbox(img, new_shape=(640, 640), color=(114, 114, 114)):
    shape = img.shape[:2]  # current shape [height, width]
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
    dw = new_shape[1] - new_unpad[0]  # width padding
    dh = new_shape[0] - new_unpad[1]  # height padding
    dw /= 2
    dh /= 2

    # Resize image
    img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

    # Add border (padding)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    return img


def detected_objects_from_front_end(image):
    global model, reader
    # cv2.imshow("recv", image)
    # cv2.waitKey(0)
    matrix = np.load('./calibration_matrix/camera_matrix.npy')
    focal_length_pixels = matrix[0, 0]
    detected_objects_list = []
    image = letterbox(image, (640, 640))  # resize correctly
    image = cv2.convertScaleAbs(image, alpha=1.2, beta=10)  # enhance contrast/brightness
    results = model(image)
    # cv2.imshow("after preprocess",image)
    # cv2.waitKey(0)
    if results and results[0] and results[0].boxes:
        for result in results[0].boxes:
            conf = result.conf[0]
            if conf >= 0.5:
                box = result.xyxy[0]
                cls = int(result.cls[0])
                x1, y1, x2, y2 = map(int, box)
                distance = 0

                # Calculate distance (existing logic remains)
                if model.names.get(cls, "unknown") in ["car", "bus", "truck", "bike", "unknown"]:
                    known_width = know_width_cls[model.names.get(cls, "unknown")]
                    perceived_width = x2 - x1
                    distance = (known_width * focal_length_pixels) / perceived_width

                # ============ MODIFIED OCR SECTION ============
                text = ""
                cls_name = model.names.get(cls, "unknown")
                if cls_name in ["textsignboard", "speed"]:
                    roi = image[y1:y2, x1:x2]

                    # Skip processing if ROI is too small
                    if roi.size > 0 and roi.shape[0] >= 5 and roi.shape[1] >= 5:
                        # Convert to grayscale (crucial for OCR accuracy)
                        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                        # Get OCR results with confidence details
                        ocr_results = reader.readtext(roi_gray, detail=1)

                        # Filter results by confidence threshold (0.3)
                        valid_texts = [
                            res[1] for res in ocr_results
                            if len(res) >= 3 and res[2] > 0.3
                        ]
                        text = " ".join(valid_texts)
                # ============ END MODIFICATIONS ============

                detected_objects_list.append({
                    'detected_object': cls_name,
                    'distance': distance,
                    'text': text
                })

                # Draw bounding box (existing logic remains)
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(image, f'{cls_name} {distance:.2f} m',
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return image, detected_objects_list