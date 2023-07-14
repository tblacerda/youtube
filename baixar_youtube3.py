import os
import datetime
import yt_dlp as youtube_dl
from pydub import AudioSegment

def download_audio(url, start_time, folder, frame_rate, channels, sample_width, line_number):
    # Get 10 seconds of audio
    end_time = start_time + 60  # seconds

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'verbose': False  # Add the verbose flag
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_file = f"{info_dict['id']}.wav"

        ydl.download([url])

    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(frame_rate)
    audio = audio.set_channels(channels)
    audio = audio.set_sample_width(sample_width)
    audio = audio[start_time * 1000:end_time * 1000]

    audio_filename = f"{line_number}_{os.path.basename(audio_file)}"
    audio_filename = os.path.splitext(audio_filename)[0] + '.wav'

    output_path = os.path.join(folder, audio_filename)
    audio.export(output_path, format="wav")

    os.remove(audio_file)
    print(f"Audio download complete with {frame_rate} samples per second, {channels} channel(s), and {sample_width * 8}-bit resolution!")


file_path = "urls_unix.txt"
with open(file_path, 'r') as file:
    lines = file.readlines()
    total_lines = len(lines)

    for counter, line in enumerate(lines, start=1):
        url, _, start_time, folder = line.strip().split(',')
        start_time = int(start_time.strip())
        print(f"Processing line {counter} of {total_lines}")
        print('Trying URL:', url)
        try:
            download_audio(url, start_time, folder, frame_rate=16000, channels=1, sample_width=2, line_number=counter)
        except:
            pass
