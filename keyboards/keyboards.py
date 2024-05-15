from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON

start_choice_yes_button: KeyboardButton = KeyboardButton(
    text=LEXICON['yes_button']
)

start_choice_no_button: KeyboardButton = KeyboardButton(
    text=LEXICON['no_button']
)

start_settings_button: KeyboardButton = KeyboardButton(
    text=LEXICON['start_settings_button']
)

settings: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[start_settings_button]],
                                    resize_keyboard=True)

start_choice: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[start_choice_yes_button],
                                              [start_choice_no_button]],
                                    resize_keyboard=True)

kb_builder_time: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
time_buttons: list[KeyboardButton] = [KeyboardButton(
                text=f'{i}:00') for i in range(24)]
kb_builder_time.row(*time_buttons, width=4)

button_1: KeyboardButton = KeyboardButton(text=LEXICON['write_button'])
button_2: KeyboardButton = KeyboardButton(text=LEXICON['settime_button'])
button_3: KeyboardButton = KeyboardButton(text=LEXICON['deletenotification_button'])
button_4: KeyboardButton = KeyboardButton(text=LEXICON['del_button'])
button_5: KeyboardButton = KeyboardButton(text=LEXICON['graphic_button'])
button_6: KeyboardButton = KeyboardButton(text=LEXICON['help_button'])

defualt_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_1],
                                              [button_2],
                                              [button_3],
                                              [button_4],
                                              [button_5],
                                              [button_6]],
                                    resize_keyboard=True)

kb_builder_mood: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
mood_buttons: list[KeyboardButton] = [KeyboardButton(
                text=str(i)) for i in range(1, 11)]
kb_builder_mood.row(*mood_buttons, width=3)
