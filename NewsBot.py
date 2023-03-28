import telebot
import requests
from random import randint
from bs4 import BeautifulSoup as BS
from config import *
from db import *
from forex_python.converter import CurrencyRates
from telebot import types
from schedule import every, run_pending
import time
from threading import Thread
import json
# from investing import stonks
from investing1 import stonks
from pprint import pprint
import datetime
from tqdm import tqdm


Beta = False
if Beta:
    bot = telebot.TeleBot(token1)
else:
    bot = telebot.TeleBot(token2)
BotDB = BotDB()
btns = list(links.keys())
htmls = {}
admin = 1387680086
currency = CurrencyRates()
t = False


def birthday(id):
    day = str(int(datetime.date.today().strftime('%d')))
    month = str(int(datetime.date.today().strftime('%m')))
    data = '.'.join([day, month])
    if BotDB.get_birth(id) == data:
        bot.send_message(id, "Дорогой пользователь, поздравляю Вас с днем рождения, спасибо, что Вы с нами!🥳")


def get_currency():
    # r = requests.get("https://invest.yandex.ru/catalog/currency/usd/")
    # html = BS(r.content, "html.parser")
    # dolVal = html.find_all(class_="QV5TZ0Aew_2aahfCgGmv")[0].text
    # try:
    #     dolProc = html.find_all(class_="rzv7e6OPChq71rCQBr9H _9RS0xgK34zINnxUjOgH")
    #     if len(dolProc) > 0:
    #         dolProc = dolProc[0].text.split("  ₽")
    #     else:
    #         dolProc = ("0", html.find_all(class_="rzv7e6OPChq71rCQBr9H SUCnYTT5LFAlaqfSzDh5")[0].text)
    # except BaseException:
    #     dolProc = ("0", "0%")
    #
    # r = requests.get("https://invest.yandex.ru/catalog/currency/eur/")
    # html = BS(r.content, "html.parser")
    # euVal = html.find_all(class_="QV5TZ0Aew_2aahfCgGmv")[1].text
    # try:
    #     euProc = html.find_all(class_="rzv7e6OPChq71rCQBr9H _9RS0xgK34zINnxUjOgH")
    #     if len(euProc) > 0:
    #         euProc = euProc[0].text.split("  ₽")
    #     else:
    #         euProc = ("0", html.find_all(class_="rzv7e6OPChq71rCQBr9H SUCnYTT5LFAlaqfSzDh5")[0].text)
    # except BaseException:
    #     euProc = ("0", "0%")
    return round(currency.get_rate('EUR', 'RUB'), 2), round(currency.get_rate('USD', 'RUB'), 2)


def get_horoscope(znak):
    r = requests.get(links[znak])
    html = BS(r.content, "html.parser")

    soup1 = html.select('h1')[0].text
    soup = html.select('p')
    return soup1, soup


headers = {
    'cookie': 'sso_checked=1; Session_id=3:1663433035.5.0.1663433035738:6xZlBQ:20D.1.2:1|883187617.0.2|64:10003835.681836.xnGm7GifGL7Ca51K8l0VpzizisI; yandex_login=maxss.k2n; yandexuid=1979425991640958970; mda2_beacon=1663433035749; gdpr=0; _ym_d=1663433038; _ym_uid=16634330381069804080; vid=e8d0a90e328f8d78; tmr_lvid=4b172abb4997249b25454fd3166bb785; tmr_lvidTS=1664709380222; _yasc=8ScIIJd6joNRWrZw+Sqjf0f5NjkpTbuWeoNd7pRyT4ngVS01bXdy2C5/jgLV; zen_sso_checked=1; vsd=eyJnZW8iOiIxODgiLCJ1YSI6IllBQlJPV1NFUiIsImVhIjozMCwiZWciOjJ9; _ym_isad=2; tmr_detect=0%7C1677143581052',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.3.949 Yowser/2.5 Safari/537.36',
    }


def get_news(url):
    try:
        r = requests.get(url + '?issue_tld=ru&utm_referrer=dzen.ru', headers=headers)
        html = BS(r.text, "html.parser")
        if url == "https://yandex.ru/news":
            html = html.find(class_="mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top")
        news = html.find_all(class_="mg-card__title")
        ur = html.find_all(class_="mg-card__link")
        return news, ur
    except Exception as error:
        print(error)
        print("bad")
        return [], ""


