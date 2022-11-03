from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from text_info import welcome_message, help_answer_message, if_not_in_channel, tg_url, list_of_commands_info
from app.config_reader import load_config
from keyboards.inline_keyboards import check_sub_menu, keyboard_of_list_of_commands, keyboard_start_list_of_commands

config = load_config("config/bot.ini")
bot = Bot(token=config.tg_bot.token)


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    channel = await bot.get_chat(tg_url)
    if check_sub_channel(chat_member=await bot.get_chat_member(channel.id, message.from_user.id)):
        await message.answer(welcome_message, reply_markup=keyboard_start_list_of_commands)
    else:
        await message.answer(if_not_in_channel, reply_markup=check_sub_menu)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


async def cmd_help(message: types.Message):
    await message.answer(help_answer_message, reply_markup=types.ReplyKeyboardRemove())


async def list_of_commands(message: types.Message):
    await message.answer(list_of_commands_info, reply_markup=keyboard_of_list_of_commands)


# Просто функция, которая доступна только администратору, чей ID указан в файле конфигурации.
async def secret_command(message: types.Message):
    await message.answer("Поздравляю! Вы - клоун!")


def check_sub_channel(chat_member):
    if chat_member["status"] != 'left':
        return True
    else:
        return False


async def sub_channel_done(call: types.CallbackQuery):
    await call.answer(text="Спасибо, что подписались на канал!", show_alert=True)
    await call.message.answer(welcome_message, reply_markup=keyboard_start_list_of_commands)


def register_handlers_common(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(list_of_commands, commands="list_of_commands", state="*")
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands="admin")


def register_callbacks_handler(dp: Dispatcher):
    dp.register_callback_query_handler(sub_channel_done, text='done')
