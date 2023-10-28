import cv2
import os
import moviepy.editor as mpe

def create_video_from_images(images_folder, output_video, fps=10, duration=10):
    images = sorted(os.listdir(images_folder))
 
    # create path to the input images
    img_path = os.path.join(images_folder, images[0])
     
    # load image
    frame = cv2.imread(img_path)
    # extract dimensions of the image
    height, width, _ = frame.shape
 
    video_writer = cv2.VideoWriter(output_video, 
                                   cv2.VideoWriter_fourcc(*'mp4v'), 
                                   fps, 
                                   (width, height))
 
    # total number of frames for the video
    frames_per_image = fps * duration
 
    for image in images:
        img_path = os.path.join(images_folder, image)
        frame = cv2.imread(img_path)
         
        for _ in range(frames_per_image):
            video_writer.write(frame)
 
    video_writer.release()
    print(f"Video {output_video} created successfully")

def add_audio():
    video_clip = mpe.VideoFileClip("./output/out.mp4")
    audio_clip = mpe.AudioFileClip("./audio/bgm.mp3")
    video_clip.audio = audio_clip.audio_loop(duration=video_clip.duration)
    video_clip.to_videofile('output/final_result.mp4')
    # final = video_clip.set_audio(audio_clip)
    # final.write_videofile("output/final_result.mp4")


create_video_from_images("./images", "output/out.mp4")
add_audio()
