from aiogram import F, Router, Bot
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, Video, InputMediaVideo, ForceReply
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.middlewares import Test # импорт мидлвари
import app.database.requests as rq
import datetime
from app.database.requests import MyCallback
from app.database.models import async_session
from app.database.models import  Preposition, Words
from sqlalchemy import select, func
from aiogram.methods import DeleteMessage, EditMessageText
import os
import math
import time
bot = Bot(token=os.getenv('TOKEN'))
class SomeClass(StatesGroup): # FSM
    translation = State()
    number = State()
    uncountable = State()
    word = State()
    trans = State()
    list = State()


class Counter():
    rightans = 0
    counter = 0
    

router = Router()

router.message.middleware(Test())

@router.message(Command("admin"))
async def openkeyboard(message: Message):
    await message.answer('admin', reply_markup=kb.admin)

@router.message(F.text == "back to main")
async def openkeyboard(message: Message):
    await message.answer( 'main', reply_markup=kb.main)   

# Get filter result as handler argument
'''
@router.message(F.text.as_('var')) 
async def cmd_star(message: Message, var):
    await message.answer("любой текст : " + var)
'''    

# if we catch the result by first handler and have a match with another, the next wont be working
'''
@router.message(F.date.func(lambda date: date.strftime("%X") > '09:00:00'))
async def cmd_start(message: Message):
    await message.answer(text= "hello", reply_markup= kb.main)
'''    

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('start', reply_markup= kb.main)


# ФИЛЬТР ПО НЕСКОЛЬКИМ ПАРАМЕТРАМ        
'''
@router.message((F.text == "привет") & (F.from_user.id == 15526957)) 
async def cmd_star(message: Message):
    await message.answer(f"привет!\n твой id:")
'''














# обработка колбэков от кнопки инлайн клавиатуры
@router.message(F.text == "Uncountable words")
async def res(calllback: Message): 
    await calllback.answer(text= await rq.retrieve_words())   


no_duplicate = []
askforstop = [10, 20, 30, 40, 50]
counter= Counter
@router.callback_query(MyCallback.filter())
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
    async with async_session() as session:
        prep = await session.scalar(select(Preposition.prep).where(Preposition.id == int(callback_data.r)))
        max = await session.scalar(select(func.max(Preposition.id)))
        no_duplicate.append(int(callback_data.r))
        if prep == callback_data.b:
            counter.rightans += 1
            counter.counter += 1
            await query.answer("✅ Right")
            rand = await rq.randforsentense(Preposition.id)
            if len(no_duplicate)%10 == 0:
                await query.message.edit_text(text= '10 выполнено, продолжить?', reply_markup =kb.settings)
            else:
                    
                if len(no_duplicate) < max:
                    while rand in no_duplicate:
                        rand = await rq.randforsentense(Preposition.id)
                    await query.message.edit_text(text= await rq.retrieve_sentense(rand), reply_markup= await rq.inlinebuttons(rand)) 
                else:
                    no_duplicate.clear()
                    rate = round(counter.rightans / counter.counter * 100, 2)
                    counter.rightans = 0
                    counter.counter = 0
                    await query.message.edit_text(text= f'Все задания пройдены\nпроцент правильных ответов ={rate}% ')

        else:
            await query.answer("❌ Wrong")
            counter.counter += 1
            desc = await session.scalar(select(Preposition.description).where(Preposition.id == int(callback_data.r)))    
            await query.message.edit_text(text= desc, reply_markup =kb.settings)


@router.message(F.text == "Learn prepositions")
async def learnprep(message: Message):
    rand = await rq.randforsentense(Preposition.id)
    await message.answer(text= await rq.retrieve_sentense(rand), reply_markup= await rq.inlinebuttons(rand))      

