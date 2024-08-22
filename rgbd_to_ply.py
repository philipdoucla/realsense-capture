import open3d as o3d
import numpy as np
import cv2
import os

# Define the paths to the color and depth folders
color_folder = 'color'
depth_folder = 'depth'
point_cloud_folder = 'point_clouds'

# Create the point_clouds directory if it doesn't exist
if not os.path.exists(point_cloud_folder):
    os.makedirs(point_cloud_folder)

# Get the list of color and depth images
color_images = sorted([os.path.join(color_folder, f) for f in os.listdir(color_folder) if f.endswith('.png')])
depth_images = sorted([os.path.join(depth_folder, f) for f in os.listdir(depth_folder) if f.endswith('.png')])

# Ensure the number of color and depth images match
if len(color_images) != len(depth_images):
    raise ValueError("The number of color and depth images must be the same.")

# Process each pair of color and depth images
for idx, (color_image_path, depth_image_path) in enumerate(zip(color_images, depth_images)):
    # Load RGB and depth images
    color_image = cv2.imread(color_image_path)
    depth_image = cv2.imread(depth_image_path, cv2.IMREAD_UNCHANGED)

    # Ensure depth is in the correct format (uint16)
    if depth_image.dtype != np.uint16:
        raise ValueError(f"Depth image {depth_image_path} must be in uint16 format.")

    # Convert images to Open3D format
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        o3d.geometry.Image(color_image),
        o3d.geometry.Image(depth_image),
        depth_scale=1000.0,  # Adjust this scale according to your depth image format
        depth_trunc=1000.0,  # Truncate depth values beyond this limit
        convert_rgb_to_intensity=False
    )

    # Create a PinholeCameraIntrinsic object
    pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
        o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault
    )

    # Create the point cloud
    point_cloud = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image,
        pinhole_camera_intrinsic
    )

    # Flip the point cloud to be compatible with Open3D's visualization
    point_cloud.transform([[1, 0, 0, 0],
                           [0, -1, 0, 0],
                           [0, 0, -1, 0],
                           [0, 0, 0, 1]])

    # Generate output filename for the point cloud
    point_cloud_filename = os.path.join(point_cloud_folder, f'point_cloud_{idx}.ply')

    # Save the point cloud as a PLY file
    o3d.io.write_point_cloud(point_cloud_filename, point_cloud)

    # Optionally, visualize the point cloud
    # o3d.visualization.draw_geometries([point_cloud])
