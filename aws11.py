import boto3
import json
# Settings
inputFileName='C:/Users/Admin/Desktop/aws1/aws1.txt'

# input the text to be translated from a file
with open(inputFileName, 'rt', encoding='utf-8') as fileObject:
    DetectSentimenttext = fileObject.read()

# carry out the translation
comprehend = boto3.client('comprehend','us-east-1')
print('Calling DetectSentiment')
sentiment = json.dumps(comprehend.detect_sentiment(Text=DetectSentimenttext, LanguageCode='en'), sort_keys=True, indent=4)
print(sentiment)
print('End of DetectSentiment\n')
