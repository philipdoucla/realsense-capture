import cv2
import re

import os

# Directory containing the PNG images
image_dir = "segmented"
# Output MP4 video file path
output_video = "output_video.mp4"
# Frame rate (number of frames per second)
fps = 20

# Function to extract numbers from filenames
def numerical_sort(value):
    # Find all numeric parts of the filename for sorting
    numbers = re.findall(r'\d+', value)
    return int(numbers[0]) if numbers else 0

# Get a list of all PNG files in the directory
images = [img for img in os.listdir(image_dir) if img.endswith(".png")]
# Sort the images numerically (based on extracted numbers from filenames)
images.sort(key=numerical_sort)

# Read the first image to get the size (height and width)
first_image = cv2.imread(os.path.join(image_dir, images[0]))
height, width, _ = first_image.shape

# Initialize the video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

# Loop through each image and add it to the video
for image in images:
    img_path = os.path.join(image_dir, image)
    img = cv2.imread(img_path)
    
    # Add the image to the video
    video_writer.write(img)

# Release the video writer object
video_writer.release()

print(f"Video saved as {output_video}")