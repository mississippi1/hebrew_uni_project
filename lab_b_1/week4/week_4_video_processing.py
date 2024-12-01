import imageio
import os
import zipfile

# Specify the zip file containing the AVI videos
zip_path = "/Users/tomerpeker/Downloads/drive-download-20241127T160402Z-001.zip"
output_base_dir = "extracted_videos_frames"

# Create a base output directory
os.makedirs(output_base_dir, exist_ok=True)

# Step 1: Extract the ZIP file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(output_base_dir)  # Extract videos to output_base_dir

print(f"All videos extracted to {output_base_dir}")

# Step 2: Process each AVI file
for root, _, files in os.walk(output_base_dir):
    for file in files:
        if file.lower().endswith('.avi'):
            video_path = os.path.join(root, file)
            video_name = os.path.splitext(file)[0]

            # Create a specific folder for each video
            video_output_dir = os.path.join(output_base_dir, video_name)
            os.makedirs(video_output_dir, exist_ok=True)

            # Step 3: Read the video and save frames
            reader = imageio.get_reader(video_path, format='FFMPEG')
            frame_number = 0

            for idx, frame in enumerate(reader):
                if idx % 5 == 0:
                    output_file = os.path.join(video_output_dir, f"frame_{frame_number:04d}.jpg")
                    imageio.imwrite(output_file, frame)
                    print(f"Saved frame {frame_number} of video {video_name}")

                frame_number += 1

            print(f"All frames for {video_name} saved to {video_output_dir}")

print("All videos processed.")
