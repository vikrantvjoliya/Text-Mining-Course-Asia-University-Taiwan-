import boto3
import json
import pandas as pd
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

import pickle

# Settings
data = "E:/KLU/3rd Year/Asia University/Final Project/amazon_tweets.csv"

df = pd.read_csv(data, header = None, dtype = 'str', encoding = 'utf-8') 

text = df.loc[1].item()
print(text)
print(" ")
print("##################### ANALYSIS#############################")

# carry out the translation
comprehend = boto3.client('comprehend','us-east-1')
print('Calling DetectSentiment')
sentiment = json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
print(sentiment)
print('End of DetectSentiment\n')

print('Calling DetectDominantLanguage')
print(json.dumps(comprehend.detect_dominant_language(Text = text), sort_keys=True, indent=4))
print("End of DetectDominantLanguage\n")

print('Calling DetectEntities')
print(json.dumps(comprehend.detect_entities(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectEntities\n')

print('Calling DetectKeyPhrases')
print(json.dumps(comprehend.detect_key_phrases(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectKeyPhrases\n')

print('Calling PII entities')
print(json.dumps(comprehend.detect_pii_entities(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of PII entities\n')

print('Calling DetectSyntax')
print(json.dumps(comprehend.detect_syntax(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectSyntax\n')


    
print("##############TRANSLATE################")    
client = boto3.client('translate', region_name="us-east-1")
# text = "Hola! Yo empecé aprendo Español hace dos mes en la escuela. Yo voy la universidad. Yo tratar estudioso Español tres hora todos los días para que yo saco mejor rápido. ¿Cosa algún yo debo hacer además construir mí vocabulario? Muchas veces yo estudioso la palabras solo para que yo construir mí voabulario rápido. Yo quiero empiezo leo el periódico Español la próxima semana. Por favor correcto algún la equivocaciónes yo hisciste. Gracias!"
result=client.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode="zh")
# print(result)
print("Translated text is :")
print(result['TranslatedText'])
print(type(result))


print("#################POLLY##################")
polly = boto3.client('polly','us-east-1')

try:
    # response = polly.synthesize_speech(Text="how to use AWS text-to-speech (AWS Polly) service with AWS python boto3 module. It has clean code walk through and demo of using same.", OutputFormat="mp3", VoiceId="Joanna")
    # response = polly.synthesize_speech(Text=result, OutputFormat="mp3", VoiceId="Joanna")
    # response = polly.synthesize_speech(Text=result['TranslatedText'], VoiceId='Zhiyu', OutputFormat='mp3', LanguageCode='cmn-CN')
    response = polly.synthesize_speech(Text=result['TranslatedText'], VoiceId='Zhiyu', OutputFormat='mp3', LanguageCode='cmn-CN')


except (BotoCoreError, ClientError) as error:
    print(error)
    sys.exit(-1)
# print(Text)
# Access the audio stream from the response
if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "ROX.mp3")
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
