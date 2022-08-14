import logging
import psycopg2  # type: ignore
import telebot  # type: ignore
from threading import Lock
from api_config import APIConfig


class Telebot_utils:
    def __init__(self) -> None:
        _logger = logging.basicConfig(level=logging.INFO)
        config = APIConfig(logger=_logger).config
        self.conn = psycopg2.connect(
            host=config["SQL_HOST"],
            database=config["SQL_DATABASE"],
            user=config["SQL_USER"],
            password=config["SQL_PASSWORD"],
            port=config["SQL_PORT"],
        )
        self.api = config["TELEGRAM_API"]
        self.admin_id = config["ADMIN_ID"]
        self.c = self.conn.cursor()
        self.lock = Lock()
        self.queue = []
        self.chating = []
        self.pairs = {}
        self.temppairs = {}
        self.bot = telebot.TeleBot(config["TELEGRAM_API"])

    def log_user(self, chat_id, username: str, user_first: str, user_last: str):
        self.c.execute("SELECT * FROM botuser where user_id=(%s);", (chat_id,))
        results = self.c.fetchall()
        if len(results) == 0:
            self.c.execute(
                "INSERT INTO botuser (user_id , username ,user_first , user_last) VALUES (%s,%s,%s,%s);",
                (chat_id, username, user_first, user_last),
            )
            self.conn.commit()
            return True
        else:
            return False

    def returnall(self, chat_id: int):
        if chat_id == self.admin_id:
            self.c.execute("SELECT * from botuser;")
            db = str(self.c.fetchall())
            return db
        else:
            return False

    def returnreported(self, chat_id: int):
        if chat_id == self.admin_id:
            self.c.execute("SELECT * from reportlist;")
            rl = str(self.c.fetchall())
            return rl
        else:
            return False

    def found(self, chat_id: int):
        if chat_id in self.chating:
            return True
        else:
            self.chating.append(chat_id)

    def requeue(self, chat_id: int):
        try:
            self.chating.remove(chat_id)

            return
        except Exception as e:
            self.bot.send_message(self.admin_id, f"debug {chat_id} : {e} : requeue")

    def getid(self, chat_id: int):
        if self.pairs.get(chat_id) is None:
            return chat_id
        else:
            return self.pairs[chat_id]

    def remove_queue(self, chat_id: int):
        if chat_id in self.queue:
            self.lock.acquire()
            self.queue.remove(chat_id)
            self.lock.release()
        return

    def exit(self, chat_id: int, chat_to: int):
        try:
            del self.pairs[chat_id]
            del self.pairs[chat_to]
            return
        except Exception as e:
            self.bot.send_message(self.admin_id, f"debug {chat_id} : {e} : exit")

    def matchmake(self, chat_id: int):
        if chat_id in self.queue:
            return False
        self.lock.acquire()
        if self.temppairs.get(chat_id) is not None:
            self.deletmpairs(chat_id)
        self.queue.append(chat_id)
        if len(self.queue) == 2:
            self.pairs[chat_id] = self.queue[0]
            self.temppairs[chat_id] = self.queue[0]
            self.pairs[self.queue[0]] = chat_id
            self.temppairs[self.queue[0]] = chat_id
            del self.queue[:]
        self.lock.release()
        return True

    def deletmpairs(self, chat_id: int):
        del self.temppairs[chat_id]

    def inchating(self, chat_id: int):
        if chat_id in self.chating:
            return True
        else:
            return False

    def report1(self, chat_id: int):
        if self.inchating(chat_id):
            self.reportlog(self.getid(chat_id), chat_id)
            return True
        else:
            if self.temppairs.get(chat_id) is None:
                return False
            self.reportlog(self.temppairs[chat_id], chat_id)
            return True

    def reportlog(self, reported: int, reporter: int):
        self.c.execute(
            "INSERT INTO reportlist(reported_id , reporter_id ) VALUES (%s,%s);",
            (reported, reporter),
        )
        self.conn.commit()
