import asyncio
import logging

from aiogram import Bot, Dispatcher, types, html, F
from aiogram.filters import Text
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.types import FSInputFile, BufferedInputFile, URLInputFile
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.utils.markdown import hide_link
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder
from config_reader import config
from datetime import datetime
from random import randint
import os
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from typing import Optional
from magic_filter import F


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher()

# старт бота
# @dp.message(Command('start'))
# async def cmd_start(message: types.Message):
#     await message.answer('Hello')


# текстовой ответ на команду
@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


# отправка стикера кости
@dp.message(Command('dice'))
async def cmd_dice(message: types.Message, bot: Bot):
    await bot.send_dice(5102838218, emoji=DiceEmoji.DICE)

# создание списка, добавление элемента в список
# mylist = [1, 2, 3]
#
#
# @dp.message(Command('add_to_list'))
# async def add_to_list(message: types.Message):
#     mylist.append(7)
#     await message.answer('Added the number 7')


# показ содержимого списка
# @dp.message(Command('show_list'))
# async def show_list(message: types.Message):
#     await message.answer(f'Your list: {mylist}')


# форматированный текст
@dp.message(Command('test4'))
async def cmd_test4(message: types.Message):
    await message.answer('Hello, <b>World</b>', parse_mode='HTML')
    # await message.answer("Hello, **World**")


# использование CommandObject (аргумент вписывается после команды)
@dp.message(Command('name'))
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        await message.answer(f'Hi, <b>{command.args}</b>')
    else:
        await message.answer('Add your name after command /name')


# @dp.message(F.text)
# async def cmd_echo_with_time(message: types.Message):
#     time_now = datetime.now().strftime('%H:%M')
#     added_text = html.underline(f'Create to {time_now}')
#     await message.answer(f'{message.html_text} \n\n{added_text}', parse_mode='HTML')


# @dp.message(F.text)
# async def cmd_name_f(message: types.Message, command: CommandObject):
#     await message.answer(f'Hi, {html.bold(html.quote(message.html_text))}', parse_mode='HTML')


# async def cmd_name2(message: types.Message, command: CommandObject):
#     if command.args:
#         await message.answer(f'Hi, {html.bold(html.quote(command.args))}', parse_mode='HTML')
#     else:
#         await message.answer('Add your name after command /name')


# @dp.message(F.text)
# async def cmd_data(message: types.Message):
#     data = {
#         'url': '<N/A>',
#         'email': '<N/A>',
#         'code': '<N/A>'
#     }
#     entities = message.entities or []
#     for item in entities:
#         if item.type in data.keys():
#             data[item.type] = item.extract_from(message.text)
#     await message.reply('Result search:\n'
#                         f'URL: {html.quote(data["url"])}\n'
#                         f'Email: {html.quote(data["email"])}\n'
#                         f'Password: {html.quote(data["code"])}'
#                         )


# отправка анимации в ответ
@dp.message(F.animation)
async def cmd_animation(message: types.Message):
    await message.reply_animation(message.animation.file_id)

# ОТПРАВКА КАРТИНОК

# загрузка картинки и сохранение ее id

file_ids = []


# BufferedInputFile
@dp.message(Command('images'))
async def cmd_upload_photo_buffer(message: types.Message):
    with open('pic/buffer_emulation.jpg', 'rb') as image_from_buffer:
        result = await message.answer_photo(
            BufferedInputFile(image_from_buffer.read(),
                              filename='image from buffer.jpg'
                              ),
            caption='Image_from_buffer'
        )
        file_ids.append(result.photo[-1].file)
        print(file_ids)


# FSInputFile
@dp.message(Command('image_file'))
async def cmd_upload_photo_file(message: types.Message):
    image_from_pc = FSInputFile('pic/image_from_pc.jpg')
    result = await message.answer_photo(image_from_pc,
                                        caption='image_from_pc')
    file_ids.append(result.photo[-1].file_id)
    print(file_ids)


# URLInputFile
@dp.message(Command('image_url'))
async def cmd_upload_photo_url(message: types.Message):
    image_from_url = URLInputFile('https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcT18dksjE01o4uNsN-SrwZSP-Ye2rXFP8hhBkjfj_-n1guajQoxP0zer6iNHLTrx1Bd')
    result = await message.answer_photo(image_from_url,
                                        caption='image_from_url')
    file_ids.append(result.photo[-1].file_id)
    print(file_ids)


# отправка картинки по id-ку
@dp.message(Command('image_from_id'))
async def cmd_photo_from_id(message: types.Message):
    try:
        image = file_ids[-1]
        await message.reply_photo(image)
        raise IndexError('List of id''s is empty')
    except IndexError as e:
        print(f'IndexError: {str(e)}')
    except Exception as e:
        print(f'Exception: {str(e)}')


# отправка картинки с текстом
@dp.message(Command('hidden_link'))
async def cmd_hidden_link(message: types.Message):
    await message.answer(
        f'{hide_link("https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcT18dksjE01o4uNsN-SrwZSP-Ye2rXFP8hhBkjfj_-n1guajQoxP0zer6iNHLTrx1Bd")}'
        f'Something text'
        )


# СКАЧИВАНИЕ

# директория на MAC
temp_dir = os.path.join(os.path.expanduser("~"), "PycharmProjects/test_bot3/tmp")


# скачивание картинки
@dp.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=os.path.join(temp_dir, f"{message.photo[-1].file_id}.jpg")
    )


# скачивание эмодзи
@dp.message(F.sticker)
async def download_sticker(message: types.Message, bot: Bot):
    await bot.download(
        message.sticker,
        destination=os.path.join(temp_dir, f'{message.sticker.file_id}.webp')
    )


