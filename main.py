import telebot
from telebot import types
import kundelik
from datetime import datetime
from datetime import timedelta, date
import db
import kunapipy
import requests.exceptions
import formatweekday

token=''
bot=telebot.TeleBot(token)

def restart():
    print('Error...')

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        print(message.text)
        out =""""""
        bot.delete_message(message.chat.id, message.message_id)
        myresult = db.getdata(f"SELECT dn FROM `users` WHERE `tg` = {message.chat.id}")

        if len(myresult) > 0:

            a =""
            for x in myresult:
                a = str(x).replace("(","")
                a = a.replace(")","")
                a = a.replace(",","")
                a = a.replace("'","")
            
            hw = kundelik.get_hw(token=a, date = date.today() + timedelta(days=1))
            print(hw)
            out = out+ datetime.strftime(date.today(),'%Y-%m-%d') + "  " + formatweekday.format_weekday(date.today().weekday()) +'\n'
            out = out+" "'\n'
            for i in hw:
                out = out+"----------"+i[1]+"----------"+'\n'
                out = out+i[0]+'\n'
            
            out = out + "------------------------------------------------------------"

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            btn2 = types.KeyboardButton("Далее")
            btn3 = types.KeyboardButton("Оценки")
            markup.add(btn1, btn2, btn3)

            bot.send_message(message.chat.id, out, reply_markup=markup)
            
        else:
            out = """Пожалуйста, введите данные аккаунта в виде логин пробел пароль"""
            bot.send_message(message.chat.id, out)
            bot.register_next_step_handler(message, login)

    except requests.exceptions.JSONDecodeError:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Проблемы на стороне серверов Kundelik")
    except: restart()

def login(message):
    try:
        log = message.text.split()[0]
        pas = message.text.split()[1]
    except IndexError:
        bot.send_message(message.chat.id, "Ошибка ввода")
        bot.register_next_step_handler(message=message, callback=login)
    try:
        token = kundelik.get_token(login=log, password=pas)

        db.setdata(f"INSERT INTO `users`(`tg`, `dn`, `currentdate`) VALUES ('{message.chat.id}','{token}','{date.today()}')")

        bot.register_next_step_handler(message=message, callback=start_message)
    
    except kunapipy.kundelik.exceptions.KunError:
        bot.send_message(message.chat.id, "Неверные данные")
        bot.register_next_step_handler(message=message, callback=login)

    except requests.exceptions.JSONDecodeError:
        bot.send_message(message.chat.id, "Проблемы на стороне серверов Kundelik")
        
    bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
        

@bot.message_handler(commands=['loguot'])
def logout(message):
    bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
    db.setdata(f"DELETE FROM `users` WHERE `tg` = '{message.chat.id}'")
    bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта. Для повторного входа введите /start")

@bot.message_handler(content_types=['text'])
def messageing(message):
    print(message.text)
    if len(message.text)<10:
        try:
            dbdate:date = db.getdata(f"SELECT currentdate FROM `users` WHERE `tg` = {message.chat.id}")
            
            currentdate:date = datetime.strptime(dbdate[0][0], '%Y-%m-%d')

            bot.delete_message(message.chat.id, message.message_id)
            if message.text == "Далее":
                currentdate = currentdate + timedelta(days=1)
                print(currentdate)

                formatted_date = datetime.strftime(currentdate,'%Y-%m-%d')
                db.setdata(f"UPDATE `users` SET `currentdate`='{formatted_date}' WHERE `tg`='{message.chat.id}'")

                dbdate:date = db.getdata(f"SELECT currentdate FROM `users` WHERE `tg` = {message.chat.id}")
            
                currentdate:date = datetime.strptime(dbdate[0][0], '%Y-%m-%d')

                out =""""""

                myresult = db.getdata(f"SELECT dn FROM `users` WHERE `tg` = {message.chat.id}")

                if len(myresult) > 0:

                    out = datetime.strftime(currentdate,'%Y-%m-%d')+ "  " + formatweekday.format_weekday(currentdate.weekday()) +'\n'
                    out = out+" "'\n'
                    for x in myresult:
                        a = str(x).replace("(","")
                        a = a.replace(")","")
                        a = a.replace(",","")
                        a = a.replace("'","")
                    
                    hw = kundelik.get_hw(token=a, date = currentdate)
                    print(hw)

                    for i in hw:
                        out = out+"----------"+i[1]+"----------"+'\n'
                        out = out+i[0]+'\n'
                    
                    out = out + "------------------------------------------------------------"

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = types.KeyboardButton("Назад")
                    btn2 = types.KeyboardButton("Далее")
                    btn3 = types.KeyboardButton("Оценки")
                    markup.add(btn1, btn2, btn3)

                    bot.send_message(message.chat.id, text=out, reply_markup=markup)

            if message.text == "Назад":
                currentdate = currentdate - timedelta(days=1)
                formatted_date = datetime.strftime(currentdate,'%Y-%m-%d')
                db.setdata(f"UPDATE `users` SET `currentdate`='{formatted_date}' WHERE `tg`='{message.chat.id}'")
                print(currentdate)

                dbdate:date = db.getdata(f"SELECT currentdate FROM `users` WHERE `tg` = {message.chat.id}")
            
                currentdate:date = datetime.strptime(dbdate[0][0], '%Y-%m-%d')

                out =""""""

                myresult = db.getdata(f"SELECT dn FROM `users` WHERE `tg` = {message.chat.id}")

                if len(myresult) > 0:

                    out = datetime.strftime(currentdate,'%Y-%m-%d')+ "  " + formatweekday.format_weekday(currentdate.weekday()) +'\n'
                    out = out+" "'\n'
                    for x in myresult:
                        a = str(x).replace("(","")
                        a = a.replace(")","")
                        a = a.replace(",","")
                        a = a.replace("'","")
                    
                    hw = kundelik.get_hw(token=a, date = currentdate)
                    print(hw)

                    for i in hw:
                        out = out+"----------"+i[1]+"----------"+'\n'
                        out = out+i[0]+'\n'
                    
                    out = out + "------------------------------------------------------------"

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = types.KeyboardButton("Назад")
                    btn2 = types.KeyboardButton("Далее")
                    btn3 = types.KeyboardButton("Оценки")
                    markup.add(btn1, btn2, btn3)

                    bot.send_message(message.chat.id, text=out, reply_markup=markup)

            if message.text == "Оценки":
                myresult = db.getdata(f"SELECT dn FROM `users` WHERE `tg` = {message.chat.id}")

                if len(myresult) > 0:
                    a =""
                    for x in myresult:
                        a = str(x).replace("(","")
                        a = a.replace(")","")
                        a = a.replace(",","")
                        a = a.replace("'","")

                bot.send_message(message.chat.id ,kundelik.get_marks(a))
        except requests.exceptions.JSONDecodeError:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "Проблемы на стороне серверов Kundelik")


    else:   
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Неверный запрос")

bot.infinity_polling()