def save_html():
    global htmls
    for i in tqdm(urls):
        try:
            news, ur = get_news(i)
            if len(news) > 0 < len(ur):
                htmls[i] = (news, ur)
            # print(news[0].text)
            if t and len(news) > 0:
                bot.send_message(1387680086, news[0].text)
        except Exception as error:
            bot.send_message(1387680086, "Ошибка при копирование html")
            print(error)
        time.sleep(randint(5, 20) / 10)
    if t:
        bot.send_message(1387680086, "проверка фонового включения25")
    print("ok")


stonks_ = {}
stonks1 = {}
stonks2 = {}


def save_stonks():
    k = 0
    for i in stonks():
        if i:
            stonks_[i[0]] = i
            stonks1[i[0].lower()] = i[0]
            stonks1[i[1].lower()] = i[0]
            stonks2[i[0]] = k
            stonks2[str(k)] = i[0]
            k += 1


def save_all():
    save_html()
    # save_stonks()


save_all()


def send_news(chat_id, topic, article):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # markup.add(types.KeyboardButton(text="⬅Назад"),
    #         types.KeyboardButton(text="Меню↩"))
    # bot.send_message(chat_id, "Нажмите 'назад', чтобы сменить тему", reply_markup=markup)
    # markup.add(types.KeyboardButton(text="Меню↩"))
    # pprint(htmls)
    if topic in htmls and article < len(htmls[topic][0]) - 1 and len(htmls[topic][0]) > 0 and len(htmls[topic][1]) > 0:
        markup = types.InlineKeyboardMarkup()
        skip = types.InlineKeyboardButton(text="Дальше", callback_data="skip")
        det = types.InlineKeyboardButton(text='Подробнее', url=htmls[topic][1][article].get('href'))
        markup.add(det, skip)
        bot.send_message(chat_id, htmls[topic][0][article].text, reply_markup=markup)
        BotDB.update_article(chat_id, article + 1)
        BotDB.update_topic(chat_id, topic)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text="⬅Назад"),
                   types.KeyboardButton(text="Меню↩"))
        bot.send_message(chat_id, "Новости на эту тему закончились", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # print(call.message.chat.id)
    # print(BotDB.get_status(call.from_user.id))
    try:
        if BotDB.user_exists(call.message.chat.id) and BotDB.get_status(call.message.chat.id) == "settings":

            if BotDB.get_modes(call.message.chat.id) == None or BotDB.get_modes(call.message.chat.id) == set("None"):
                print("bad")
                BotDB.update_modes(call.message.chat.id, "123")
            true_modes = set(BotDB.get_modes(call.message.chat.id))
            markup = types.InlineKeyboardMarkup()
            if "1" in true_modes:
                btn_1 = types.InlineKeyboardButton(text='Новости📰   ✅', callback_data="mode 1")
            else:
                btn_1 = types.InlineKeyboardButton(text='Новости📰   ❌', callback_data="not_mode 1")
            if "2" in true_modes:
                btn_2 = types.InlineKeyboardButton(text='Гороскоп💫  ✅', callback_data="mode 2")
            else:
                btn_2 = types.InlineKeyboardButton(text='Гороскоп💫  ❌', callback_data="not_mode 2")
            if "3" in true_modes:
                btn_3 = types.InlineKeyboardButton(text='Курсы валют💰   ✅', callback_data="mode 3")
            else:
                btn_3 = types.InlineKeyboardButton(text='Курсы валют💰   ❌', callback_data="not_mode 3")

            if call.data == "not_mode 1":
                btn_1 = types.InlineKeyboardButton(text='Новости📰   ✅', callback_data="mode 1")
                true_modes.add("1")
                BotDB.update_modes(call.message.chat.id, "".join(true_modes))
            elif call.data == "mode 1":
                btn_1 = types.InlineKeyboardButton(text='Новости📰   ❌', callback_data="not_mode 1")
                BotDB.update_modes(call.message.chat.id, "".join(true_modes - set("1")))
            elif call.data == "not_mode 2":
                btn_2 = types.InlineKeyboardButton(text='Гороскоп💫  ✅', callback_data="mode 2")
                true_modes.add("2")
                BotDB.update_modes(call.message.chat.id, "".join(true_modes))
            elif call.data == "mode 2":
                btn_2 = types.InlineKeyboardButton(text='Гороскоп💫  ❌', callback_data="not_mode 2")
                BotDB.update_modes(call.message.chat.id, "".join(true_modes - set("2")))
            elif call.data == "not_mode 3":
                btn_3 = types.InlineKeyboardButton(text='Курсы валют💰   ✅', callback_data="mode 3")
                true_modes.add("3")
                BotDB.update_modes(call.message.chat.id, "".join(true_modes))
            elif call.data == "mode 3":
                btn_3 = types.InlineKeyboardButton(text='Курсы валют💰   ❌', callback_data="not_mode 3")
                BotDB.update_modes(call.message.chat.id, "".join(true_modes - set("3")))
            markup.add(btn_1)
            markup.add(btn_2)
            markup.add(btn_3)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Выберите категории рассылки",
                                  reply_markup=markup)
        elif BotDB.get_status(call.message.chat.id) == 'invest_case_add1':
            z = stonks2[call.data.split('_')[1]]
            if BotDB.get_case(call.message.chat.id):
                print(call.data)
                BotDB.update_case(call.message.chat.id, BotDB.get_case(call.message.chat.id) + '_' +
                                  stonks2[call.data.split('_')[1]])
            else:
                BotDB.update_case(call.message.chat.id, stonks2[call.data.split('_')[1]])
            bot.send_message(call.message.chat.id, f'Акция <{z}> добавлена в портфель')
        elif BotDB.get_status(call.message.chat.id) == 'invest_case_del':
            inv = set(BotDB.get_case(call.message.chat.id).split('_'))
            k = stonks2[call.data.split('_')[1]]
            inv.remove(k)
            inv = '_'.join(list(inv))
            BotDB.update_case(call.message.chat.id, inv)
            bot.send_message(call.message.chat.id, f'Акция <{k}> удалена')

        elif BotDB.get_status(call.message.chat.id) == 'invest_statis':
            print(999)
            # pprint(stonks_)
            # pprint(call.data)
            data = list(map(str, stonks_[call.data]))
            pprint(data)
