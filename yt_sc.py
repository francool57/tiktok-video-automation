from pytubefix import YouTube
import random
from youtubesearchpython import VideosSearch

class Bcolors: # For colored messages 
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#search the video and randomly choose it (no bigger than 15m)
def link_gen(search):
    videosSearch = VideosSearch(search)
    num = random.randint(0,19)
    num2 = random.randint(0,19)
    page = random.choice([0,1,2,3,4,5])
    for i in range(page):
        videosSearch.next()
    x = videosSearch.result()['result']
    try:
        link = x[num]['link'] 
    except:
        link = x[num2]['link'] 
    print(f'{Bcolors.GREEN}Youtube video was found{Bcolors.END}')
    return link

def Download(search = 'minecraft parkour gameplay no copyright 4k', url = None, resolution = '1080p'):
    if url == None:
        youtubeObject = YouTube(link_gen(search))
        streams = youtubeObject.streams
        if int(youtubeObject.length) < 900:
            stream = (streams.filter(
                                        only_video=True, 
                                        res='1080p', 
                                        video_codec='vp9'
                                        ))
            try:
                execute(stream)
            except BaseException as e: 
                print(f"{Bcolors.RED}An error has occurred: ||{str(e)}|| Re-running{Bcolors.END}")
                Download()
        else:
            print(f'{Bcolors.RED}Video was too big, searching again{Bcolors.END}')
            Download()
    else:
        youtubeObject = YouTube(url)
        streams = youtubeObject.streams
        stream = (streams.filter(
                            only_video=True, 
                            res=resolution, 
                            video_codec='vp9'
                            ))
        execute(stream)

def execute(stream):
    print(f'{Bcolors.PINK}Downloading...{Bcolors.END}')
    stream.first().download(filename='fullyoutube.mp4')
    print(f"{Bcolors.GREEN}Download was completed{Bcolors.END}")