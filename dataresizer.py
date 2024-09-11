import os
from PIL import Image

# Define the input and output folder paths
input_folder = 'raw data'  # Folder with original images
output_folder = 'resized_raw_data'  # Folder to save resized images

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Set the target sizex``
target_size = (640,1020)

# Loop through all the files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # Filter image files
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        
        # Resize the image
        img_resized = img.resize(target_size)
        
        # Save the resized image to the output folder
        save_path = os.path.join(output_folder, filename)
        img_resized.save(save_path)
        
        print(f"Resized and saved {filename} to {output_folder}")
