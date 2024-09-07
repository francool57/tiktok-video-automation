from groq import Groq
from moviepy.editor import *
from moviepy.config import change_settings
from faster_whisper import WhisperModel
import yt_sc as yut
import VoiceRSSWebAPI
import random
import base64
import time as tm

banner = '''    
██╗░░██╗██╗░░██╗░█████╗░███╗░░██╗███╗░░██╗██╗░░░██╗
╚██╗██╔╝╚██╗██╔╝██╔══██╗████╗░██║████╗░██║╚██╗░██╔╝
░╚███╔╝░░╚███╔╝░███████║██╔██╗██║██╔██╗██║░╚████╔╝░
░██╔██╗░░██╔██╗░██╔══██║██║╚████║██║╚████║░░╚██╔╝░░
██╔╝╚██╗██╔╝╚██╗██║░░██║██║░╚███║██║░╚███║░░░██║░░░
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝░░░╚═╝░░░
               github.com/francool57
        \n'''
print(banner)
starttime = tm.time()

#TODO: Change variables that fit you
path = r'YOUR_FILES_PATH\\'
audio_file_mp3 = r"story_audio.mp3" 
video_file_mp4 = r"fullyutubevideo.mp4" 
hookfile = r"hookaudio.mp3" 
storyhook = 'I was abducted by my own uncle, but he never expected what i did to him.' # First words of the video, do as the example
groc_api_key = 'YOUR_GROC_API' # Groc API key: https://console.groq.com/keys
voicerss_api = 'YOUR_VOICERSS_API' # VoiceRSS API key: https://www.voicerss.org/

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
change_settings({"IMAGEMAGICK_BINARY": r"c:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"}) # ImageMagick executable input with

# Find random youtube video and download (no setting will result in minecraft parkout)

try:
    yut.Download(file_name_dir=path+video_file_mp4) # Implement search='YOUR_DESIRED_SEARCH' to your desires 
except BaseException as e:
    print(f"{yut.Bcolors.RED}An error has occurred: ||{str(e)}||. Re-running...{yut.Bcolors.END}") # Errors that can be resolved with 
    yut.Download(file_name_dir=path+video_file_mp4)                                                                                 # re-running the script will fix themselves


# Groc API
client = Groq(
    api_key=groc_api_key,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f'''Generate a scary reddit-like story being told from the point of view of the person that was exposed to the event. 
            The story should be around this first line that the person said \"{storyhook}\", and the story should not contain this phrase.
            This story should be around 80 words.
            The story has to be based on realistic events.
            Start the story with a short hook that portrays the most unsettling part of the story.
            The story should have a good ending.
            The story should be as a written essay, without anything as hook or here's a scary story told from the point of view of a Reddit-like storyteller.''',
        }
    ],
    model="llama3-8b-8192",
)
response = chat_completion.choices[0].message.content
print(f'{yut.Bcolors.GREEN}Text was generated{yut.Bcolors.END}')

#tts
voicer = random.choice(['Mike','John','Amy','Linda'])
voice = VoiceRSSWebAPI.speech({  
    'key': voicerss_api,
    'hl': 'en-us',
    'v': voicer, 
    'src': response,
    'r': '0',
    'c': 'mp3',
    'f': '44khz_16bit_stereo',
    'ssml': 'false',
    'b64': 'true'
})                              # Story voiceover

# b64 to mp3
wav_file = open(os.path.join(path, audio_file_mp3), "wb")   
decode_string = base64.b64decode(voice['response'])
wav_file.write(decode_string)
print(f'{yut.Bcolors.GREEN}Audio was created as story_audio.mp3{yut.Bcolors.END}')
wav_file.close()

voice = VoiceRSSWebAPI.speech({
    'key': voicerss_api,
    'hl': 'en-us',  
    'v': voicer,
    'src': storyhook,
    'r': '0',
    'c': 'mp3',
    'f': '44khz_16bit_stereo',
    'ssml': 'false',
    'b64': 'true'
})                              # Hook voiceover

wav_file = open(os.path.join(path, hookfile), "wb")
decode_string = base64.b64decode(voice['response'])
wav_file.write(decode_string)
print(f'{yut.Bcolors.GREEN}Audio was created as hookaudio.mp3{yut.Bcolors.END}')
wav_file.close()

def video_create():
    # Load the audio file
    audio = AudioFileClip(path + audio_file_mp3)
    audio2 = AudioFileClip(path + hookfile)
    print(f'{yut.Bcolors.BLUE}Audio was added{yut.Bcolors.END}')


    # Load the video file
    video = VideoFileClip(path + video_file_mp4)
    # Calculate the center coordinates of the video
    crop_x = 1980 / 2
    crop_y = 1280 / 2

    # Resize the video to TikTok format (720x1280)
    video = video.resize((1980, 1280))
    video_resized = video.crop(
                            x_center = crop_x, 
                            y_center = crop_y, 
                            width=720, 
                            height=1280
                            ).set_duration(audio.duration+audio2.duration)

    print(f'{yut.Bcolors.BLUE}Video was re-sized{yut.Bcolors.END}')

    # Attach the audio to the video
    mixed = CompositeAudioClip([audio2, audio.set_start(audio2.duration)]) # Sums both audios
    video_with_audio = video_resized.set_audio(mixed)

    # Define the text to display, one word at a time
    clips = []
    model_size = "large-v3"

    # stt and word division
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    segments, info = model.transcribe(path+audio_file_mp3, word_timestamps=True)
    segments2, info2 = model.transcribe(path+hookfile, word_timestamps=True)
    print(f'{yut.Bcolors.CYAN}Fast-Whisper model loaded{yut.Bcolors.END}')

    for segment2 in segments2:
        for i,word in enumerate(segment2.words):
            time = word.end-word.start
            txt = TextClip(word.word, 
                            font='Arial-Black',
                            fontsize=70, 
                            color='red', 
                            size=(1080, 250), 
                            stroke_color='black', 
                            stroke_width=2).set_position('center').set_duration(time).set_start(word.start)
            clips.append(txt)
    print(f'{yut.Bcolors.BLUE}Hook was appended as clips{yut.Bcolors.END}')
    
    # Add each word as a separate TextClip
    for segment in segments:
        for i,word in enumerate(segment.words):
            time = word.end-word.start
            txt_clip = TextClip(word.word, 
                                font='Arial-Black',
                                fontsize=70, 
                                color='white', 
                                size=(1080, 250), 
                                stroke_color='black', 
                                stroke_width=2).set_position('center').set_duration(time).set_start(word.start+audio2.duration)
            clips.append(txt_clip)
    print(f'{yut.Bcolors.BLUE}Text was appended as clips{yut.Bcolors.END}')

    # Overlay the text clips on the video
    video_with_text = CompositeVideoClip([video_with_audio] + clips)

    size_vid = str(video_with_text.size).replace(', ','x')
    print(f'{yut.Bcolors.CYAN}Video has {size_vid} dimensions{yut.Bcolors.END}')
    # Export the final video
    video_with_text.write_videofile(f"{path}final_tiktok_video.mp4", fps=24)

if __name__ == '__main__':
    video_create()
    endtime = tm.time()
    timee = int(endtime-starttime)
    print(f'Elapsed time: {timee}s')
else: 
    print('I have no idea why it did not run')
    exit()