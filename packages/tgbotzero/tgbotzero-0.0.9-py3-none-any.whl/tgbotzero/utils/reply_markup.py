import json
from typing import Union, Tuple, Optional

import telebot.types


class Button:
    button: telebot.types.InlineKeyboardButton

    def __init__(self, text: str, button_name: str, data=None):
        if type(button_name) != str or not ('on_button_' + button_name).isidentifier():
            raise ValueError('Имя кнопки должно состоять из букв, цифр и подчёркиваний, например, name = "left_button_1"')
        try:
            data = json.dumps(data, ensure_ascii=False)
        except Exception as e:
            raise ValueError('Данные в параметре data должны быть «простыми»: числа, строки, списки')
        callback_data = f'{button_name};{data}'
        if len(callback_data) > 64:
            raise ValueError('Данных в параметре data слишком много, столько не лезет :(')
        self.button = telebot.types.InlineKeyboardButton(text=text, callback_data=callback_data)


def to_reply_markup(buttons: list[Button]) -> Optional[telebot.types.InlineKeyboardMarkup]:
    if buttons:
        reply_markup = telebot.types.InlineKeyboardMarkup()
        for button in buttons:
            reply_markup.row(button.button)
    else:
        reply_markup = None
    return reply_markup
