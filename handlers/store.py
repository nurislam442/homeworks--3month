from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import buttons
from db import db_main

from buttons import cancel, size_keyboard

class store(StatesGroup):
    product_name = State()
    size = State()
    price = State()
    category = State()
    product_photo = State()

    collection = State()
    info_product = State()
    productid = State()
    Submit = State()

async def start_fsm(message: types.Message):
    await message.answer("введите название товара:", reply_markup=cancel)
    await store.product_name.set()

async def load_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await store.next()
    await message.answer("введите/выберите размер товара:", reply_markup=size_keyboard())
async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await store.next()
    await message.answer("введите цену товара:", reply_markup=cancel)

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await store.next()
    await message.answer("введите категорию товара:", reply_markup=cancel)

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await store.next()
    await message.answer("отправьте фото товара", reply_markup=cancel)

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_photo'] = message.photo[-1].file_id
    await store.next()
    await message.answer('введите колекцию товара:', reply_markup=cancel)
async def load_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text
    await store.next()
    await message.answer('введите информацию о продукте:')

async def load_info_product(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['infoproduct'] = message.text
    await store.next()
    await message.answer('введите айди продукта:')
async def load_productid(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit():
            data['productid'] = message.text
            await message.answer_photo(photo=data['product_photo'], caption=f"имя товара - {data['product_name']}\n"
                                                                            f"размер товра - {data['size']}\n"
                                                                            f"цена товара - {data['price']}\n"
                                                                            f"категория товара - {data['category']}\n"
                                                                            f"коллекция товара - {data['collection']}\n"
                                                                            f"информация о товаре - {data['infoproduct']}\n"
                                                                            f"айди продукта - {data['productid']}")
            await message.answer("верны ли данные?(да/нет)", reply_markup=buttons.submit)
            await store.next()
        else:
            await message.answer("вводите только цифры:")




async def submit(message: types.Message, state=FSMContext):
    if message.text.lower() == 'да':
        kb_remove = types.ReplyKeyboardRemove()
        await message.answer('Отлично, товар в базе!', reply_markup=kb_remove)

        async with state.proxy() as data:
            await db_main.sql_insert_store_to_collection_products(
                productid=data['productid'],
                collection=data['collection']
            )
        async with state.proxy() as data:
            await db_main.sql_insert_store(
                name_product=data['product_name'],
                product_id=data['productid'],
                size=data['size'],
                price=data['price'],
                photo=data['product_photo'],
                )

            await db_main.sql_insert_store_to_product_details(
                productid=data['productid'],
                category=data['category'],
                infoproduct=data['infoproduct']
            )
        await state.finish()

    elif message.text.lower() == 'нет':
        kb_remove = types.ReplyKeyboardRemove()
        await message.answer('Отменено!', reply_markup=kb_remove)
        await state.finish()
    else:
        await message.answer('Введите Да или Нет')
        await state.finish()




def reg_handler_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True),
                                state="*")

async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('отменено')

def reg_handler_fsm_registration(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(start_fsm, commands=['registration'])

    dp.register_message_handler(load_product_name, state=store.product_name)
    dp.register_message_handler(load_size, state=store.size)
    dp.register_message_handler(load_price, state=store.price)
    dp.register_message_handler(load_category, state=store.category)

    dp.register_message_handler(load_photo,state=store.product_photo, content_types=["photo"])
    dp.register_message_handler(load_collection, state=store.collection)
    dp.register_message_handler(load_info_product, state=store.info_product)
    dp.register_message_handler(load_productid, state=store.productid)
    dp.register_message_handler(submit, state=store.Submit)
