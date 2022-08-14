# Anonymous telegram chat bot
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

# Overview
A telegram chat bot that matches random strangers together and provide a platform for them to engage in anonymous chat in the safety of telegram's platform. This bot is mainly coded in python and uses the Pytelegrambot library with PostgreSQL database and hosted on heroku. This bot matches two online strangers and allows them to send messages, stickers, videos and pictures to on another without ever exposing their identity unless they wish to. The chat is ended whenever anyone uses the /quit command. Users are also able to report other users that violates the rules.

## Features
- Users are able to be randomly matched at anytime of the day
- Users are not required to provide any personal information to work
- Users are able to end the chat at any point in time should they feel the need to
- Users are also able to report their chat partner even after their chat has ended, granted the user has not started a new chat
- Users can message the developer anonymously in the /messagedev command
- Programme is containerised and is currently hosted on Heroku

# State of the project
All the features have been completed and tested throughly to the best of my abilities. The bot is out of development and fully in production

> 

# How does it work
Users upon pressing start would be presented with a welcome message that introduce how the bot works. For more detailed instructions, the user can use the command "/help" at any point in time. Users can start a new chat by the "/search", then the user would be added to a queue to be matched to the next user. I created a matchmaking algorithm specifically for this use case. The matchmaking algorithm is built upon a queue that automatically matches users. At any point in time, users can use "/quit" to leave the queue or the chat. Users can also use "/report" to report their current chat partner or their previous chat partner. Due to the nature of this bot, it is built to be thread safe.

By editing the environment variables, the user can set their own chat_id as the bot admin. By becoming the bot admin, the user can access developer command which are /trick and /send.

## Commands

### /start
Initialise the bot and sends a short welcome message depicting how to use the bot

### /help
Sends a more detailed instruction message that also contains a link to start a anonymous/private chat with the developer 

### /search
Places the users in the queue to be matched

### /quit
Removes the user from the queue or the chat respectively

### /report
Sends a report to the developer. The reporter and reported ID is stored for investigation 

### /messagedev
Allows the user to secretly and anonymously send a message to the developer

## Bot admin commands

###/trick
Returns the database of the users using the bot and the database of all the reported users. The database would contain their user_id, user_name and time_reported among other information.

###/send
Allows the bot admin to message one of users of the bot

# Usage
1) Get an bot API key from this [link](https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0)
2) Clone the repository and replace the required environmental variable
3) You can run the code locally or in docker using the appropriate docker run command
4) Once your ready to deploy you can deploy to Heroku by following the guide [here](https://devcenter.heroku.com/articles/getting-started-with-python)

# contact 
Ching ming yuan - cmingyuan123@gmail.com - [LinkedIn](https://www.linkedin.com/in/ming-yuan-ching-9290a322b/)

