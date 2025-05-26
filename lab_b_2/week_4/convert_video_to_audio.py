import ffmpeg
import os

FFMPEG_PATH = r"/usr/local/bin/ffmpeg"


def convert_mp4_to_mp3(mp4_path, mp3_path=None):
    if not os.path.exists(mp4_path):
        raise FileNotFoundError(f"File not found: {mp4_path}")

    if mp3_path is None:
        mp3_path = os.path.splitext(mp4_path)[0] + ".mp3"
    print(mp3_path)
    try:

        ffmpeg \
            .input(mp4_path) \
            .output(mp3_path, format='mp3', acodec='libmp3lame', audio_bitrate='192k') \
            .run(cmd=FFMPEG_PATH, overwrite_output=True, quiet=True)
        return mp3_path
    except ffmpeg.Error as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")


# Example usage
if __name__ == "__main__":
    input_video = '/Users/tomerpeker/Downloads/screen-2 (3).mp4'
    convert_mp4_to_mp3(input_video)
