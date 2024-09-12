# AI-Grocery-Store-Management-System

## Overview
This Python program is designed to automate grocery inventory management by detecting missing items and sending email notifications for restocking. The system uses a YOLO model to identify objects (groceries) in an image, checks the inventory database for available stock, and sends appropriate emails based on inventory levels.

## Key Features:
- Object Detection: Uses a YOLO model to detect groceries in a given image.
- Inventory Check: Compares detected groceries with available stock from the inventory database.
- Automated Email Notifications: Sends emails for restocking items or low inventory alerts.