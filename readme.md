## Daniel Britt Project 2 Handin 2

### Theme :snowflake:
The theme for this chat application is what I call epichat!
It is a fun little chat app theme, that has an epic way of delivering messages to whoever is connected.

### Theme Incorporation :cyclone:
For incorporating the theme, I created a logo that says epichat and sits in the top left of the page.
The message box in the center is 50% of the screen, it shows the messages nicely displayed inside with hr under every message to separate them.
The gray background for the page I feel gives the chat a nice mood, and allows for long hours of chatting!

### Problems :anger:
There are two problems I am dealing with, which are more or less based off one another.
The main problem is that I cannot store two people logged into the chat app at once.
Sure, if another person logs in, they can send messages, but the second person overwrites the first person's login details.
The second problem based off this problem is that I don't have a constant user list, because I have no way of knowing who has logged in, and is still currently logged in.

### Improvements :heavy_plus_sign:
I would liked to have made the sections of my chat application look more like a chat app.
I could have achieved this by having different square sections throughout the site that has different kinds of information in it, like the user list, and login or out buttons.
It also would have been nice to have this implemented into an actual web page, with one part of the site having a chat area.

### Tools Used :hammer:
Cleverbot API | 
Amazon Polly | 
ReactJS | 
Flask | 
SocketIO

### Improvements from Handin 1 :heavy_check_mark:
Please regrade these sections from Handin 1

1. all messages received on server are relayed to all clients
    - 2 points, I believe the messages are sent to all the clients, I just tested it and it works.
2. all clients show new user on connect
    - 1 point, the bot says when a new user connects by saying, "Someone looged in from Google/Facebook"
3. all clients remove user on disconnect
    - 1 point, the number counter of how many people are connected increases and decreases based on when someone logs out and in.
4. all clients update count on disconnect
    - 1 point, the number counter at the top does work when someone logs out and in.
5. database is not SQLite	
    - 2 points, I fixed the database for this turnin.
6. messages are persisted via database
    - 3 points, the database works now and stores all messages.
7. users can only send messages after authentication
    - 1 point, the auth flow should work fine.