import cv2
import time

def avc1_encode_video(input_video_path, output_video_path):
    video = cv2.VideoCapture(input_video_path)
    
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    start_time = time.time()

    while True:
        ret, frame = video.read()

        if not ret:
            break

        out.write(frame)

    video.release()
    out.release()

    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

video_encode_time = avc1_encode_video('output_video.mp4', 'output_encoded_video.mp4')

print(video_encode_time)
