from flask import Flask, request, redirect
import json
import requests
import re
from google.cloud import translate
import urllib.request as urllib
from twilio.twiml.messaging_response import Message, MessagingResponse

app = Flask(__name__)

#User latitude and longitude--hard-coded to Rutgers student center for now
userlat = 40.5055
userlon = -74.45188903808594

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    #get info about the users's incoming message
    message = request.form['Body']

    if "SMSnet" in lower( message)
    
    responseParas = urlToParagraphs(message_body)
    responseStr = responseParas[0]
    
    #Construct a response message
    resp = MessagingResponse()
    resp.message(responseStr)
    print(responseStr)
    return str(resp)


def searchResults(query):
    #Searches Google
    r = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyDUWG4it4VI2Q-OfjuO0_sKAqNV1MxU7Xg&cx=016941051599191875790:7bkp8je7amz&q="+query)

    searchResultsStr = json.loads(r.text)["items"]
    searchResults = []
    for i in range(3):
        searchResults.append({"title" : searchResultsStr[i]["title"],
            "website" : searchResultsStr[i]["displayLink"],
            "snippet" : searchResultsStr[i]["snippet"],
            "url" : searchResultsStr[i]["formattedUrl"]})

    c = 1
    responseStr = ""
    for item in searchResults:
        responseStr += str(c) + ") "
        responseStr += item["title"] + "\n" + item["snippet"].strip('\n') + "\n" + item["website"]
        responseStr += "\n"
        c += 1
    return searchResults, responseStr


def urlToParagraphs(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.Request(url, headers=headers)
        resp = urllib.urlopen(req)
        respData = resp.read()
        paragraphs = re.findall(r'<p>(.*?)</p>', str(respData))
        parsed = []

        for para in paragraphs:
            a = re.sub(r'\<[^>]*\>', '', para)
            b = re.sub(r'&#9.*?93;', '', a)
            c = b.replace('\\n', '')
            parsed.append(c)
        return parsed

    except Exception as e:
        print(str(e))
        return []


def translate(text, targetLang):
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=targetLang)
    return translation


if __name__ == "__main__":
    app.run(debug=True)
