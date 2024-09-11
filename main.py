from ultralytics import YOLO
import cv2  # For displaying the image until you close it
from IPython.display import display, Image
from db import read_records

def predict_grocery(frame):
    # Load the YOLO model
    model = YOLO("best (1).pt")
    # Perform object detection
    results = model.predict(source=frame, show=False)
    return results

def find_missing_grocery(detection):
    all_classes = detection[0].names
    classes = []
    for result in detection:
        boxes = result.boxes  # Get the bounding boxes for detected objects
        for box in boxes:
            cls = int(box.cls)  # Get the class index of the detected object
            classes.append(cls)
        classes = set(classes)
        missing_groceries = []
        for i in (set(all_classes.keys())-classes):
            missing_groceries.append(all_classes[i])
        return missing_groceries

def check_inventory_sendmail(groceries):
    inventory = read_records("Inventory")
    for i in groceries:
        if inventory[i] > 10:
            print(f"sent request for filling to shopfloor {i}")
        else:
            print(f"sent request for procurement team for restocking {i}")
    


frame = "IMG_20240907_191857_jpg.rf.99db031cd90b0464f8b18cc6efe9205d.jpg"
prediction = predict_grocery(frame)
image_with_boxes = prediction[0].plot()  # This will plot the bounding boxes on the image
finished_goods = (find_missing_grocery(prediction))
check_inventory_sendmail(finished_goods)
# Display the image with detected boxes using cv2
cv2.imshow("Detected Objects", image_with_boxes)
cv2.waitKey(0)  # Wait until you press any key
cv2.destroyAllWindows()  # Close the window

