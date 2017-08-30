import os, flask, flask_socketio, flask_sqlalchemy, requests
from random import randint
import json
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
import urlparse
session = Session(aws_access_key_id=os.getenv("accessKey"), aws_secret_access_key=os.getenv("secretKey"), region_name="us-west-2")
polly = session.client("polly")
#This is NOT A TESTO
#This is IS another test
#This is a fourth test
from flask import Response, request

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

import models

userCount = 0
name = ''
pic = ''
messageText = ''
userCount = 0
userList = []

@app.route('/')
def hello():
    return flask.render_template('index.html')

# Someone logged into facebook, emitted from scripts/login.js
@socketio.on('fbtoken')
def getFBinfo(token):
    botLogin("facebook")
    global userCount
    global name
    global pic
    print "someone logged into facebook!"
    print userList
    userCount = userCount + 1
    socketio.emit('userCount', {
        'num': userCount,
    })
    print "userCount"
    print userCount
    #Begin keeping track of people
    userList.append({"sid" : request.sid, "token": token['facebook_user_token']['accessToken']})
    # print "request sid is"
    # print request.sid
    
    for i in userList:
        # print i
        if i["sid"] == request.sid:
            response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + i["token"])        
    # print token['facebook_user_token']['signedRequest']
    # print token['facebook_user_token']['accessToken']
    
    json = response.json()
    #Add name to userList
    for i in userList:
        if i["sid"] == request.sid:
            i["name"] = json['name']
            i["pic"] = json['picture']['data']['url']
            name = i["name"]
            pic = i["pic"]
    print userList
    # print json
    print "ACTIVATING LOGOUT BUTTON FOR FB"
    flask_socketio.emit("sendFB", {
        'data': '',
    })
    
@socketio.on('onfbtoken')
def fbon():
    flask_socketio.emit("sendFB", {
        'data': 'fbtoken received',
    })
# Someone logged out from facebook, emitted from scripts/login.js
@socketio.on('fblogout') 
def fblogout():
    botLogout("facebook")
    global userCount
    userCount = userCount - 1
    print "userCount"
    print userCount
    #Remove user from list
    for i in userList:
        if i["sid"] == request.sid:
            userList.remove(i)
    socketio.emit('userCount', {
        'num': userCount,
    })
    print "logging out"
    flask_socketio.emit('fblogout', {
        'data': ''
    })
    
@socketio.on('onfblogout')
def fbout():
    flask_socketio.emit("sendFB", {
        'data': 'fbtoken removed',
    })
    
# Someone logged into google, emitted from scripts/login.js
@socketio.on('googleToken')
def googleLogin(token):
    botLogin("google")
    global userCount
    #global name
    #global pic

    print "someone logged into google!"
    userCount = userCount + 1
    print "userCount"
    print userCount
    socketio.emit('userCount', {
        'num': userCount,
    })
    userList.append({"sid":request.sid, "name":token['gName'], "pic":token['gImage']})
    for i in userList:
        # print i
        if i["sid"] == request.sid:
            name = i['name']
            pic = i['pic']
    print "ABOUT TO ACTIVATE GOOGLE LOGOUT BUTTON"
    flask_socketio.emit("glogin", {
        'data': '',
    })
    
@socketio.on('ongtoken')
def gon():
    flask_socketio.emit("sendG", {
        'data': 'gtoken received',
    })
    
# Someone logged out from google, emitted from scripts/login.js
@socketio.on('glogout')
def gLogout():
    botLogout("google")
    global userCount
    userCount = userCount - 1
    print "userCount"
    print userCount
    socketio.emit('userCount', {
        'num': userCount,
    })
    print "logging out"
    #Remove user from list
    for i in userList:
        if i["sid"] == request.sid:
            userList.remove(i)
    flask_socketio.emit('glogout', {
        'data': ''
    })
    
@socketio.on('onglogout')
def gout():
    flask_socketio.emit("removeG", {
        'data': 'gtoken removed',
    })
    
# When page loads, send usercount, and messages, if it's not empty(which causes bugs if it is empty)
@socketio.on('pageLoad')
def pageLoad():
    print "pageLoad"
    global userCount
    socketio.emit('userCount', {
        'num': userCount,
    })
    print "sent userCount"
    messages = getMessages()
    if len(messages) > 0:
        flask_socketio.emit('messageSend', {
            'list': messages,
        })
        
def didPageLoad():
    return "PAGE LOADED"
