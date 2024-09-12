from ultralytics import YOLO
import cv2  # For displaying the image until you close it
from IPython.display import display, Image
from db import read_records
import smtplib
from email.message import EmailMessage


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
            send_restock_email(i)
        else:
           send_low_inventory_email(i)
            
def send_restock_email(product_name):
    sender_email = "hemanth.vudavagandla@gmail.com" 
    receiver_email = "hemanth.vudavagandla@gmail.com"
    subject = "Restock Request for Product"
    
    # Create email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Email body
    body = f"""
    Dear Shop Floor Team,

    Kindly restock the following product into the shelves:

    Product Name: {product_name}

    Thank you for your prompt attention to this matter.

    Best regards,
    Inventory Management Team
    """
    msg.set_content(body)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_password = "your_email_app_password"

    # Sending the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() 
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Restock email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    
def send_low_inventory_email(product_name):
    sender_email = "hemanth.vudavagandla@gmail.com"
    receiver_email = "hemanthreddy.vudavagandla@gmail.com"
    subject = f"Inventory Low - Refill Request for {product_name}"
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    body = f"""
    Dear Procurement Team,

    This is to inform you that the inventory for {product_name} is running low. 
    We kindly request you to prioritize refilling this product at the earliest convenience to avoid any disruption in our operations.

    Please let me know if further information is required.

    Thank you for your prompt attention to this matter.

    Best regards,
    Inventory Management Team
    """
    msg.set_content(body)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_password = "your_email_app_password"

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Low inventory email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

frame = "IMG_20240907_191857_jpg.rf.99db031cd90b0464f8b18cc6efe9205d.jpg"
prediction = predict_grocery(frame)
image_with_boxes = prediction[0].plot()  # This will plot the bounding boxes on the image
finished_goods = (find_missing_grocery(prediction))
check_inventory_sendmail(finished_goods)
# Display the image with detected boxes using cv2
cv2.imshow("Detected Objects", image_with_boxes)
cv2.waitKey(0)  # Wait until you press any key
cv2.destroyAllWindows()  # Close the window

