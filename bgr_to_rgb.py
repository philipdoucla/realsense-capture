import os
import cv2

# Define the path to the directory containing the BGR images
input_dir = "color"
output_dir = "rgb_fix"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize a counter to skip the first frame
skip_first = True

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    if skip_first:
        skip_first = False  # Skip the first file and reset the flag
        continue  # Skip this iteration

    if filename.endswith(".jpg") or filename.endswith(".png"):  # Modify based on your image format
        # Construct the full input and output file paths
        input_path = os.path.join(input_dir, filename)
        
        print(  )
        
        # Change the output file extension to .jpeg
        output_filename = os.path.splitext(filename)[0][12:].zfill(4) + ".jpg"

        output_path = os.path.join(output_dir, output_filename)

        # Load the image in BGR format (default in OpenCV)
        color_image = cv2.imread(input_path)

        # Convert the BGR image to RGB
        color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # Save the converted image as JPEG to the output directory
        cv2.imwrite(output_path, color_image_rgb, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # Quality is set to 100

        print(f"Converted {filename} to RGB and saved as {output_filename} in {output_dir}")

print("Conversion complete!")
