from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text = 'Buy a bot')]], 
    resize_keyboard=True, 
    input_field_placeholder='What are you interested in'
)

main_admin = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text = 'Buy a bot')], [KeyboardButton(text = 'Send a message to everyone')], [KeyboardButton(text = 'Issue subscription')]], 
    resize_keyboard=True, 
    input_field_placeholder='What are you interested in'
)

main_sub = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text = 'Find out the number of days of subscription')]], 
    resize_keyboard=True, 
    input_field_placeholder='What are you interested in'
)

cancel = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text = 'Cancel')]], 
    resize_keyboard=True,
)
