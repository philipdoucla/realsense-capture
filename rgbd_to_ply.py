import open3d as o3d
import numpy as np
import cv2

# Load RGB and depth images
color_image = cv2.imread('color_image.png')
depth_image = cv2.imread('depth_image.png', cv2.IMREAD_UNCHANGED)

# Ensure depth is in the correct format (uint16)
if depth_image.dtype != np.uint16:
    raise ValueError("Depth image must be in uint16 format.")

# Convert images to Open3D format
rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
    o3d.geometry.Image(color_image),
    o3d.geometry.Image(depth_image),
    depth_scale=1000.0,  # Adjust this scale according to your depth image format
    depth_trunc=3.0,  # Truncate depth values beyond this limit
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

# Save the point cloud as a PLY file
o3d.io.write_point_cloud('point_cloud.ply', point_cloud)

# Optionally, visualize the point cloud
o3d.visualization.draw_geometries([point_cloud])
