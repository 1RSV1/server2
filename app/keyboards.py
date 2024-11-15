from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime
import app.database.requests as rq

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Learn words"),KeyboardButton(text = "Uncountable words")],
                                     [KeyboardButton(text = "Learn prepositions"), 
                                      KeyboardButton(text = "/admin")] ], resize_keyboard= True, input_field_placeholder= "Choose the button")

admin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "write Uncountable")],
                                     [KeyboardButton(text = "кнопка 2"), 
                                      KeyboardButton(text = "back to main")] ], resize_keyboard= True, input_field_placeholder= "Choose the button")

emptykeyboard = ReplyKeyboardMarkup(keyboard= [[]], input_field_placeholder= 'Write translation')

#одно значение будет истиным, два остальных ложные с пояснением в отдельном хэндлере, где будет предложение продолжить?
choice = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="название кнопки", callback_data="response"), 
                                                InlineKeyboardButton(text="название кнопки", callback_data="response"), 
                                                InlineKeyboardButton(text="название кнопки", callback_data="response")]])

settings = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="continue", callback_data="Learn prepositions"), InlineKeyboardButton(text="exit", callback_data="exit")]])

buttons = ["1", "Обновить" ] # InlineKeyboardBuilder
async def add_day(p):
    buttons.insert(-1, str(p))
    return buttons
   
    

       


async def inlinebuttons(): # создание клавиатуры через функцию исходя из данных из бд (BUILDER)
    keyboard = InlineKeyboardBuilder()
    for button in buttons[:-1]:     
        keyboard.add(InlineKeyboardButton(text = button, callback_data= button )) 
    for button in buttons[-1:]:
        keyboard.add(InlineKeyboardButton(text = button, callback_data= "res"))    
            
    return keyboard.adjust(2).as_markup()     #adjust(2).


