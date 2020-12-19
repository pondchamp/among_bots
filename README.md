# Among Us Chatbot

#### _Check me out on Twitch! https://twitch.tv/julescodes_

A chatbot created in Python for Among Us shenanigans.

## Prerequisites
* Windows 10
* [Python 3](https://www.python.org/downloads/)
* [PyCharm Community](https://www.jetbrains.com/pycharm/download/)
* [Npcap](https://nmap.org/npcap/)
* [Git](https://git-scm.com/download/win)
* [A GCP account key](https://cloud.google.com/text-to-speech/docs/libraries)
    * You'll also need to visit this link and enter payment info to
      activate the TTS API, though unless you're planning on making
      \>1M/mth requests, it should be free:
      https://console.developers.google.com/apis/api/texttospeech.googleapis.com/overview?project=<your_project_id>

## Installation

1. In Command Prompt, clone this repository into your directory of choice:
```cmd
git clone https://github.com/pondchamp/among_bots.git
cd among_bots
git submodule init
git submodule update
```

2. Open the root folder of this repo in PyCharm Community as a project.
3. Navigate to the terminal tab at the bottom of PyCharm, then run the
   following commands to install the following Python modules:
```cmd
pip install pynput
pip install pywin32
pip install --upgrade google-cloud-texttospeech
pip install playsound
pip install scapy
```
