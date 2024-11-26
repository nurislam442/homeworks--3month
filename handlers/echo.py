from aiogram import types, Dispatcher

async def echo_handler_for_str(message: types.Message):
    if message.text.isdigit():
        message.text = int(message.text)
        await message.answer(message.text**2)
    else:
        await message.answer(message.text)

def register_echo_handler(dp: Dispatcher):
    dp.register_message_handler(echo_handler_for_str)