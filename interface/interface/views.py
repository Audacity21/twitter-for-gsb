from django.shortcuts import render, redirect
import tweepy
import webbrowser
from django.contrib import messages
from .config import API_KEY , API_SECRET, auth


def index(request):
    return render(request,"index.html")

def login(request):
    redirect_url = auth.get_authorization_url()
    webbrowser.open(redirect_url)
    return render(request,"login.html")

def otp(request):
    otp = request.POST.get('otp')
    request.session['otp'] = otp
    return render(request,"text.html")

def text(request):
    key = request.session.get('otp')
    text = request.POST.get('text')
    request.session['text'] = text
    sendTweet(request, key, text)
    return render(request,"text.html")


def sendTweet(request, otp, txt):
    ACCESS_TOKEN, ACCESS_SECRET = auth.get_access_token(otp)
    client = tweepy.Client(consumer_key=API_KEY,consumer_secret=API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET)
    txt = request.POST.get('text')
    res = client.create_tweet(text = txt)
    print(res)
    messages.info(request,'Tweeted successfully')
