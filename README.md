
# Tiktok style video automation 

A tiktok style video automated using: [Groq AI](https://groq.com/) - to generate text, [Faster Whisper Git](https://github.com/SYSTRAN/faster-whisper) - for word timestamps, [Pytubefix](https://github.com/JuanBindez/pytubefix) - to download youtube videos and [VoiceRSS TTS](https://www.voicerss.org/) - for tts purposes.


## Video output demonstration 

First 15s of the final video: (no sound here)

![](https://github.com/francool57/tiktok-video-automation/blob/main/final_tiktok_gif.gif)
**Note:** Default font is Arial Black, in example im using Yataghan Regular

![Alt text](https://img001.prntscr.com/file/img001/1j_auwOBTUakiTCKrDEdvA.png)

**Alt:** Terminal screenshot

## How To Deploy

Clone the git repositorie or download [here](https://github.com/francool57/tiktok-video-automation/archive/refs/heads/main.zip)
```cmd
  git clone https://github.com/francool57/tiktok-video-automation.git
  cd tiktok-video-automation
```
Run ```python setup.py``` and input: ```GROC_API_KEY``` & ```VOICERSS_API_KEY```

**Finally** - run ```python short_create.py```, input your catchy hook and let the program do its job!



## FAQ

#### Can I get a specific video?

Yes. Inside ```short_create.py``` find the ```yut.Download()``` and change it to: ```yut.Download(url='YOUR_DESIRED_VIDEO')```.



## Authors

- [@xannydev](https://github.com/francool57)

