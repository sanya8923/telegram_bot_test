import asyncio
import logging

from aiogram import Bot, Dispatcher, types, html, F
from aiogram.filters.command import Command, CommandObject
from aiogram.types import FSInputFile, BufferedInputFile, URLInputFile
from aiogram.enums.dice_emoji import DiceEmoji
from config_reader import config
from datetime import datetime

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Hello')


@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


async def cmd_test2(message: types.Message):
    await message.reply('Test2')


@dp.message(Command('dice'))
async def cmd_dice(message: types.Message, bot: Bot):
    await bot.send_dice(5102838218, emoji=DiceEmoji.DICE)


# mylist = [1, 2, 3]
#
#
# @dp.message(Command('add_to_list'))
# async def add_to_list(message: types.Message):
#     mylist.append(7)
#     await message.answer('Added the number 7')


# @dp.message(Command('show_list'))
# async def show_list(message: types.Message):
#     await message.answer(f'Your list: {mylist}')


@dp.message(Command('test3'))
async def cmd_test(message: types.Message):
    await message.reply('test3')


@dp.message(Command('test4'))
async def cmd_test4(message: types.Message):
    await message.answer('Hello, <b>World</b>', parse_mode='HTML')
    # await message.answer("Hello, **World**")


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


@dp.message(F.animation)
async def cmd_animation(message: types.Message):
    await message.reply_animation(message.animation.file_id)


file_ids = []


@dp.message(Command('images'))
async def cmd_upload_photo_buffer(message: types.Message):
    with open('pic/buffer_emulation.jpg', 'rb') as image_from_buffer:
        result = await message.answer_photo(
            BufferedInputFile(image_from_buffer.read(),
                              filename='image from buffer.jpg'
                              ),
            caption='Image_from_buffer'
        )
        file_ids.append(result.photo[-1].file_id)
        print(file_ids)


@dp.message(Command('image_file'))
async def cmd_upload_photo_file(message: types.Message):
    image_from_pc = FSInputFile('pic/image_from_pc.jpg')
    result = await message.answer_photo(image_from_pc,
                                        caption='image_from_pc')
    file_ids.append(result.photo[-1].file_id)
    print(file_ids)


# @dp.message(Command('image_url'))
# async def cmd_upload_photo_url(message: types.Message):
#     file_ids = []


async def main():
    dp.message.register(cmd_test2, Command('test2'))
    # dp.message.register(cmd_name2, Command('name2'))

    # dp.message.register(add_to_list)
    # dp.message.register(show_list)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