# обычная клавиатура
# @dp.message(Command('start'))
# async def cmd_start(message: types.Message):
#     kb = [
#             [types.KeyboardButton(text='Button 1')],
#             [types.KeyboardButton(text='Button 2')]
#           ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
#     await message.answer('Choice button', reply_markup=keyboard)


# обычные кнопки форматированные
@dp.message(Command('start'))
async def cmd_start_beautiful(message: types.Message):
    kb = [
            [
                KeyboardButton(text='/keyboard_1_16'),  # кнопки в одном элементе списка
                KeyboardButton(text='/special_commands'),  # ставят их в один ряд
                KeyboardButton(text='/my_user_id')
            ],
            [
                KeyboardButton(text='/inline_url'),
                KeyboardButton(text='/random')
            ]
          ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Tra-ta-ta',
        one_time_keyboard=True,
    )
    # resize_keyboard уменьшает клавиатуру
    # input_field_placeholder в окошке куда пишем прописывает Tra-ta-ta
    await message.answer('Choice button', reply_markup=keyboard)


# KEYBOARD BUILDER

@dp.message(Command('keyboard_1_16'))
async def keyboard_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for button in range(1, 17):
        builder.add(types.KeyboardButton(text=str(button)))
    builder.adjust(4)
    await message.answer(
        'Choice number:',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(Command('special_commands'))
async def special_commands(message: types.Message):
    builder = ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text='Get location', request_location=True),
        types.KeyboardButton(text='Get contact', request_contact=True)
    )
    builder.row(
        types.KeyboardButton(
            text='Create quiz',
            request_poll=types.KeyboardButtonPollType(type='quiz')
        )
    )
    builder.row(
        types.KeyboardButton(
            text="Choice Premium User",
            request_user=types.KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True
            )
        ),
        types.KeyboardButton(
            text="Choice Super Chat",
            request_chat=types.KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )
    )
    await message.answer('Choice action:',
                         reply_markup=builder.as_markup(resize_keyboard=True)
                         )


@dp.message(Command('my_user_id'))
async def get_user_id(message: types.Message):
    await message.answer(f'message_id: {message.message_id}\nuser_id: {message.from_user.id}')


# @dp.message(F.user_shared)
# async def on_user_shared(message: types.Message):
#         # request = types.KeyboardButtonRequestUser.request_id
#         # user_id = types.KeyboardButtonRequestUser.
#     print(
#         f'Request {message.user_shared.request_id}'
#         f'User_ID {message.user_shared.user_id}'
#     )

# inline клавиатура
@dp.message(Command("inline_url"))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(types.InlineKeyboardButton(
        text="Оф. канал Telegram",
        url="tg://resolve?domain=telegram")
    )

    # Чтобы иметь возможность показать ID-кнопку,
    # У юзера должен быть False флаг has_private_forwards
    user_id = 5102838218
    chat_info = await bot.get_chat(user_id)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text="Какой-то пользователь",
            url=f"tg://user?id={user_id}")
        )

    await message.answer(
        'Выберите ссылку',
        reply_markup=builder.as_markup(),
    )


@dp.message(Command('random'))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Push me',
        callback_data='random_value'
        )
    )
    await message.answer(
        'Push button and bot send you random number from 1 to 10',
        reply_markup=builder.as_markup()
    )


@dp.callback_query(Text('random_value'))
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    # C оконком благодарности
    # await callback.answer(
    #     text='Thanks',
    #     show_alert=True
    # )
    # Просто убираем часы в углу кнопки
    # await callback.answer()


user_data = {}


def get_keyboard():
    button = [
        [
            types.InlineKeyboardButton(text='-1', callback_data='num_decr'),
            types.InlineKeyboardButton(text='+1', callback_data='num_incr')
        ],
        [types.InlineKeyboardButton(text='confirm', callback_data='num_finish')]
    ]
    result = types.InlineKeyboardMarkup(inline_keyboard=button)
    return result


async def update_num_text(message: types.Message, new_value: int):
    if suppress(TelegramBadRequest):  # Страховка от MessageNotModified
        await message.edit_text(
            f'write number: {new_value}',
            reply_markup=get_keyboard()
    )


@dp.message(Command('number'))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer(
        f'Your number: 0',
        reply_markup=get_keyboard()
    )


@dp.callback_query(Text(startswith='num_'))
async def callback_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split('_')[1]

    if action == 'incr':
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == 'decr':
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == 'finish':
        await callback.message.edit_text(f'total: {user_value}')

    await callback.answer()


class NumbersCallbackFactory(CallbackData, prefix='fabnum'):
    action: str
    value: Optional[int]


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()

    builder.button(text='-2', callback_data=NumbersCallbackFactory(action='change', value=-2))
    builder.button(text='-1', callback_data=NumbersCallbackFactory(action='change', value=-1))
    builder.button(text='1', callback_data=NumbersCallbackFactory(action='change', value=1))
    builder.button(text='2', callback_data=NumbersCallbackFactory(action='change', value=2))
    builder.button(text='confirm', callback_data=NumbersCallbackFactory(action='finish'))

    builder.adjust(4)
    return builder.as_markup()

def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f'Write number: {new_value}',
            reply_markup=get_keyboard_fab()
        )


@dp.callback_query(NumbersCallbackFactory.filter())
async def callback_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    user_value = user_data.get(callback.from_user.id, 0)
    if callback_data.action == 'Change':
        user_data[callback.from_user.id] = user_value + callback_data.value
        await update_num_text_fab(callback.message, user_value + callback_data.value)
    else:
        await callback.message.edit_text(
            f'Total: {user_value}'
        )
    callback.answer()


async def main():
    # dp.message.register(cmd_name2, Command('name2'))

    # dp.message.register(add_to_list)
    # dp.message.register(show_list)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