# Get messages from database
def getMessages():
    messageList = []
    print "BEGIN"
    # error below doesn't matter, it's a c9 issue
    messageQuery = models.Message.query.all()
    for i in range (0, len(messageQuery)):
        message = { 'message':messageQuery[i].message,'name':messageQuery[i].name,'pic':messageQuery[i].pic}
        messageList.append(message)
    return messageList

# When the server recieves a message, emited from scripts/input.js
@socketio.on('message')
def message(message):
    # global name
    # global pic
    for i in userList:
        if i['sid'] == request.sid:
            name = i["name"]
            pic = i["pic"]
    global messageText
    print "request sid is"
    print request.sid
    messageText = message['data']
    parts = urlparse.urlsplit(messageText)
    if not parts.scheme or not parts.netloc:  
        print "not an url"
    else:
        print "yes an url"
        messageText = "<a" + messageText
    inputMessage(name, pic, messageText)

# Input messages into db
def inputMessage(name, pic, messageText):
    print "entered inputMessage"
    print name
    print pic
    print messageText
    chatMessage = models.Message(messageText, name, pic)
    #Errors below also don't matter. Another c9 issue.
    models.db.session.add(chatMessage)
    models.db.session.commit()
    messages = getMessages()
    print "MESSAGE"
    print messageText
    socketio.emit('messageSend', {
        'list': messages,
    })
    if messageText[:2] == "!!":
        print "GOING TO BOT FUNCTION"
        if "!! about" in messageText:
            message = "I am a bot for Daniel's Chatroom. I provide help, humor, and, well more humor."
            name  ="epichatBot"
            pic = "https://revlo-public-us-west.s3-us-west-2.amazonaws.com/reward_images/064d017e-86a4-4d12-abd2-e714d2baa9ce/nightbot-profile_image-b575592fb15cf224-300x300.png"
            inputMessage(name, pic, message)
        elif "!! help" in messageText:
            message = "Try typing '!! about', '!! help', '!! say', '!! joke', '!! name'"
            name = "epichatBot" 
            pic = "https://revlo-public-us-west.s3-us-west-2.amazonaws.com/reward_images/064d017e-86a4-4d12-abd2-e714d2baa9ce/nightbot-profile_image-b575592fb15cf224-300x300.png"
            inputMessage(name, pic, message)
        elif "!! say" in messageText:
            text = messageText[6:]
            
            print "GOING TO /READ"
            socketio.emit('player', {
                "text":text
            })
        elif "!! joke" in messageText:
            ran = randint(0,4)
            if ran == 0:
                text = "I dreamt I was forced to eat a giant marshmallow. When I woke up, my pillow was gone."
            if ran == 1:
                text = "Police officer: 'Can you identify yourself, sir?' Driver pulls out his mirror and says: 'Yes, it's me.'"
            if ran == 2:
                text = "What do you get when you cross-breed a cow and a shark? I don't know, but I wouldn't enjoy milking it."
            if ran == 3:
                text = "In a boomerang shop: 'I'd like to buy a new boomerang please. Also, can you tell me how to throw the old one away?'"
            if ran == 4:
                text = "My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away."
            message = text
            name = "epichatBot"
            pic = "https://revlo-public-us-west.s3-us-west-2.amazonaws.com/reward_images/064d017e-86a4-4d12-abd2-e714d2baa9ce/nightbot-profile_image-b575592fb15cf224-300x300.png"
            inputMessage(name, pic, message)
        elif "!! name" in messageText:
            message = "My name? You ask my name? Why do you care about my name??!! But if you really want to know, it's epichatobotonomifoldiroznorishomnifacious. "
            name = "epichatBot"
            pic = "https://revlo-public-us-west.s3-us-west-2.amazonaws.com/reward_images/064d017e-86a4-4d12-abd2-e714d2baa9ce/nightbot-profile_image-b575592fb15cf224-300x300.png"
            inputMessage(name, pic, message)
        else:
            message = "Unrecognized command... Did you even read the help manual?"
            name = "epichatBot"
            pic = "https://revlo-public-us-west.s3-us-west-2.amazonaws.com/reward_images/064d017e-86a4-4d12-abd2-e714d2baa9ce/nightbot-profile_image-b575592fb15cf224-300x300.png"
            inputMessage(name, pic, message)

@socketio.on('botDone')
def bot():
    flask_socketio.emit("botFinished", {
        'data': 'bot complete',
    })
