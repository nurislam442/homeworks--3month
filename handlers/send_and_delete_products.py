from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import db_main
from aiogram.types import InputMediaPhoto


async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_all = types.InlineKeyboardButton('Вывести все товары', callback_data='all_delete_hand')
    button_one = types.InlineKeyboardButton('Вывести по одному', callback_data='one')
    keyboard.add(button_all, button_one)
    await message.answer('Выберите как отправить товары:', reply_markup=keyboard)

async def send_all_delete_products(callback_query: types.CallbackQuery):
    products = db_main.fetch_all_products()
    if products:
        for product in products:
            caption = (f"Заполненный товар:\n"
                       f"Название - {product[3]}\n"
                       f"Артикул - {product[0]}\n"
                       f"Размер - {product[4]}\n"
                       f"Цена - {product[5]}\n"
                       f"Информация о товаре - {product[2]}\n"
                       f"Категория - {product[1]}\n")
            delete_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
            delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product[0]}')
            delete_keyboard.add(delete_button)
            await callback_query.message.answer_photo(
                photo=product[6],
                caption=caption,
                reply_markup=delete_keyboard
            )
        else:
            await callback_query.message.answer(text='В базе больше нет товаров')
async def delete_all_products(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data.split('_')[1])
    db_main.delete_product(product_id)
    if callback_query.message.photo:
        new_caption = 'Товар удален. Обновите список!'
        photo_404 = open('media/img_2.png', 'rb')
        await callback_query.message.edit_media(
            InputMediaPhoto(media=photo_404, caption=new_caption)
        )
    else:
        await callback_query.message.edit_text('Товар был удален. Обновите список')
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['send_delete_products'])
    dp.register_callback_query_handler(send_all_delete_products, Text(equals='all_delete_hand'))
    dp.register_callback_query_handler(delete_all_products, Text(startswith='delete_'))