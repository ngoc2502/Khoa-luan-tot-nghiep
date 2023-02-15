import cv2
import os
import sqlite3

'''
Saving .avi videos as .jpg frames (also creates a frames.db SQL database per video)
'''
def save_video_frames_as_jpg(video_path):
    # Create a folder to store the frames
    frames_folder = os.path.splitext(video_path)[0] + "_frames"
    os.makedirs(frames_folder, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Failed to open video file")
        return

    # Create a SQL database for the frames
    frames_db = os.path.splitext(video_path)[0] + "_frames.db"
    conn = sqlite3.connect(frames_db)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE frames
                      (frame_number INTEGER PRIMARY KEY,
                       file_name TEXT NOT NULL)""")

    # Loop through the frames and save them as .jpg files
    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_file_name = f"{frames_folder}/frame{frame_number:04d}.jpg"
        cv2.imwrite(frame_file_name, frame)
        cursor.execute("INSERT INTO frames (frame_number, file_name) VALUES (?, ?)",
                       (frame_number, frame_file_name))
        frame_number += 1

    # Close the video file and SQL database
    cap.release()
    conn.commit()
    conn.close()

    print(f"Saved {frame_number} frames to {frames_folder} and created {frames_db}")

def process_avi_videos_in_folder(folder_path):
    for video_file_name in os.listdir(folder_path):
        if video_file_name.endswith(".avi"):
            video_path = os.path.join(folder_path, video_file_name)
            save_video_frames_as_jpg(video_path)

#Check function 
# save_video_frames_as_jpg('cat.avi')

process_avi_videos_in_folder('avi_data_check')