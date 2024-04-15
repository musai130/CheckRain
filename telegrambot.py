
from aiogram.filters import Command, StateFilter
from bot import BotBD
import asyncio
from aiogram import Bot, Dispatcher, types
import keyboards as kb
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message, CallbackQuery
import time
from config import TOKEN
import datetime
BotBD = BotBD('users.db')

bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        return dt

def day_to_seconds(days):
        return days * 24 * 60 * 60

@dp.message(Command('start'))
async def start_cmd(message: types.Message):
    if not BotBD.user_exists(message.from_user.id):
        BotBD.add_user(message.from_user.id)
        await message.bot.send_message(message.from_user.id, f'Hi! {message.from_user.id}', reply_markup=kb.main)
    if BotBD.check_admin(message.from_user.id): 
        await message.bot.send_message(message.from_user.id, 'Hi!\n\nYou are logged in as admin', reply_markup=kb.main_admin)
    elif BotBD.get_sub_status(message.from_user.id):
        await message.bot.send_message(message.from_user.id, f'Hi! {message.from_user.id}', reply_markup=kb.main_sub)
    else:
        await message.bot.send_message(message.from_user.id, f'Hi! {message.from_user.id}', reply_markup=kb.main)

class FSMFillForm(StatesGroup):
    fill_id = State()
    fill_days = State()
    msg = State()
    send_msg = State()
@dp.message(F.text.lower() == 'cancel', StateFilter(default_state))
async def process_cancel_command(message: Message):
    if(BotBD.check_admin(message.from_user.id)):
        await message.answer(text='Nothing to cancel', reply_markup=kb.main_admin)
    else:
        await message.answer(text='Nothing to cancel', reply_markup=kb.main)

@dp.message(F.text.lower() == 'cancel', ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    if(BotBD.check_admin(message.from_user.id)):
        await message.answer(text='Canceled', reply_markup=kb.main_admin)
    else:
        await message.answer(text='Canceled', reply_markup=kb.main)
    await state.clear()
@dp.message(F.text.lower() == 'issue subscription', StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    if(BotBD.check_admin(message.from_user.id)):
        await message.answer(text='User ID', reply_markup=kb.cancel)
        await state.set_state(FSMFillForm.fill_id)
    else:
        await message.answer(text='You are not an admin', reply_markup=kb.main)

@dp.message(StateFilter(FSMFillForm.fill_id), F.text.isnumeric())
async def process_id_sent(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.answer(text='Number of days of subscription', reply_markup=kb.cancel)
    await state.set_state(FSMFillForm.fill_days)

@dp.message(StateFilter(FSMFillForm.fill_id))
async def warning_not_id(message: Message):
    await message.answer(text='You invalid', reply_markup=kb.cancel)

@dp.message(StateFilter(FSMFillForm.fill_days),
            lambda x: x.text.isdigit() and 0 <= int(x.text) <= 365)
async def process_days_sent(message: Message, state: FSMContext):
    await state.update_data(days=message.text)
    add_sub_time = await state.get_data()
    id_user = int(add_sub_time['id']); sub_time_days = int(add_sub_time['days'])
    sub_time = int(time.time()) + day_to_seconds(sub_time_days)
    BotBD.set_time_sub(sub_time, id_user)
    await message.answer(text=f'You have added user: id: {id_user}, days: {sub_time_days}', reply_markup=kb.main_admin)
    try:
        if(not BotBD.check_admin(id_user)):
            await message.bot.send_message(id_user, f'Congratulations! You have been given a subscription for <blockquote>{sub_time_days}</blockquote> days', parse_mode='html', reply_markup=kb.main_sub)
    except:
        pass
    await state.clear()

@dp.message(StateFilter(FSMFillForm.fill_days))
async def warning_not_days(message: Message):
    await message.answer(text='You invalid', reply_markup=kb.cancel)

@dp.message(F.text.lower() == 'buy a bot')
async def Buy_Bot(message: types.Message):
    await message.answer(f"To buy a bot, send your UserID here\n\nYour UserID: <blockquote><code>{message.from_user.id}</code></blockquote>", parse_mode='html')

@dp.message(F.text.lower() == 'send a message to everyone', StateFilter(default_state))
async def Send_Message(message: types.Message, state: FSMContext):
    if(BotBD.check_admin(message.from_user.id)):
        await message.answer(text='Enter your message', reply_markup=kb.cancel)
        await state.set_state(FSMFillForm.msg)
    else:
        await message.answer(text='You are not an admin', reply_markup=kb.main)
    

@dp.message(StateFilter(FSMFillForm.msg))
async def process_id_sent(message: Message, state: FSMContext):
    await state.update_data(msg=message.text)
    msg = await state.get_data()
    msg_send = msg['msg']
    await message.answer(text = msg_send, reply_markup=kb.notify_users, parse_mode='markdownV2')


@dp.message(F.text.lower() == 'find out the number of days of subscription')
async def Check_Sub(message: types.Message):
    if(not BotBD.check_admin(message.from_user.id)):
        user_sub = time_sub_day(BotBD.get_time_sub(message.from_user.id))
        if user_sub == False:
            await message.answer('You dont have a subscription', reply_markup=kb.main)
        else: 
            await message.answer(f'Before your subscription ends: {user_sub}', reply_markup=kb.main_sub)
    else:
        await message.answer('You admin', reply_markup=kb.main_admin)


@dp.message(F.text.lower() == 'check users')
async def CheckUsers(message: types.Message):
    if(BotBD.check_admin(message.from_user.id)):
        count = 0
        count_sub = 0
        for row in BotBD.get_users():
            if BotBD.get_sub_status(row[0]):
                count_sub+=1
            else:
                count+=1
        await message.answer(f'Users:\n\nSub: {count_sub}\n\nUnsub: {count}', reply_markup=kb.main_admin)    


@dp.callback_query(F.data == 'True_answer')
async def True_answer(callback: CallbackQuery, state: FSMContext):
    msg = await state.get_data()
    msg_send = msg['msg']
    await bot.send_message(callback.from_user.id, 'Message sent to all users', reply_markup=kb.main_admin)
    for row in BotBD.get_users():
        await bot.send_message(row[0], text = msg_send, parse_mode='markdownV2')
    await callback.message.delete()
    await state.clear()

@dp.callback_query(F.data == 'False_answer')
async def False_answer(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, 'Message deleted', reply_markup=kb.main_admin)
    await callback.message.delete()
    await state.clear()


            
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())