#             bot.send_message(call.message.chat.id, f'''Акция "{data[0]}", краткое "{data[1]}"
# Динамика в сравнении с прошлым торговым днем: {data[3]}%
# Риск этой позиции: {data[4]}
# Стоимость одной акции: {data[5]} {data[6]}''')
            bot.send_message(call.message.chat.id, f'''Акция "{data[0]}", краткое "{data[1]}"
Динамика в сравнении с прошлым торговым днем: {data[3]}{'%' if data[3][-1] != '%' else ''} {data[2]}
{"Рекомендуемые действия" if not data[-2].isdigit() else "Уровень риска"}: {data[4]}
Стоимость одной акции: {data[5]}; {data[6]}
Страна регистрации компании: {data[-1]}
Сфера деятельности: {data[4] if not data[4].isdigit() else 'Неизвестно'}''')
        elif call.data == "skip":
            send_news(call.message.chat.id, BotDB.get_topic(call.message.chat.id),
                      BotDB.get_article(call.message.chat.id))
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text="⬅Назад"),
                       types.KeyboardButton(text="Меню↩"))
            bot.send_message(call.message.chat.id, "Нажмите 'назад', чтобы сменить тему", reply_markup=markup)
            # BotDB.update_status(call.message.chat.id, "pass")
            BotDB.update_article(call.message.chat.id, 0)
            send_news(call.message.chat.id, call.data, 0)
            bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as error:
        print("ошибка callback")
        print(error)


