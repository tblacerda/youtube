# ambiente pyaudio
import os
import datetime
from pytube import YouTube
from pydub import AudioSegment

def download_audio(url, frame_rate, channels, sample_width, _Start, Folder, LineNumber):
        # Get 10 seconds of audio
    
    end_time = _Start + 60 # seconds
    
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download()

    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(frame_rate)
    audio = audio.set_channels(channels)
    audio = audio.set_sample_width(sample_width)
    audio = audio[start_time*1000 : end_time*1000]
    
    audio_filename = f"{LineNumber}_{os.path.basename(audio_file)}"
    audio_filename = os.path.splitext(audio_filename)[0] + '.wav'

    output_path = os.path.join(Folder, audio_filename)
    audio.export(output_path, format="wav")

    os.remove(audio_file)
    print(f"Audio download complete with {frame_rate} samples per second, {channels} channel(s), and {sample_width * 8}-bit resolution!")


file_path = "urls_unix.txt"
with open(file_path, 'r') as file:
    lines = file.readlines()
    total_lines = len(lines)
    
    for counter, line in enumerate(lines, start=1):
        url,_,start_time, folder = line.strip().split(',')
        start_time = int(start_time.strip())
        print(f"Processando linha {counter} of {total_lines}")
        print('Tentando URL: ', url)
        #try:
        download_audio(url, frame_rate=16000, channels=1, sample_width=2, _Start=start_time, Folder=folder, LineNumber=counter)
        # except:
        #     pass
