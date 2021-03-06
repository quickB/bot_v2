from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from natsort import *
import urllib.parse
import time

import subprocess
from subprocess import call
import os
import glob
import shutil

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/help", "/Random"]
    keyboard.add(*buttons)

    await message.answer("/Random image for random page", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("---------bot_v1---------\n"
                         "Пока только одна команда\n"
                         "/Random - картинки с рандомной страницы Джоя")


@dp.message_handler(commands=['Random'])
async def process_start_command(message: types.Message):
    await message.answer("загружаю картинки")
    # задаются типы альбомов для отправки
    mediaA = types.MediaGroup()
    mediaB = types.MediaGroup()
    mediaC = types.MediaGroup()
    mediaD = types.MediaGroup()
    mediaE = types.MediaGroup()
    mediaF = types.MediaGroup()
    mediaG = types.MediaGroup()

    # peer это префикс в имени файла,означающий принадлежность к альбому
    # потом я всё переделаю без буквенных префиксов, а пока так
    # сокральное значение "Т" состоит в том, что оно не из диапазона A-G
    peer = 'T'
    file_source = './image/'

    # запускаем скрипт скачивания картинок с рандомной страницы и забираем счетчик картинок
    p = subprocess.Popen(['./jreactor_random_page.sh'], stdout=subprocess.PIPE)
    count_files = int(p.stdout.readline())

    # если картинок больше десятков на 1 (например, 11,21,31 и т.д.) то последняя картинка
    # сохраняется в отдельную папку и докидывается потом отдельным сообщением, т.к. альбомы работают с 2-10
    ost_cf = count_files % 10
    await message.answer("картинки загружены, распихиваю по альбомам")
    if ost_cf == 1:
        # для перемещения одного файла написал скрипт на баше)
        # потом на питоне напишу строку
        scr = subprocess.Popen(['./move_last_file.sh'], stdout=subprocess.PIPE)
        wait_sh = scr.stdout.readline()

    # тутнадо переделать. получаем список файлов
    name_of_files = [os.path.basename(x) for x in glob.glob('./image/*')]
    # удаляем имена папок (надо в одну строку написать, чтоли)
    name_of_files.remove('last')
    name_of_files.remove('gif')
    name_of_files.remove('doc')
    # сортируем по счетчику (чтоб вместо 1,10,2,3...9 было 1,2,3,4...10)
    name_of_files=natsorted(name_of_files)

    # это строка для дебага, можно удалить
    # print(name_of_files)

    if name_of_files:
        # тут файлы распихиваются по альбомам в зависимости от префикса
        for file in name_of_files:
            if file[0] == 'A':
                mediaA.attach_photo(types.InputFile(file_source + file))
                peer = 'A'
            elif file[0] == 'B':
                mediaB.attach_photo(types.InputFile(file_source + file))
                peer = 'B'
            elif file[0] == 'C':
                mediaC.attach_photo(types.InputFile(file_source + file))
                peer = 'C'
            elif file[0] == 'D':
                mediaD.attach_photo(types.InputFile(file_source + file))
                peer = 'D'
            elif file[0] == 'E':
                mediaE.attach_photo(types.InputFile(file_source + file))
                peer = 'E'
            elif file[0] == 'F':
                mediaF.attach_photo(types.InputFile(file_source + file))
                peer = 'F'
            elif file[0] == 'G':
                mediaG.attach_photo(types.InputFile(file_source + file))
                peer = 'G'

        # а тут пошла жара))) да, это надо переделать когда избавлюсь от префиксов
        # но работает. тайм слип посавил, с ним телеграм бота реже банит за спам в лс пользователю
        # у меня прилетал до 4х раз в день на 9 секунд каждый. с задержкой пока только раз
        if peer == 'A':
            await message.answer_media_group(media=mediaA)
        elif peer == 'B':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
        elif peer == 'C':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
        elif peer == 'D':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
            time.sleep(1)
            await message.answer_media_group(media=mediaD)
        elif peer == 'E':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
            time.sleep(1)
            await message.answer_media_group(media=mediaD)
            time.sleep(1)
            await message.answer_media_group(media=mediaE)
        elif peer == 'F':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
            time.sleep(1)
            await message.answer_media_group(media=mediaD)
            time.sleep(1)
            await message.answer_media_group(media=mediaE)
            time.sleep(1)
            await message.answer_media_group(media=mediaF)
        elif peer == 'G':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
            time.sleep(1)
            await message.answer_media_group(media=mediaD)
            time.sleep(1)
            await message.answer_media_group(media=mediaE)
            time.sleep(1)
            await message.answer_media_group(media=mediaF)
            time.sleep(1)
            await message.answer_media_group(media=mediaG)
        else:
            await message.answer("что-то пошло не так")
    else:
        await message.answer("картинок нет")


    #докидываем анимации, если они были
    dir_gif = './image/gif'
    files = os.listdir(dir_gif)
    time.sleep(1)
    if files != '':
        dir_for_add = './image/gif/'
        files_for_add = []
        for file in files:
            files_for_add.append(dir_for_add + file)
        for var in files_for_add:
            video = open(var, 'rb')
            await message.answer_animation(video)
            video.close()

    # докидываем последнюю картинку, если есть
    # надо переделать. цикл не нужен. она всегда одна
    last_dir = './image/last'
    last_files = os.listdir(last_dir)
    time.sleep(1)
    if last_files != '':
        dir_for_add = './image/last/'
        files_for_add = []
        for file in last_files:
            files_for_add.append(dir_for_add + file)
        for var in files_for_add:
            photo = open(var, 'rb')
            await message.answer_photo(photo)
            photo.close()

    # докидываем картинки больше 5мб (если есть) как документы
    as_doc = './image/doc'
    doc_files = os.listdir(as_doc)
    time.sleep(1)
    if doc_files != '':
        dir_for_add = './image/doc/'
        files_for_add = []
        for file in doc_files:
            files_for_add.append(dir_for_add + file)
        for var in files_for_add:
            big_file = open(var, 'rb')
            await message.answer_document(big_file)
            big_file.close()

@dp.message_handler()
async def echo_message(message: types.Message):
    # забираем текст сообщения пользователя как тег
    tag_react = message.text
    # перекодируем для URL если текст на русском
    tag_for_curl = urllib.parse.quote(tag_react)
    await message.answer("загружаю картинки")

    # задаются типы альбомов для отправки
    mediaA = types.MediaGroup()
    mediaB = types.MediaGroup()
    mediaC = types.MediaGroup()
    mediaD = types.MediaGroup()
    mediaE = types.MediaGroup()
    mediaF = types.MediaGroup()
    mediaG = types.MediaGroup()

    # peer это префикс в имени файла,означающий принадлежность к альбому
    # потом я всё переделаю без буквенных префиксов, а пока так
    # сокральное значение "Т" состоит в том, что оно не из диапазона A-G
    peer = 'T'
    file_source = './image/'

    # запускаем скрипт скачивания картинок и передаём в аргумент тег из сообщения пользователя
    # забираем счетчик картинок
    p = subprocess.Popen(['./jreactor_tag_page.sh {0}'.format(tag_for_curl)], stdout=subprocess.PIPE, shell=True)
    count_files = int(p.stdout.readline())

    # если картинок больше десятков на 1 (например, 11,21,31 и т.д.) то последняя картинка
    # сохраняется в отдельную папку и докидывается потом отдельным сообщением, т.к. альбомы работают с 2-10
    ost_cf = count_files % 10
    await message.answer("картинки загружены, распихиваю по альбомам")
    if ost_cf == 1:
        # для перемещения одного файла написал скрипт на баше)
        # потом на питоне напишу строку
        scr = subprocess.Popen(['./move_last_file.sh'], stdout=subprocess.PIPE)
        wait_sh = scr.stdout.readline()

    # тутнадо переделать. получаем список файлов
    name_of_files = [os.path.basename(x) for x in glob.glob('./image/*')]
    # удаляем имена папок (надо в одну строку написать, чтоли)
    name_of_files.remove('last')
    name_of_files.remove('gif')
    name_of_files.remove('doc')
    # сортируем по счетчику (чтоб вместо 1,10,2,3...9 было 1,2,3,4...10)
    name_of_files = natsorted(name_of_files)
    

    if name_of_files:
        # тут файлы распихиваются по альбомам в зависимости от префикса
        for file in name_of_files:
            if file[0] == 'A':
                mediaA.attach_photo(types.InputFile(file_source + file))
                peer = 'A'
            elif file[0] == 'B':
                mediaB.attach_photo(types.InputFile(file_source + file))
                peer = 'B'
            elif file[0] == 'C':
                mediaC.attach_photo(types.InputFile(file_source + file))
                peer = 'C'
            elif file[0] == 'D':
                mediaD.attach_photo(types.InputFile(file_source + file))
                peer = 'D'
            elif file[0] == 'E':
                mediaE.attach_photo(types.InputFile(file_source + file))
                peer = 'E'
            elif file[0] == 'F':
                mediaF.attach_photo(types.InputFile(file_source + file))
                peer = 'F'
            elif file[0] == 'G':
                mediaG.attach_photo(types.InputFile(file_source + file))
                peer = 'G'

        # а тут пошла жара))) да, это надо переделать когда избавлюсь от префиксов
        # но работает. тайм слип посавил, с ним телеграм бота реже банит за спам в лс пользователю
        # у меня прилетал до 4х раз в день на 9 секунд каждый. с задержкой пока только раз
        if peer == 'A':
            # print(mediaA)
            await message.answer_media_group(media=mediaA)
        elif peer == 'B':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
        elif peer == 'C':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
        elif peer == 'D':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
            time.sleep(1)
            await message.answer_media_group(media=mediaD)
        elif peer == 'E':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
            time.sleep(1)
            await message.answer_media_group(media=mediaD)
            time.sleep(1)
            await message.answer_media_group(media=mediaE)
        elif peer == 'F':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
            time.sleep(1)
            await message.answer_media_group(media=mediaD)
            time.sleep(1)
            await message.answer_media_group(media=mediaE)
            time.sleep(1)
            await message.answer_media_group(media=mediaF)
        elif peer == 'G':
            await message.answer_media_group(media=mediaA)
            time.sleep(1)
            await message.answer_media_group(media=mediaB)
            time.sleep(1)
            await message.answer_media_group(media=mediaC)
            time.sleep(1)
            await message.answer_media_group(media=mediaD)
            time.sleep(1)
            await message.answer_media_group(media=mediaE)
            time.sleep(1)
            await message.answer_media_group(media=mediaF)
            time.sleep(1)
            await message.answer_media_group(media=mediaG)
        else:
            await message.answer("что-то пошло не так")
    else:
        await message.answer("картинок нет")
    # докидываем анимации, если они были
    dir_gif = './image/gif'
    files = os.listdir(dir_gif)
    time.sleep(1)
    if files != '':
        dir_for_add = './image/gif/'
        files_for_add = []
        for file in files:
            files_for_add.append(dir_for_add + file)
        for var in files_for_add:
            video = open(var, 'rb')
            await message.answer_animation(video)
            video.close()
    # докидываем последнюю картинку, если есть
    last_dir = './image/last'
    last_files = os.listdir(last_dir)
    time.sleep(1)
    if last_files != '':
        dir_for_add = './image/last/'
        files_for_add = []
        for file in last_files:
            files_for_add.append(dir_for_add + file)
        for var in files_for_add:
            photo = open(var, 'rb')
            await message.answer_photo(photo)
            photo.close()
    # докидываем картинки больше 5мб (если есть) как документы
    as_doc = './image/doc'
    doc_files = os.listdir(as_doc)
    time.sleep(1)
    if doc_files != '':
        dir_for_add = './image/doc/'
        files_for_add = []
        for file in doc_files:
            files_for_add.append(dir_for_add + file)
        for var in files_for_add:
            big_file = open(var, 'rb')
            await message.answer_document(big_file)
            big_file.close()

    #await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)

