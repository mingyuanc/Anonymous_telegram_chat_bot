import os
import time
import telebot.types
from telebot import TeleBot
from flask import Flask, request
from util import Telebot_utils


util = Telebot_utils()
bot = TeleBot(util.api)
server = Flask(__name__)


@bot.message_handler(commands=["start"])
def command_help(message):
    username = str(message.chat.username)
    user_first = str(message.chat.first_name)
    user_last = str(message.chat.last_name)
    chat_id = message.chat.id
    util.log_user(chat_id, username, user_first, user_last)
    bot.reply_to(
        message,
        """Hello!, this is a anonymous chat bot that
                             matches you with local students.\n
                             Press /search to start, /quit to leave the
                             chat and /report to report a user.
                             \nDo read /help before begining.
                             \nHappy chatting!""",
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            "Message the developer", url="https://t.me/Mingyuannnn"
        )
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            "Message the developer anonymously", callback_data="msgdev"
        )
    )
    bot.send_message(
        message.chat.id,
        """1) To start a random chat /search.\n
        2) Once a match is found a prompt would
         be sent and you can start to chat!\n
        3) You can /quit at anytime to leave
         the queue or leave the chat \n
        4) This bot supports the sending of audio
         files, stickers, pictures and videos \n
        5) /report to report a user. Once a new
         chat has been started(/search) you cannot
         report the previous user \n""",
    )
    bot.send_message(
        message.chat.id,
        """6) You can message me anonymously at anytime by
         pressing the button below or by /messagedev""",
        reply_markup=keyboard,
    )


@bot.message_handler(commands=["messagedev"])
def msgdev1(message):
    chat_id = message.chat.id
    msg = bot.send_message(
        chat_id,
        """what message do you wish to send the dev?\n
        Only one message would be sent at a time.""",
    )
    bot.register_next_step_handler(msg, msgdev2)


@bot.callback_query_handler(func=lambda call: True)
def msgdev(call):
    bot.answer_callback_query(call.id)
    msg = bot.send_message(
        call.message.chat.id,
        """what message do you wish to send the dev?\n
        Only one message would be sent at a time.""",
    )
    bot.register_next_step_handler(msg, msgdev2)


def msgdev2(message):
    bot.send_message(244202108, message.text)
    chat_id = message.chat.id
    bot.send_message(chat_id, "message sent successfully!")


@bot.message_handler(commands=["trick"])
def trick(message):
    chat_id = message.chat.id
    db = util.returnall(chat_id)
    rl = util.returnreported(chat_id)
    if db is False or rl is False:
        bot.send_message(chat_id, "Sorry i do not understand this command.")
    else:
        bot.send_message(chat_id, "db")
        bot.send_message(chat_id, db)
        bot.send_message(chat_id, "reported list")
        bot.send_message(chat_id, rl)


@bot.message_handler(commands=["send"])
def send(message):
    chat_id = message.chat.id
    if chat_id == util.admin_id:
        msg = bot.reply_to(message, "which chat_id do you which to chat to")
        bot.register_next_step_handler(msg, send_message)
    else:
        bot.reply_to(message, "Sorry i do not understand this command.")


def send_message(message):
    try:
        msg_id = int(message.text)
        msg = bot.reply_to(message, "what message do you wish to send?")
        bot.register_next_step_handler(msg, ls, msg_id)
    except Exception as e:
        bot.send_message(util.admin_id, str(e))
        bot.reply_to(message, "calm down too many messages.")


def ls(message, msg_id):
    try:
        text = str(message.text)
        chat_id = message.chat.id
        bot.send_message(msg_id, text)
        bot.send_message(chat_id, "message successfully sent")
    except Exception as e:
        bot.send_message(util.admin_id, f"debug {chat_id}: {e}: /send")  # type: ignore


@bot.message_handler(commands=["report"])
def report(message):
    chat_id = message.chat.id
    if util.report1(chat_id):
        bot.send_message(chat_id, "report sent successfully")
        bot.send_message(
            chat_id,
            """You can send screenshots of the chat to me to
             aid with the reporting process""",
        )
    else:
        bot.send_message(chat_id, "Error nobody to report")


@bot.message_handler(commands=["search"])
def matchmake_1(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Searching... /quit to leave the queue at anytime")
    bot.send_chat_action(chat_id, "typing")
    if util.found(chat_id):
        bot.reply_to(
            message,
            """Sorry it seems that you are
             currently searching or in a chat""",
        )
    else:
        if not util.matchmake(chat_id):
            util.requeue(chat_id)
            util.remove_queue(chat_id)
            bot.send_message(
                chat_id, "some error has occurred please requeue with /search"
            )
        else:
            while util.getid(chat_id) == chat_id:
                time.sleep(1)
                if not util.inchating(chat_id):
                    break
            if util.inchating(chat_id):
                chatto = util.getid(chat_id)
                bot.send_message(util.admin_id, f"{chat_id} is chating with {chatto}")
                bot.send_message(
                    chat_id,
                    """Found, you can start chating now /quit to leave the chat
                     at anytime""",
                )


@bot.message_handler(commands=["quit"])
def quit(message):
    chat_id = message.chat.id
    # check if in a chat
    # if not in chat
    if chat_id == util.getid(chat_id):
        if util.inchating(chat_id):
            util.requeue(chat_id)
            util.remove_queue(chat_id)
            bot.reply_to(message, "Quiting...")
        else:
            bot.reply_to(message, "/search to queue for a chat")
    # if in chat
    else:
        bot.reply_to(message, "/search to queue for another chat")
        bot.send_message(
            util.getid(chat_id),
            "user has left the chat , /search to queue for another chat",
        )
        util.requeue(chat_id)
        util.requeue(util.getid(chat_id))
        util.exit(chat_id, util.getid(chat_id))


@bot.message_handler(func=lambda m: True)
@bot.message_handler(content_types=["audio", "sticker", "photo", "video"])
def reply(message):
    chat_id = message.chat.id
    if util.getid(chat_id) == chat_id:
        bot.send_message(chat_id, "/search to queue for another chat")
    else:
        bot.forward_message(2137218499, chat_id, message.message_id)
        if message.content_type == "photo":
            reply = message.photo[0].file_id
            bot.send_photo(util.getid(chat_id), reply)
        elif message.content_type == "audio":
            reply = message.audio.file_id
            bot.send_audio(util.getid(chat_id), reply)
        elif message.content_type == "video":
            reply = message.video.file_id
            bot.send_video(util.getid(chat_id), reply)
        elif message.content_type == "sticker":
            reply = message.sticker.file_id
            bot.send_sticker(util.getid(chat_id), reply)
        else:
            bot.send_message(util.getid(chat_id), message.text)


@server.route("/" + util.api, methods=["POST"])
def getMessage():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://sgchattrial.herokuapp.com/" + util.api)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
