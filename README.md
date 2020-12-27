# Among Us Chatbot

#### _Check me out on Twitch! https://twitch.tv/julescodes_

A chatbot created in Python for Among Us shenanigans.

## Prerequisites
* Windows 7/8/10
* [Python 3](https://www.python.org/downloads/)
* [Npcap](https://nmap.org/npcap/)
* [Git](https://git-scm.com/download/win)
* (Optional) [A GCP account key](https://cloud.google.com/text-to-speech/docs/libraries#setting_up_authentication)
    * Once you've created an account key, download the file as `creds.json` and save it in the root folder of the repo.
        * Environment variable step in above link is optional if you do this step.
    * You'll also need to 
      [activate the TTS API](https://console.developers.google.com/apis/api/texttospeech.googleapis.com/overview). 
      Google requests your billing info, though unless you're planning on submitting `>1MM chars/mth`, you
      shouldn't get billed.
      

## Install and Run

1. In Command Prompt, clone this repository into your directory of choice:
```cmd
C:\...> git clone https://github.com/pondchamp/among_bots.git
```

2. Open the root folder of this repo in PyCharm Community as a project.
3. Run the `run.bat` file:
```cmd
C:\...> cd among_bots
C:\...\among_bots> run.bat
```

**NOTE: Text-to-speech only works when the Among Us game window is active.**

## Usage and Copyright

Source code use, reproduction, and distribution rights are managed by the Apache License terms (see `LICENSE`).

You are free to use or modify this bot for livestreams or on-demand video recordings, provided you provide attribution
to my Twitch channel (**JulesCodes**) in the content of the video.

## Credits

Thank you to the following people for providing various libraries that I leveraged to create this project!
* [Among Us Parser by _jordam_](https://github.com/jordam/amongUsParser)
* [Among Us Protocol Documentation](https://wiki.weewoo.net/)
