import json
import os
from pathlib import Path
import shutil
path = Path.cwd()

def req_instalation():
    os.system('pip install faster-whisper')
    os.system('pip install -r requirements.txt')

def create_files():
    open(os.path.join(str(path)+r'\video_audio','story_audio.mp3'), 'wb')
    open(os.path.join(str(path)+r'\video_audio','hookaudio.mp3'), 'wb')
    
def settings():
    data = {
        'path': str(path)+r'\video_audio\\',
        'groc_api_key': input('GROC_API_KEY: '),
        'voicerss_api': input('VOICERSS_API_KEY: ')
    }
    with open('settings.json', 'w') as f:
        json.dump(data, f, indent=4)

if shutil.which("magick") == None:
    print('Install ImageMagick')
    exit()

req_instalation()
create_files()
settings()


