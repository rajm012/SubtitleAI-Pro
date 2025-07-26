from pytubefix import YouTube
from faster_whisper import WhisperModel
import os
import uuid
from urllib.parse import urlparse, parse_qs

def clean_youtube_url(url):
    if "youtu.be" in url:
        url = url.split("?")[0]
    elif "youtube.com" in url:
        parsed = urlparse(url)
        video_id = parse_qs(parsed.query).get("v", [None])[0]
        if video_id:
            url = f"https://www.youtube.com/watch?v={video_id}"
    return url



def download_audio(youtube_url, output_dir="downloads"):
    yt = clean_youtube_url(youtube_url)
    yt = YouTube(yt)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    unique_filename = f"{uuid.uuid4()}.mp4"
    download_path = os.path.join(output_dir, unique_filename)
    audio_stream.download(output_path=output_dir, filename=unique_filename)
    
    return download_path

# def transcribe_audio(audio_path, model_size="base"):
#     try:
#         # Explicitly use CPU and int8 compute type for better compatibility
#         model = WhisperModel(model_size, device="cpu", compute_type="int8")
        
#         segments, _ = model.transcribe(audio_path, beam_size=5)
        
#         subtitles = []
#         for segment in segments:
#             subtitles.append({
#                 "start": segment.start,
#                 "end": segment.end,
#                 "text": segment.text.strip()
#             })
        
#         return subtitles
#     except Exception as e:
#         print(f"Error during transcription: {e}")
#         return []
    
def transcribe_audio(audio_path, model_size="base"):
    try:
        # Use translate mode to force English output
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        
        segments, _ = model.transcribe(audio_path, beam_size=5, task="translate")
        
        subtitles = []
        for segment in segments:
            subtitles.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
        
        return subtitles
    except Exception as e:
        print(f"Error during transcription: {e}")
        return []

def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def write_srt(subtitles, filename="output.srt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, sub in enumerate(subtitles, 1):
            start_time = seconds_to_srt_time(sub["start"])
            end_time = seconds_to_srt_time(sub["end"])
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{sub['text']}\n\n")

if __name__ == "__main__":
    youtube_link = input("Enter YouTube video link: ")
    print("📥 Downloading audio...")
    audio_path = download_audio(youtube_link)
    print(f"✅ Audio downloaded to: {audio_path}")
    
    print("🧠 Generating subtitles...")
    subs = transcribe_audio(audio_path)
    
    if not subs:
        print("❌ No subtitles generated. Please check for errors above.")
        exit(1)

    print("💾 Writing to SRT file...")
    write_srt(subs, filename="output.srt")
    
    print("✅ Subtitle generation completed! File saved as `output.srt`.\n")
    print("--- Preview ---\n")
    for s in subs[:5]:
        print(f"[{s['start']:.2f}s - {s['end']:.2f}s] {s['text']}")


