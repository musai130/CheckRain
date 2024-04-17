from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text = 'Buy a bot')]], 
    resize_keyboard=True, 
    input_field_placeholder='What are you interested in'
)

main_admin = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text = 'Buy a bot')], [KeyboardButton(text = 'Send a message to everyone')], [KeyboardButton(text = 'Issue subscription')], [KeyboardButton(text = 'Check Users')]], 
    resize_keyboard=True, 
    input_field_placeholder='What are you interested in'
)

main_sub = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text = 'Find out the number of days of subscription')]], 
    resize_keyboard=True, 
    input_field_placeholder='What are you interested in'
)

notify_users = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = 'True',  callback_data='True_answer')],  
        [InlineKeyboardButton(text = 'False',  callback_data='False_answer')]
        ]
    )

cancel = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text = 'Cancel')]], 
    resize_keyboard=True,
)
