import pyrealsense2 as rs
import numpy as np
import cv2
import os
import sys

# Check if an argument was provided
if len(sys.argv) != 2:
    print("Usage: python program.py <label>")
    sys.exit(1)

# Get the directory name suffix from the command-line argument
dir_suffix = sys.argv[1]

# Create the color and depth directories with the suffix
color_dir = f'color_{dir_suffix}'
depth_dir = f'depth_{dir_suffix}'

# Create the directories
os.makedirs(color_dir, exist_ok=True)
os.makedirs(depth_dir, exist_ok=True)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Enable the depth and color streams
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Create an align object
align_to = rs.stream.color
align = rs.align(align_to)

try:
    frame_count = 0  # Initialize frame counter

    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Convert BGR to RGB
        color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # Apply colormap on depth image (optional for visualization)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Stack both images vertically for visualization
        images = np.vstack((color_image_rgb, depth_colormap))

        # Create a named window
        cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)

        # Resize the window (not the image)
        cv2.resizeWindow('RealSense', 640, 640)

        # Show images
        cv2.imshow('RealSense', images)

        # Save the frames to files with incrementing filenames
        color_filename = os.path.join(color_dir, f'color_image_{frame_count}.png')
        depth_filename = os.path.join(depth_dir, f'depth_image_{frame_count}.png')

        cv2.imwrite(color_filename, color_image_rgb)
        cv2.imwrite(depth_filename, depth_image)

        frame_count += 1  # Increment frame counter

        # Break the loop by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()

cv2.destroyAllWindows()
