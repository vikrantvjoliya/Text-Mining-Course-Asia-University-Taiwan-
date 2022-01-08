import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
import json
from tempfile import gettempdir


#C:\Users\Vikrant\AppData\Local\Temp
inputFileName="E:/KLU/3rd Year/Asia University/Final Project/roxx.txt"
with open(inputFileName, 'rt', encoding='utf-8') as fileObject:
    DetectSentimenttext = fileObject.read()

polly = boto3.client('polly')

try:
    # response = polly.synthesize_speech(Text="how to use AWS text-to-speech (AWS Polly) service with AWS python boto3 module. It has clean code walk through and demo of using same.", OutputFormat="mp3", VoiceId="Joanna")
    # response = polly.synthesize_speech(Text=DetectSentimenttext, OutputFormat="mp3", VoiceId="Ivy")
    response = polly.synthesize_speech(Text=DetectSentimenttext, VoiceId='Aditi', OutputFormat='mp3', LanguageCode='hi-IN')

except (BotoCoreError, ClientError) as error:
    print(error)
    sys.exit(-1)
# print(Text)



# Access the audio stream from the response
if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "KUNDI.mp3")
            try:
            # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
            # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")
    sys.exit(-1)

# Play the audio using the platform's default player
if sys.platform == "win32":
    os.startfile(output)
else:
    # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, output])