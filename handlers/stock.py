from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import lic_code
from text_info import last_message
from database.sqlite import create_profile, edit_profile


class Stock_activate(StatesGroup):
    waiting_for_right_code = State()
    waiting_for_name = State()
    waiting_for_phone_number = State()


# Обратите внимание: есть второй аргумент
async def stock_start(message: types.Message, state: FSMContext):
    await message.answer("Введите код из письма Деда Мороза:")
    await state.set_state(Stock_activate.waiting_for_right_code.state)


async def code_entered(message: types.Message, state: FSMContext):
    if not(len(message.text) == 7 and message.text.isdigit()):
        await message.answer("Пожалуйста, введите правильный код. (Код ошибки 001)")
        return
    if int(message.text) not in lic_code.db:
        await message.answer("Пожалуйста, введите правильный код. (Код ошибки 002)")
        return
    await state.update_data(code_entered=int(message.text))
    await state.set_state(Stock_activate.waiting_for_name.state)
    await create_profile(user_id=message.from_user.id)
    await message.answer("Напишите имя собственника карты МИРТЕК:")


async def name_entered(message: types.Message, state: FSMContext):
    await state.update_data(name_entered=message.text.lower())
    await state.set_state(Stock_activate.waiting_for_phone_number.state)
    await message.answer("Теперь введите номер телефона:")


async def phone_number_entered(message: types.Message, state: FSMContext):
    if not(len(message.text) == 10 and message.text.isdigit()):
        await message.reply("(Код ошибки 003)")
        await message.answer("Пожалуйста, введите правильный номер телефона.\nПример: 9234521103")
        return
    await state.update_data(phone_number_entered=message.text)
    user_data = await state.get_data()
    await message.answer(f"Вы активировали код {user_data['code_entered']}, на имя {user_data['name_entered']} "
                         f"по следующему номеру {user_data['phone_number_entered']}.")
    await edit_profile(state, user_id=message.from_user.id)
    await message.answer(f"{last_message}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_stock(dp: Dispatcher):
    dp.register_message_handler(stock_start, commands="ny_stock_2023", state="*")
    dp.register_message_handler(code_entered, state=Stock_activate.waiting_for_right_code)
    dp.register_message_handler(name_entered, state=Stock_activate.waiting_for_name)
    dp.register_message_handler(phone_number_entered, state=Stock_activate.waiting_for_phone_number)
