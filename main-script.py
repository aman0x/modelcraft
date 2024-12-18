import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from ultralytics import YOLO
from inference_sdk import InferenceHTTPClient


# =========================
# 1. Load Image for Detection
# =========================
def load_image(image_path):
    """Loads an image from a given path."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from {image_path}")
    return image


# =========================
# 2. Roboflow Inference Client
# =========================
def run_roboflow_detection(image, model_id, api_key):
    """
    Uses the Roboflow API to perform segmentation on the given image.
    """
    CLIENT = InferenceHTTPClient(
        api_url="https://outline.roboflow.com",
        api_key=api_key
    )

    try:
        result = CLIENT.infer(image, model_id=model_id)
        print("Roboflow detection successful.")
        return result
    except Exception as e:
        print(f"Error during Roboflow detection: {e}")
        return None


# =========================
# 3. YOLOv8 Detection
# =========================
def run_yolo_detection(image):
    """
    Uses YOLOv8 to detect objects in the image.
    """
    try:
        model = YOLO('yolov8n.pt')  # You can use 'best.pt' if you have a trained model
        results = model.predict(image, conf=0.25)  # Set confidence threshold
        print("YOLOv8 detection successful.")
        return results
    except Exception as e:
        print(f"Error during YOLOv8 detection: {e}")
        return None


# =========================
# 4. Visualize Detections
# =========================
def visualize_results(image, yolo_results=None, roboflow_results=None):
    """
    Visualizes both YOLOv8 and Roboflow detection results.
    """
    if roboflow_results:
        # Draw bounding boxes from Roboflow result
        for prediction in roboflow_results['predictions']:
            x = int(prediction['x'] - prediction['width'] / 2)
            y = int(prediction['y'] - prediction['height'] / 2)
            w = int(prediction['width'])
            h = int(prediction['height'])
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green for Roboflow

    if yolo_results:
        # Draw YOLO results on the image
        yolo_results[0].plot()

    # Convert BGR to RGB for plt
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(12, 8))
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.title("Detections from Roboflow and YOLOv8")
    plt.show()


# =========================
# 5. Save Results to CSV
# =========================
def save_detections_to_csv(detections, output_csv='detections.csv'):
    """
    Saves the detected objects (class, confidence, and bounding box) to a CSV file.
    """
    try:
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Class', 'Confidence', 'X1', 'Y1', 'X2', 'Y2'])  # CSV headers
            for result in detections:
                x1, y1, x2, y2 = result['box']
                writer.writerow([result['class'], result['confidence'], x1, y1, x2, y2])
        print(f"Detections saved to {output_csv}")
    except Exception as e:
        print(f"Error saving detections to CSV: {e}")


# =========================
# 6. 3D Visualization of Floorplan
# =========================
def plot_3d_floorplan(wall_boxes):
    """
    Visualizes the 3D structure of the floorplan using detected wall coordinates.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for box in wall_boxes:
        x1, y1, x2, y2 = box
        vertices = [
            [(x1, y1, 0), (x2, y1, 0), (x2, y2, 0), (x1, y2, 0)],
            [(x1, y1, 10), (x2, y1, 10), (x2, y2, 10), (x1, y2, 10)]
        ]
        poly3d = Poly3DCollection(vertices, alpha=0.4, linewidths=1, edgecolors='r')
        ax.add_collection3d(poly3d)
    plt.show()


# =========================
# 7. Main Execution
# =========================
if __name__ == "__main__":
    # Inputs
    image_path = "/Users/amanchandel/Work/projects/MCV2/floorplans/6.jpg"
    model_id = "floor-plan-segmentation-dtr4r/3"
    api_key = os.getenv('ROBOFLOW_API_KEY')  # Make sure to set the API key in your environment
    
    # Step 1: Load image
    image = load_image(image_path)
    
    # Step 2: Run Roboflow Detection
    roboflow_results = run_roboflow_detection(image, model_id, api_key)

    # Step 3: Run YOLOv8 Detection (local backup)
    yolo_results = run_yolo_detection(image)
    
    # Step 4: Visualize Results
    visualize_results(image, yolo_results=yolo_results, roboflow_results=roboflow_results)

    # Step 5: Extract Wall Coordinates (example logic)
    wall_boxes = [
        [100, 200, 150, 250],  # Example format [x1, y1, x2, y2]
        [300, 400, 350, 450]
    ]

    # Step 6: 3D Plotting (only plotting walls for now)
    plot_3d_floorplan(wall_boxes)

    # Step 7: Save Results to CSV (optional)
    if yolo_results:
        detections = []
        for box in yolo_results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box
            cls = int(box.cls[0])  # Class index
            conf = float(box.conf[0])  # Confidence score
            detections.append({'class': cls, 'confidence': conf, 'box': [x1, y1, x2, y2]})
        save_detections_to_csv(detections)