# The talking part of the bot, amazon polly and cleverbot
@app.route("/read")
def reader():
    print "IN READ"
    input = flask.request.args.get('text', "not set")
    url = "http://www.cleverbot.com/getreply"
    key = os.getenv("cleverKey")
    cs = "80nxdxIJO2BxCBF2VYdDMLZXRVdRQJYxR2JxN4A4MxA2NwE2C2E0aXFoY0VgazFgevF1cgYuYtVlPJcAAAA"
    reply = "ProcessReply"
    payload = {
        "key":key,
        "input":input,
        "cs":cs,
        "reply":reply
    }
    r = requests.get(url, params=payload)
    robot = r.json()['output']
    message = "Bot says: " + robot
    name = "epichatBot"
    pic = "https://revlo-public-us-west.s3-us-west-2.amazonaws.com/reward_images/064d017e-86a4-4d12-abd2-e714d2baa9ce/nightbot-profile_image-b575592fb15cf224-300x300.png"
    inputMessage(name, pic, message)
    # text = """Call me Ishmael. Some years ago--never mind how long precisely--having
    #     little or no money in my purse, and nothing particular to interest me on
    #     shore, I thought I would sail about a little and see the watery part of
    #     the world. It is a way I have of driving off the spleen and regulating
    #     the circulation. Whenever I find myself growing grim about the mouth;
    #     whenever it is a damp, drizzly November in my soul; whenever I find
    #     myself involuntarily pausing before coffin warehouses, and bringing up
    #     the rear of every funeral I meet; and especially whenever my hypos get
    #     such an upper hand of me, that it requires a strong moral principle to
    #     prevent me from deliberately stepping into the street, and methodically
    #     knocking people's hats off--then, I account it high time to get to sea
    #     as soon as I can. This is my substitute for pistol and ball. With a
    #     philosophical flourish Cato throws himself upon his sword; I quietly
    #     take to the ship. There is nothing surprising in this. If they but knew
    #     it, almost all men in their degree, some time or other, cherish very
    #     nearly the same feelings towards the ocean with me."""
    voiceId = "Joanna"
    outputFormat = 'mp3'
    """Geraint | Gwyneth | Mads | Naja | Hans | Marlene | Nicole | Russell | Amy | 
    Brian | Emma | Raveena | Ivy | Joanna | Joey | Justin | Kendra | Kimberly | 
    Salli | Conchita | Enrique | Miguel | Penelope | Chantal | Celine | Mathieu | 
    Dora | Karl | Carla | Giorgio | Mizuki | Liv | Lotte | Ruben | Ewa | Jacek | 
    Jan | Maja | Ricardo | Vitoria | Cristiano | Ines | Carmen | Maxim | Tatyana | 
    Astrid | Filiz"""
    
    response = polly.synthesize_speech(Text=robot, VoiceId=voiceId, OutputFormat=outputFormat)
    print response
    def generate():
        fogg = response["AudioStream"]
        data = fogg.read(1024)
        while data:
            yield data
            data = fogg.read(1024)
    return Response(generate(), mimetype="audio/mpeg")
    
def readerDone():
    return "READER DONE"

def botResponse(text):
    if "!! about" in text:
        return "finished bot about"
    elif "!! help" in text:
        return "finished bot help"
    elif "!! say" in text:
        return "finished bot say"
    elif "!! joke" in text:
        return "finished bot joke"
    elif "!! name" in text:
        return "finished bot name"
    else:
        return "finished bot unrecognized"

# The bot tells the client who logged in, and from where
def botLogin(which):
    print which
    message = "Someone logged in from " + which
    name = "epichatBot"
    pic = "https://revlo-public-us-west.s3-us-west-2.amazonaws.com/reward_images/064d017e-86a4-4d12-abd2-e714d2baa9ce/nightbot-profile_image-b575592fb15cf224-300x300.png"
    inputMessage(name, pic, message)
# The bot tells the client who logged out, and from where
def botLogout(which):
    print which
    message = "Someone logged out from " + which, 
    name = "epichatBot"
    pic = "https://revlo-public-us-west.s3-us-west-2.amazonaws.com/reward_images/064d017e-86a4-4d12-abd2-e714d2baa9ce/nightbot-profile_image-b575592fb15cf224-300x300.png"
    inputMessage(name, pic, message)

# On connect
@socketio.on('connect')
def on_connect():
    global userCount
    print 'Someone connected!'
    
def connect():
    return "CONNECTED"

# On disconnect
@socketio.on('disconnect')
def on_disconnect():
    global userCount
    print "Someone Disconnected"
def disconnect():
    return "DISCONNECTED"

if __name__ == '__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080))
        # debug=True
    )