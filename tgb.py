import sqlite3
import telebot

bot = telebot.TeleBot('6453851613:AAETCA9dthP_bVYJGuMY7DVwg-bpn-OjPVw')


conn = sqlite3.connect('phonebook.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone_number TEXT)''')
conn.commit()
conn.close()

def view_contacts():
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def save_contact(name, phone_number):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone_number) VALUES (?, ?)", (name, phone_number))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я Телефонный справочник. Чтобы добавить контакт, используйте /add')

@bot.message_handler(commands=['add'])
def add_contact(message):
    bot.reply_to(message, 'Введите имя и номер телефона контакта в формате "Имя Номер"')

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.split()
    if len(text) == 2:
        save_contact(text[0], text[1])
        bot.reply_to(message, f'Контакт {text[0]} успешно добавлен!')
    else:
        bot.reply_to(message, 'Неверный формат. Используйте "Имя Номер"')

@bot.message_handler(commands=['view'])
def view(message):
    contacts = view_contacts()
    if len(contacts) > 0:
        response = 'Контакты:\n'
        for contact in contacts:
            response += f'{contact[1]}: {contact[2]}\n'
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, 'У вас пока нет контактов.')

bot.polling()