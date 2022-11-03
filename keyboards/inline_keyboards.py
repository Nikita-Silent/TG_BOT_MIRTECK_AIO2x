from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from text_info import url, text_of_the_button_subscribe, all_commands, list_of_commands_info, start_list_of_commands, \
    text_of_the_button_subscribe_done

# Клавиатура по коммандам
keyboard_start_list_of_commands = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start_list_of_commands.add(*start_list_of_commands)
keyboard_of_list_of_commands = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_of_list_of_commands.add(*all_commands)

# Кнопка уже подписался
btnDoneSub = InlineKeyboardMarkup(text=text_of_the_button_subscribe_done, callback_data='done')
# Кнопка сабскрайба
btnUrlChannel = InlineKeyboardButton(text=text_of_the_button_subscribe, url=url)

# Клавиатура на старте бота
check_sub_menu = InlineKeyboardMarkup(row_width=1)
check_sub_menu.insert(btnUrlChannel)
check_sub_menu.insert(btnDoneSub)

