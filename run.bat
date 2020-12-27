@Echo Off
cd "%~dp0"
git submodule update --init
py -m pip install --upgrade pip
py -m pip install pynput
py -m pip install pywin32
py -m pip install playsound
py -m pip install scapy
py -m pip install --upgrade google-cloud-texttospeech
cls
py main.py
