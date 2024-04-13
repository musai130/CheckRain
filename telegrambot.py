
from aiogram.filters import Command, StateFilter
from bot import BotBD
import asyncio
from aiogram import Bot, Dispatcher, types
import keyboards as kb
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
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
    if BotBD.check_admin(message.from_user.id): 
        await message.bot.send_message(message.from_user.id, 'Hi!\n\nYou are logged in as admin', reply_markup=kb.main_admin)
    elif BotBD.get_sub_status(message.from_user.id):
        await message.bot.send_message(message.from_user.id, f'Hi! {message.from_user.id}', reply_markup=kb.main_sub)
    else:
        await message.bot.send_message(message.from_user.id, f'Hi! {message.from_user.id}', reply_markup=kb.main)

class FSMFillForm(StatesGroup):
    fill_id = State()
    fill_days = State()
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
    await message.answer(text='invalid syntax', reply_markup=kb.cancel)

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
    await message.answer(text='invalid syntax', reply_markup=kb.cancel)

@dp.message(F.text.lower() == 'buy a bot')
async def Buy_Bot(message: types.Message):
    await message.answer(f"To buy a bot, send your UserID here\n\nYour UserID: <blockquote><code>{message.from_user.id}</code></blockquote>", parse_mode='html')

@dp.message(F.text.lower() == 'send a message to everyone')
async def Send_Message(message: types.Message):
    if(BotBD.check_admin(message.from_user.id)):
        await message.answer("")
    
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
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
