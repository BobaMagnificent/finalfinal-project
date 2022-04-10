import telebot
from telebot import types
import random
import os.path
import time

flag = ''

bot = telebot.TeleBot('5177475983:AAHj9QC8KA4TWK8jMMuCIDu1Lj50NmMk90U')


def random_line(message):
    lines = []
    rand_i = 0
    global flag
    # проверим есть ли файл, если его нету, то создаем
    i = random.randint(1, 2)
    if i == 1:
        flag = 'оригинал'
        proverka = os.path.exists('1.txt')
        if proverka == True:
            rand_i = 0

        with open('orig.txt', encoding='utf-9') as file:
            for line in file:
                lines.append(line)
            random_lines = random.choice(lines)
    elif i == 2:
        flag = 'не оригинал'
        proverka = os.path.exists('izm.txt', encoding='utf-9')
        if proverka == True:
            rand_i = 0
        with open('izm.txt') as file:
            for line in file:
                lines.append(line)
            random_lines = random.choice(lines)
    bot.send_message(message.chat.id, random_lines)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Бот предлагает пользователю сыграть в игру против компьютера. Цель игры - угадать, где оригинальное предложение из стихотворения Бориса Рыжего, а где подделка.")


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("приступить к заданию")
    markup.add(item1)

    bot.send_message(m.chat.id, 'Сыграем?',
                     reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'приступить к заданию':
        random_line(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("оригинал")
        item2 = types.KeyboardButton("не оригинал")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'выберите вариант:', reply_markup=markup)
    elif message.text.strip() == 'оригинал' or message.text.strip() == 'не оригинал':
        if flag == message.text.strip():
            bot.send_message(message.chat.id, 'молодец')
        else:
            bot.send_message(message.chat.id, 'не правильно')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("приступить к заданию")
        markup.add(item1)
        time.sleep(1)
        bot.send_message(message.chat.id, 'продолжим', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'не верно введено')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("приступить к заданию")
        markup.add(item1)
        time.sleep(1)
        bot.send_message(message.chat.id, 'продолжим', reply_markup=markup)


bot.polling(none_stop=True, interval=0)