def send_hor():
    bot.send_message(1387680086, "Вроде должна быть рассылка")
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(text="Меню↩")
    markup1.add(back)
    for i in BotDB.get_id():  # [(1387680086, 999)]: #
        try:
            i = (int(i[0]), 999)
            birthday(i[0])
            if "1" in BotDB.get_modes(i[0]) or "2" in BotDB.get_modes(i[0]) or "3" in BotDB.get_modes(
                    i[0]) or BotDB.get_modes(i[0]) is None:
                bot.send_message(i[0], "Утренние новости☕️📰:", reply_markup=markup1)
                if "2" in BotDB.get_modes(i[0]) or BotDB.get_modes(i[0]) is None:
                    if BotDB.get_znak(i[0]) in btns:
                        bot.send_message(i[0], get_horoscope(BotDB.get_znak(i[0]))[0])
                        for j in get_horoscope(BotDB.get_znak(i[0]))[1]:
                            bot.send_message(i[0], j)
                    else:
                        bot.send_message(i[0],
                                         "Вы не указали вашу дату рождения для гороскопа, если хотите его получать введите команду '/активировать'")
                if "3" in BotDB.get_modes(i[0]) or BotDB.get_modes(i[0]) is None:
                    bot.send_message(i[0], "Курс валют💰:")
                    znach = get_currency()
                    dol = f"Доллар💵: {znach[1]}"

                    eu = f"Евро💶: {znach[0]}"

                    bot.send_message(i[0], f"""{dol}

                {eu}""")

                if "1" in BotDB.get_modes(i[0]) or BotDB.get_modes(i[0]) is None:
                    bot.send_message(i[0], "Новости📰:")
                    for j in range(len(htmls["https://yandex.ru/news"][0])):
                        markup = types.InlineKeyboardMarkup()
                        det = types.InlineKeyboardButton(text='Подробнее',
                                                         url=htmls["https://yandex.ru/news"][1][j].get('href'))
                        markup.add(det)
                        # markup.add(types.KeyboardButton(text="Меню↩"))
                        bot.send_message(i[0], htmls["https://yandex.ru/news"][0][j].text, reply_markup=markup)
        except BaseException as er:
            print(i[0], "Он забанил")
            print(er)


every().day.at("05:00").do(send_hor)
every(5).minutes.do(save_all)


def work():
    while True:
        run_pending()
        time.sleep(0.5)


def polling():
    # run_pending()
    bot.infinity_polling()


# while True:
#   run_pending()
#  time.sleep(1)

@bot.message_handler(commands=["send"])
def send(message):
    send_hor()
    bot.send_message(message.chat.id, "Всем отправил")


@bot.message_handler(commands=["start"])
def welcome(message):
    if (message.chat.id,) not in BotDB.get_id():
        bot.send_message(message.chat.id,
                         "{0.first_name}, здравствуйте, я новостной бот. Напишите мне день и месяц вашего рождения (через точку), чтобы получать гороскоп".format(
                             message.from_user))
        if not BotDB.user_exists(message.chat.id):
            BotDB.add_user(message.chat.id, "welcome", "{0.first_name}".format(message.from_user),
                           message.from_user.username, "pass", '123')
        else:
            BotDB.update_status(message.chat.id, "welcome")
    else:
        bot.send_message(message.chat.id, "Я тебя помню")
        BotDB.update_status(message.chat.id, "menu")
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn1 = types.KeyboardButton(text="Гороскопы🪐")
        btn2 = types.KeyboardButton(text="Курсы валют💰")
        btn3 = types.KeyboardButton(text="Новости📰")
        btn5 = types.KeyboardButton(text="Инвестиции📈")
        btn4 = types.KeyboardButton(text="Настройки⚙")
        markup.add(btn1, btn2, btn3, btn5, btn4)
        bot.send_message(message.chat.id, "Вы в меню", reply_markup=markup)


@bot.message_handler(commands=["активировать"])
def activate(message):
    bot.send_message(message.chat.id,
                     "{0.first_name}, напишите мне день и месяц вашего рождения (через точку), чтобы получать гороскоп".format(
                         message.from_user))
    if not BotDB.user_exists(message.chat.id):
        BotDB.add_user(message.chat.id, "welcome", "{0.first_name}".format(message.from_user),
                       message.from_user.username, "pass")
    else:
        BotDB.update_status(message.chat.id, "welcome")


