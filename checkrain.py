from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
from datetime import datetime
from config import TOKEN
from bot import BotBD
import asyncio
from aiogram import Bot, Dispatcher

BotBD = BotBD('users.db')

bot = Bot(token=TOKEN)

loop = asyncio.new_event_loop()

dp = Dispatcher()

async def run_selenium():
    while True:
        try:
            current_time = datetime.now()
            agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            driver = Driver(uc=True, log_cdp=True, headless2=True, no_sandbox=True, agent=agent, proxy=False)
            print(f'{current_time} | Create driver')
            current_time = datetime.now()
            driver.get('https://bandit.camp/')
            print(f'{current_time} | Connected to the site')
            rain_event_found = False
            text_rain = ''
            message_ids = []
            temp_lenght = 0
            working_driver = True
        except Exception as e:
            current_time = datetime.now()
            print(f'{current_time} | Failed to connect to the site: {e}')
            time.sleep(60)
        while True:
            try:
                chat = driver.find_element(By.CLASS_NAME, 'chat-footer')
                findRain = chat.find_element(By.CLASS_NAME, 'v-btn__content')
                if (findRain.text == 'JOIN RAIN EVENT'):
                    if not rain_event_found:
                        await asyncio.sleep(5)
                        try:
                            checkBonus = chat.find_element(By.CLASS_NAME, 'd-inline-flex')
                            bonus = float(checkBonus.text.replace(',', '.'))
                        except Exception as e:
                            print(e)
                            bonus = 0
                        current_time = datetime.now()
                        print(f'{current_time} | Finded rain')
                        for row in BotBD.get_users():
                            try:
                                text_rain = f'Finded Rain: <b>{"{:.2f}".format(bonus)}</b>\n\nStatus: <u>in progress</u>'
                                message = await bot.send_message(row[0], text_rain, parse_mode="html")
                                message_ids.append((row[0], message.message_id))
                            except Exception as e:
                                print(f"Error sending rain notification: {e}")
                        rain_event_found = True
                    else:
                        try:
                            checkChat = driver.find_element(By.CLASS_NAME, 'chat-messages')
                            newBonus = checkChat.find_elements(By.CLASS_NAME, 'scrap')
                            msg_mass = list(newBonus[i] for i in range(len(newBonus)))
                            msg = list(float(msg_mass[i].text.replace(',', '.')) for i in range(len(msg_mass)))
                            if(temp_lenght!=len(msg_mass)):
                                temp_lenght = len(msg_mass)
                                current_time = datetime.now()
                                print(f'{current_time} | Found rain with changed conditions')
                                text_rain = f'Finded Rain: <b>{"{:.2f}".format(bonus + sum(msg))}$</b>'
                                for i in range(len(msg)):
                                    text_rain += f'\n\nSomeone tipped <blockquote>{"{:.2f}".format(msg[i])}$</blockquote> into the rain.'
                                text_rain +='\n\nStatus: <u>in progress</u>'
                                for user_id, message_id in message_ids:
                                    try:
                                        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=text_rain, parse_mode="html")
                                    except Exception as e:
                                        print(f"Error editing rain notification: {e}")
                        except Exception as e:
                            print(f'Error when resending rain: {e}')
                elif(rain_event_found):
                    text_rain = text_rain.replace('in progress', 'finished')
                    for user_id, message_id in message_ids:
                        try:
                            await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=text_rain, parse_mode="html")
                        except Exception as e:
                                        print(f"A mistake at the finish of the rain: {e}")
                    current_time = datetime.now()
                    print(f'{current_time} | Finished rain')
                    driver.quit()
                    time.sleep(10)
                    break
            except WebDriverException  as e:
                current_time = datetime.now()
                print(f'{current_time} | Occurred when there was an error working with WebDriver: {e}')
                if(working_driver):
                    await asyncio.sleep(5)
                    working_driver = False
                else:
                    current_time = datetime.now()
                    print(f'{current_time} | Reboot WebDriver...')
                    driver.quit()
                    time.sleep(10)
                    break
            except Exception as e:
                current_time = datetime.now()
                print(f'{current_time} | Exception in func CheckRain: {e}')
            
