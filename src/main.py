import cv2
import os
import moviepy.editor as mpe
from gtts import gTTS
from pydub import AudioSegment


def create_video_from_images(images_folder, output_video, fps=10, duration_per_image=7):
    print(f"Current working directory: {os.getcwd()}")
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_video), exist_ok=True)
    
    # Ensure images_folder exists and is a directory
    if not os.path.isdir(images_folder):
        print(f"Images folder '{images_folder}' does not exist or is not a directory.")
        return
    images = sorted(
        img for img in os.listdir(images_folder)
        if img.lower().endswith(('.png', '.jpg', '.jpeg'))
    )
    if not images:
        print(f"No images found in {images_folder}!")
        return

    # Load first image to get dimensions
    first_img_path = os.path.join(images_folder, images[0])
    frame = cv2.imread(first_img_path)
    if frame is None:
        print(f"Unable to read first image: {images[0]}")
        return
    height, width, _ = frame.shape
    print(f"Reference image shape: {frame.shape}")

    # Initialize Video Writer
    video_writer = cv2.VideoWriter(
        output_video,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    frames_per_image = fps * duration_per_image

    # Precompute image paths
    img_paths = [os.path.join(images_folder, img) for img in images]
    print(f"Images to be used ({len(img_paths)}):")
    for img_path in img_paths:
        print(f"  {img_path}")
    for img_path, image in zip(img_paths, images):
        print(f"Processing image: {image}")
        frame = cv2.imread(img_path)
        if frame is None:
            print(f"Skipping {image} - Unable to read image at {img_path}.")
            continue
        if frame.shape != (height, width, 3):
            print(f"Resizing {image} from {frame.shape} to {(height, width, 3)}")
            frame = cv2.resize(frame, (width, height))
        # Write all frames for this image in one go
        for _ in range(frames_per_image):
            video_writer.write(frame)

    video_writer.release()
    print(f"Video {output_video} created successfully")


def add_bgm_audio(video_path, audio_path, output_path):
    print("Embedding background music...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    video_clip = mpe.VideoFileClip(video_path)
    audio_clip = mpe.AudioFileClip(audio_path)
    # Use min duration for safety
    min_duration = min(video_clip.duration, audio_clip.duration)
    video_clip = video_clip.subclip(0, min_duration)
    audio_clip = audio_clip.subclip(0, min_duration)
    final_video = video_clip.set_audio(audio_clip)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4, preset="ultrafast")
    print(f"Video {output_path} created successfully with background music")


def add_text_audio(output_video):
    os.makedirs("audio", exist_ok=True)

    mytext = ("Subhas Chandra Bose was born on 23 January 1897 in Cuttack, India."
              "He was a prominent leader in the Indian independence movement against British rule."
              "Bose founded the Indian National Army (INA) to fight for India’s freedom."
              "He famously said, “Give me blood, and I will give you freedom!” to inspire Indians to join the struggle."
              "He disappeared in 1945, and is presumed to have died in a plane crash, leaving a lasting legacy.")

    tts = gTTS(text=mytext, lang='en', slow=True)
    speech_file = "./audio/speech.mp3"
    tts.save(speech_file)

    audio = AudioSegment.from_file(speech_file)
    # Use inplace speedup and export
    faster_audio = audio.speedup(playback_speed=1.3)
    faster_audio_file = "./audio/faster_output.mp3"
    faster_audio.export(faster_audio_file, format="mp3")

    add_bgm_audio(output_video, faster_audio_file, "output/final_result.mp4")


# Running the functions
create_video_from_images("images", "output/out.mp4")
#add_bgm_audio("output/out.mp4", "./audio/bgm1.mp3", "output/final_result.mp4")
add_text_audio("output/out.mp4")  # Uncomment to add TTS audio
