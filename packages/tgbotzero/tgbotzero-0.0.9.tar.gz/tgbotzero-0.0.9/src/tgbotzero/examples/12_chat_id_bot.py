from tgbotzero import *

TOKEN = '123:tokenHereFromBotFatherInTelegram'


def on_message(msg: str, chat_id: int):
    return f"Текущий chat id: {chat_id}"


run_bot()