@bot.message_handler(commands=["отказаться"])
def cancel(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(text="Меню↩")
    markup.add(back)
    BotDB.update_znak(message.chat.id, "pass")
    bot.send_message(message.chat.id, "Рассылка отменена")
    bot.send_message(message.chat.id,
                     "У вас не подключена рассылка, чтобы её активировать введите команду '/активировать'",
                     reply_markup=markup)


@bot.message_handler(content_types=["text"])
def chat(message):
    global t
    if message.text == "True" and message.chat.id == 1387680086:
        t = True
        bot.send_message(message.chat.id, "True2")
    if message.text == "False" and message.chat.id == 1387680086:
        t = False
        bot.send_message(message.chat.id, "False2")
    if message.text == 'Назад↩':
        BotDB.update_status(message.chat.id, 'invest')
    if message.text == 'Инвестиции📈' and BotDB.get_status(message.chat.id) == 'menu':
        BotDB.update_status(message.chat.id, "invest")
    if message.text == 'Добавить акцию✅' and BotDB.get_status(message.chat.id) == 'invest_case':
        BotDB.update_status(message.chat.id, "invest_case_add")
    if message.text == 'Удалить акцию🚫' and BotDB.get_status(message.chat.id) == 'invest_case':
        BotDB.update_status(message.chat.id, "invest_case_del")
    if message.text == 'Мои акции🧮':
        BotDB.update_status(message.chat.id, "invest_statis")
    if message.text == 'Мой портфель💼':
        BotDB.update_status(message.chat.id, "invest_case")
    if message.text == "Меню↩":
        BotDB.update_status(message.chat.id, "menu")
    if message.text == "Гороскопы🪐" and BotDB.get_status(message.chat.id) == 'menu':
        BotDB.update_status(message.chat.id, "horoscope")
    if message.text == "Новости📰" or message.text == "⬅Назад":
        BotDB.update_status(message.chat.id, "news")
    if message.text == "Курсы валют💰":
        BotDB.update_status(message.chat.id, "curr")
    if message.text == "Настройки⚙":
        BotDB.update_status(message.chat.id, "settings")
    if message.text in btns:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton(text="Меню↩")
        markup.add(back)
        bot.send_message(message.chat.id, get_horoscope(message.text)[0])
        for i in get_horoscope(message.text)[1]:
            bot.send_message(message.chat.id, i.text, reply_markup=markup)
        BotDB.update_status(message.chat.id, "pass")

    if BotDB.get_status(message.chat.id) == 'invest_case_add1':
        markup = types.InlineKeyboardMarkup()
        t = True
        for i in stonks1:
            if message.text.lower() in i:
                t = False
                cal = 'add_' + str(stonks2[stonks1[i]])
                markup.add(types.InlineKeyboardButton(text=str(stonks1[i]), callback_data=cal))
        if not t:
            bot.send_message(message.chat.id, 'Вот все, что удалось найти, выберите ту, которую хотите добавить',
                         reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'По вашему запросу ничего не найдено')

    if BotDB.get_status(message.chat.id) == "welcome":
        BotDB.add_birth(message.chat.id, message.text)
        data = list(map(int, message.text.split(".")))
        if len(data) == 2 and 0 < data[0] < 32 and 0 < data[1] < 13:
            znak = "Овен"
            if (21 <= data[0] <= 31 and data[1] == 3) or (data[1] == 4 and 1 <= data[0] <= 19):
                znak = btns[0]

            elif (data[0] >= 20 and data[0] <= 30 and data[1] == 4) or (
                    data[1] == 5 and data[0] >= 1 and data[0] <= 20):

                znak = btns[1]

            elif (data[0] >= 21 and data[0] <= 31 and data[1] == 5) or (
                    data[1] == 6 and data[0] >= 1 and data[0] <= 21):

                znak = btns[2]

            elif (data[0] >= 22 and data[0] <= 30 and data[1] == 6) or (
                    data[1] == 7 and data[0] >= 1 and data[0] <= 22):

                znak = btns[3]

            elif (data[0] >= 23 and data[0] <= 31 and data[1] == 7) or (
                    data[1] == 8 and data[0] >= 1 and data[0] <= 22):

                znak = btns[4]

            elif (data[0] >= 23 and data[0] <= 31 and data[1] == 8) or (
                    data[1] == 9 and data[0] >= 1 and data[0] <= 22):

                znak = btns[5]

            elif (data[0] >= 23 and data[0] <= 30 and data[1] == 9) or (
                    data[1] == 10 and data[0] >= 1 and data[0] <= 23):

                znak = btns[6]

            elif (24 <= data[0] <= 31 and data[1] == 10) or (
                    data[1] == 11 and 1 <= data[0] <= 22):

                znak = btns[7]

            elif (23 <= data[0] <= 30 and data[1] == 11) or (
                    data[1] == 12 and 1 <= data[0] <= 21):

                znak = btns[8]

            elif (22 <= data[0] <= 31 and data[1] == 12) or (
                    data[1] == 1 and 1 <= data[0] <= 20):

                znak = btns[9]

            elif (21 <= data[0] <= 31 and data[1] == 1) or (
                    data[1] == 2 and 1 <= data[0] <= 18):

                znak = btns[10]

            elif (19 <= data[0] <= 29 and data[1] == 2) or (
                    data[1] == 3 and 1 <= data[0] <= 20):

                znak = btns[11]

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text="Меню↩")
            markup.add(btn1)
            bot.send_message(message.chat.id, f"А вы знали, что Вы {znak}?")
            BotDB.update_status(message.chat.id, "pass")
            BotDB.update_znak(message.chat.id, znak)
            bot.send_message(message.chat.id,
                             "Теперь каждое утро в 8 часов вы будете получать актуальный гороскоп, новости и курс валют,,"
                             " чтобы отменить рассылку введите команду '/отказаться'",
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Введены невенрные данные, попробуйте еще раз")

    if BotDB.get_status(message.chat.id) == "news":
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        home = types.KeyboardButton(text="Меню↩")
        markup1.add(home)
        bot.send_message(message.chat.id, "Чтобы вернуться, нажмите кнопку меню", reply_markup=markup1)
        markup = types.InlineKeyboardMarkup()
        btn_0 = types.InlineKeyboardButton(text='Глвное❗', callback_data="https://dzen.ru/news")
        btn_1 = types.InlineKeyboardButton(text='Казань🕌', callback_data="https://dzen.ru/news/region/kazan")
        btn_2 = types.InlineKeyboardButton(text='Коронавирус🦠',
                                           callback_data="https://dzen.ru/news/rubric/koronavirus")
        btn_3 = types.InlineKeyboardButton(text='Политика🇺🇳', callback_data="https://dzen.ru/news/rubric/politics")
        btn_4 = types.InlineKeyboardButton(text='Экономика📈', callback_data="https://dzen.ru/news/rubric/business")
        btn_5 = types.InlineKeyboardButton(text='Спорт⚽️',
                                           callback_data="https://dzen.ru/sport?utm_source=yxnews&utm_medium=desktop")
        btn_6 = types.InlineKeyboardButton(text='Происшествия🚨',
                                           callback_data="https://dzen.ru/news/rubric/incident")
        btn_7 = types.InlineKeyboardButton(text='Культура🎨', callback_data="https://dzen.ru/news/rubric/culture")
        btn_8 = types.InlineKeyboardButton(text='Технологии💻', callback_data="https://dzen.ru/news/rubric/computers")
        markup.add(btn_0)
        markup.add(btn_1)
        markup.add(btn_2)
        markup.add(btn_3)
        markup.add(btn_4)
        markup.add(btn_5)
        markup.add(btn_6)
        markup.add(btn_7)
        markup.add(btn_8)
        bot.send_message(message.chat.id, "Выберите тему", reply_markup=markup)

    if BotDB.get_status(message.chat.id) == 'invest_statis':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        markup.add(types.KeyboardButton(text="Назад↩"))
        bot.send_message(message.chat.id, 'Чтобы вернуться нажмите "Назад"', reply_markup=markup)
        markup = types.InlineKeyboardMarkup()
        if BotDB.get_case(message.chat.id):
            for i in BotDB.get_case(message.chat.id).split('_'):
                markup.add(types.InlineKeyboardButton(text=i, callback_data=i))
            bot.send_message(message.chat.id, 'Для просмотра данных выберите акцию из вашего портфеля', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            markup.add(types.KeyboardButton(text="Назад↩"))
            bot.send_message(message.chat.id, 'У вас нет акций, их можно добавить в разделе "Портфель"', reply_markup=markup)

    if BotDB.get_status(message.chat.id) == 'invest_case':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        back = types.KeyboardButton(text="Назад↩")
        btn1 = types.KeyboardButton(text="Добавить акцию✅")
        btn2 = types.KeyboardButton(text="Удалить акцию🚫")
        markup.add(back, btn1, btn2)
        bot.send_message(message.chat.id, "Вы зашли в раздел портфель, здесь вы можете редактировать свой портфель",
                         reply_markup=markup)
        mes = 'В вашем портфеле:'
        for i in BotDB.get_case(message.chat.id).split('_'):
            mes += f'\n-{i}'
        bot.send_message(message.chat.id, mes)

    if BotDB.get_status(message.chat.id) == 'invest':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton(text="Меню↩")
        btn1 = types.KeyboardButton(text="Мой портфель💼")
        btn2 = types.KeyboardButton(text='Мои акции🧮')
        markup.add(back, btn2, btn1)
        bot.send_message(message.chat.id, 'вы зашли в раздел инвестициий', reply_markup=markup)

    if BotDB.get_status(message.chat.id) == 'invest_case_add':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        markup.add(types.KeyboardButton(text="Назад↩"))
        bot.send_message(message.chat.id, 'Введите полное или краткое название акции, я постараюсь что-то найти',
                         reply_markup=markup)
        BotDB.update_status(message.chat.id, 'invest_case_add1')

    if BotDB.get_status(message.chat.id) == 'invest_case_del':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        markup.add(types.KeyboardButton(text="Назад↩"))
        bot.send_message(message.chat.id, 'Чтобы вернуться нажмите "Назад"', reply_markup=markup)
        markup = types.InlineKeyboardMarkup()
        if BotDB.get_case(message.chat.id):
            for i in BotDB.get_case(message.chat.id).split('_'):
                cal = 'del_' + str(stonks2[i])
                markup.add(types.InlineKeyboardButton(text=i, callback_data=cal))
            bot.send_message(message.chat.id, 'Выберите акцию, которую хотите удалить',
                             reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            markup.add(types.KeyboardButton(text="Назад↩"))
            bot.send_message(message.chat.id, 'У вас нет акций, их можно добавить в разделе "Портфель"',
                             reply_markup=markup)

    if BotDB.get_status(message.chat.id) == "menu":
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn1 = types.KeyboardButton(text="Гороскопы🪐")
        btn2 = types.KeyboardButton(text="Курсы валют💰")
        btn3 = types.KeyboardButton(text="Новости📰")
        btn5 = types.KeyboardButton(text="Инвестиции📈")
        btn4 = types.KeyboardButton(text="Настройки⚙")
        markup.add(btn1, btn2, btn3, btn5, btn4)
        bot.send_message(message.chat.id, "Вы в меню", reply_markup=markup)

    if BotDB.get_status(message.chat.id) == "horoscope":
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn1 = types.KeyboardButton(text=btns[0])
        btn2 = types.KeyboardButton(text=btns[1])
        btn3 = types.KeyboardButton(text=btns[2])
        btn4 = types.KeyboardButton(text=btns[3])
        btn5 = types.KeyboardButton(text=btns[4])
        btn6 = types.KeyboardButton(text=btns[5])
        btn7 = types.KeyboardButton(text=btns[6])
        btn8 = types.KeyboardButton(text=btns[7])
        btn9 = types.KeyboardButton(text=btns[8])
        btn10 = types.KeyboardButton(text=btns[9])
        btn11 = types.KeyboardButton(text=btns[10])
        btn12 = types.KeyboardButton(text=btns[11])
        back = types.KeyboardButton(text="Меню↩")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, back)
        bot.send_message(message.chat.id, "Выберите знак зодиака для которого хотите узнать гороскоп",
                         reply_markup=markup)

    if BotDB.get_status(message.chat.id) == "curr":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton(text="Меню↩")
        markup.add(back)
        znach = get_currency()
        dol = f"Доллар💵: {znach[1]}"

        eu = f"Евро💶: {znach[0]}"

        bot.send_message(message.chat.id, f"""{dol}

{eu}""", reply_markup=markup)
        BotDB.update_status(message.chat.id, "pass")

    if BotDB.get_status(message.chat.id) == "settings":
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton(text="Меню↩")
        markup1.add(back)
        bot.send_message(message.chat.id, "Чтобы вернуться, нажмите кнопку меню", reply_markup=markup1)
        markup = types.InlineKeyboardMarkup()
        if "1" in BotDB.get_modes(message.chat.id):
            btn_1 = types.InlineKeyboardButton(text='Новости📰   ✅', callback_data="mode 1")
        else:
            btn_1 = types.InlineKeyboardButton(text='Новости📰   ❌', callback_data="not_mode 1")
        if "2" in BotDB.get_modes(message.chat.id):
            btn_2 = types.InlineKeyboardButton(text='Гороскоп💫  ✅', callback_data="mode 2")
        else:
            btn_2 = types.InlineKeyboardButton(text='Гороскоп💫  ❌', callback_data="not_mode 2")
        if "3" in BotDB.get_modes(message.chat.id):
            btn_3 = types.InlineKeyboardButton(text='Курсы валют💰   ✅', callback_data="mode 3")
        else:
            btn_3 = types.InlineKeyboardButton(text='Курсы валют💰   ❌', callback_data="not_mode 3")
        markup.add(btn_1)
        markup.add(btn_2)
        markup.add(btn_3)
        bot.send_message(message.chat.id, "Выберите категории рассылки", reply_markup=markup)


th = Thread(target=work)
th.start()

th1 = Thread(target=bot.infinity_polling)
th1.start()
