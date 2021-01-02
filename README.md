# Among Us Chatbot

#### _Check me out on Twitch! https://twitch.tv/julescodes_

A chatbot created in Python for Among Us shenanigans.

## Prerequisites
* Windows 7/8/10
* [Npcap](https://nmap.org/npcap/)
  
### Optional: Using GCP Text To Speech (TTS)

**NOTE: TTS only works when the Among Us game window is active.**

Among Bots uses gTTS out of the box - no further setup is required.
However, if you would like a smoother voice with more intonation (plus all-caps mode),
you will need to set up GCP TTS:

1. [Create a GCP account](https://console.cloud.google.com/).
2. [Create a GCP account key](https://console.cloud.google.com/apis/credentials/serviceaccountkey).
    * Select `New Service Account`.
    * Enter a desired service account name and ID.
    * For `Role`, select `Project > Owner`.
    * Leave key type as `JSON` and click `Create`.
3. Rename the downloaded credentials file to `creds.json` and save it in the same folder as the downloaded EXE.
4. [Activate the TTS API](https://console.developers.google.com/apis/api/texttospeech.googleapis.com/overview).
   * Google requests your billing info, though unless you're planning on submitting `>1MM chars/mth`, you
     shouldn't get billed.
      

## Install and Run

**Download Among.Bots.exe [here](https://github.com/pondchamp/among_bots/releases/download/v0.2-alpha/Among.Bots.exe).**

This EXE is unsigned, so you'll need to dismiss security warnings to run the program.

## Usage and Copyright

Source code use, reproduction, and distribution rights are managed by the Apache License terms (see `LICENSE`).

You are free to use or modify this bot for livestreams or on-demand video recordings, provided you provide attribution
to my Twitch channel (**JulesCodes**) in the content of the video.

## Credits

Thank you to the following people for providing various libraries that I leveraged to create this project!
* [Among Us Parser by _jordam_](https://github.com/jordam/amongUsParser)
* [Among Us Protocol Documentation](https://wiki.weewoo.net/)
