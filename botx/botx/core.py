from time import sleep
from telebot import TeleBot
from telebot import types
from parser import Parser
from config import TOKEN
from test3 import *
from test3 import chatbot_response
class Bot:
    def __init__(self, token) -> None:
        self.TOKEN = token
        self.bot = TeleBot(token=self.TOKEN, parse_mode="html")
        self.current_index = 0
        self.lst = None
        
        @self.bot.message_handler(commands=["start"])
        def welcome(message):
            self.bot.send_message(message.chat.id,
                     f'Привет {message.from_user.first_name}!\nПривет. Я бот по поиску работы',
                     reply_markup=keyboard_handler_down())

        def keyboard_handler_down():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
            search_job = types.KeyboardButton('Поиск работы')
            markup.add(search_job)
            return markup

        
        
        @self.bot.message_handler(content_types=["text"])
        def handler_down(message):
            if message.text == "Поиск работы":
                self.bot.send_message(message.chat.id, 'Какую профессию ищем?')
                self.bot.register_next_step_handler(message, show_cards)
        

        @self.bot.message_handler(content_types=['text'])
        def keyboard_xz():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
            bck = types.KeyboardButton('Назад')
            nxt = types.KeyboardButton('Далее')
            markup.add(bck, nxt)
            return markup

        def show_cards(message):
            if self.current_index == 0:
                vacansy_name = message.text
                print(vacansy_name)
                self.lst = Parser(vacansy_name).info_to_vac_list()
                self.bot.send_message(message.chat.id,self.__rasparse(self.lst[self.current_index]), reply_markup=keyboard_xz())
                self.current_index+=1
                self.bot.register_next_step_handler(message, show_cards)
            elif message.text == "Назад":
                # self.bot.delete_message(message.chat.id, message.message_id)
                # self.bot.delete_message(message.chat.id, message.message_id-1)
                self.current_index -=1
                self.bot.send_message(message.chat.id,self.__rasparse(self.lst[self.current_index]), reply_markup=keyboard_xz())
                self.bot.register_next_step_handler(message, show_cards)

                print(message.text)
            elif self.current_index > 0 and message.text == "Далее":
                print('fdfd')
                # self.bot.delete_message(message.chat.id, message.message_id)
                # self.bot.delete_message(message.chat.id, message.message_id-1)
                self.current_index +=1
                self.bot.send_message(message.chat.id,self.__rasparse(self.lst[self.current_index]), reply_markup=keyboard_xz())
                self.bot.register_next_step_handler(message, show_cards)
            else:
                self.bot.send_message(message.chat.id, chatbot_response(message.text)) 
                self.bot.register_next_step_handler(message, show_cards)
            


                
            

            
        
    def start(self):
        self.bot.polling(none_stop=True)
        print('бот рабайтен')
    def stop(self):
        pass
    def __rasparse(self,dct:dict):
        out = ''
        for i, v in dct.items():
            
            out+=str(v)+"\n"
        print('gggggggggg')
        return out
bot = Bot(TOKEN)
bot.start()