@router.callback_query(F.data == "Learn prepositions") # тут будет ошибка при переборе заданий
async def learnprep(query: CallbackQuery):
    rand = await rq.randforsentense(Preposition.id)
    while rand in no_duplicate:
        rand = await rq.randforsentense(Preposition.id)
    await query.message.edit_text(text= await rq.retrieve_sentense(rand), reply_markup= await rq.inlinebuttons(rand))  

@router.callback_query(F.data == "exit")
async def learnprep(query: CallbackQuery):
    no_duplicate.clear()
    rate = round(counter.rightans / counter.counter * 100, 2)
    counter.rightans = 0
    counter.counter = 0
    await query.message.edit_text(text= f'процент правильных ответов ={rate}% ')      


@router.callback_query(F.data == "2")
async def res(calllback: CallbackQuery):
    calllback.answer("done") 
    await calllback.message.answer_media_group(media= await rq.retrieve_photo("2"))    
    await calllback.message.answer_location(latitude= await rq.send_latitude("2"), longitude= await rq.send_longitude("2"), reply_markup= await kb.inlinebuttons()) 


    
      



# СОСТОЯНИЯ НА ДОБАВЛЕНИЕ НЕИСЧИСЛЯЕМЫХ СЛОВ
@router.message(F.text == "write Uncountable")
async def somereg(message: Message, state: FSMContext):
    await state.set_state(SomeClass.uncountable)
    await message.answer("добавьте слова")

@router.message(SomeClass.uncountable)
async def somereg1(message: Message, state: FSMContext):
    await state.update_data(uncountable = message.text)
    await state.set_state(SomeClass.translation)
    await message.answer("добавьте перевод")    

@router.message(SomeClass.translation, F.text)
async def somereg1(message: Message, state: FSMContext):
    await state.update_data(translation = message.text)
    data = await state.get_data()
    await rq.write_words(data["uncountable"], data["translation"])
    await message.answer("добавлено")    



# СОСТОЯНИЕ НА ДОБАВЛЕНИЕ id    
@router.message(Command("addid"))
async def somereg(message: Message, state: FSMContext):
    await state.set_state(SomeClass.number)
    await message.answer("добавьте id пользователя")

@router.message(SomeClass.number)
async def somereg5(message: Message, state: FSMContext):
    await state.update_data(number = message.text)
    data = await state.get_data()
    if await rq.add_user(data["number"]):
        await message.answer("добавлено")
        await state.clear()       
    else: 
        await message.answer("пользователь уже добавлен")
        await state.clear()


no_duplicate2 = []
@router.message(F.text == "Learn words")
async def takeoutfromdb1(message: Message, state: FSMContext):
    async with async_session() as session:
        await state.set_state(SomeClass.word)
        max = await session.scalar(select(func.max(Words.id)))
        if len(no_duplicate2) < max:
            rand = await rq.randforsentense(Words.id)
            while rand in no_duplicate2:
                rand = await rq.randforsentense(Words.id)
            no_duplicate2.append(rand)    
            list = await rq.retrieve_word(Words.word, rand)
            list2 = await rq.retrieve_word(Words.translation, rand)
            await state.update_data(list = list, list2 = list2)
            await message.answer(text = list[0])
        else:  
            no_duplicate2.clear()
            await message.answer('слова закончились')
            
# reply_markup= ForceReply(input_field_placeholder= 'Write translation') выше 
    

@router.message(SomeClass.word)
async def takeoutfromdb(message: Message, state: FSMContext):
    await state.update_data(word = [message.text, message.message_id])
    data = await state.get_data()
    await bot.edit_message_text('я удалюсь через 5 сек', inline_message_id= str(data['word'][1]))

    time.sleep(5)
    await bot.delete_message(chat_id=155269575, message_id= data['word'][1])
    if data['word'][0].casefold() in data['list2']:
        await state.clear()
        await takeoutfromdb1(message, state)
    else: 
        await state.clear()   
        await message.answer(f"Варианты правильного перевода: {' '.join(data['list2'])}") 
          