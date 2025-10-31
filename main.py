from selenium import webdriver
from selenium.common import NoAlertPresentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime
import asyncio
import logging
import os
from dotenv import load_dotenv, dotenv_values

from webdriver_manager.chrome import ChromeDriverManager

LECTION_TIME = datetime.time(12, 30, 25)

logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s")

handler1 = logging.StreamHandler()
handler1.setFormatter(formatter)
logger2.addHandler(handler1)

handler2 = logging.FileHandler("py_log.log", mode='a')
handler2.setFormatter(formatter)
logger2.addHandler(handler2)


#logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a", format="[%(asctime)s] [%(levelname)s]: %(message)s")
load_dotenv()
s = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
load_dotenv()

async def open_lection():
    f = True
    cnt = 0
    while f and cnt < 4:
        try:
            driver = webdriver.Chrome(service=s, options=chrome_options)
            driver.get('https://stavmirea.ru/')
            name_field = driver.find_element(by=By.ID, value='lgn')
            pass_field = driver.find_element(by=By.ID, value='login-password')
            submit_button = driver.find_element(by=By.CSS_SELECTOR, value='input.btn.btn-success')
            name_field.send_keys(os.getenv("LOGIN"))
            await asyncio.sleep(1)
            pass_field.send_keys(os.getenv("PASSWORD"))
            await asyncio.sleep(1)
            submit_button.click()
            await asyncio.sleep(2)
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except NoAlertPresentException:
                logger2.info("Нет всплывающего окна")
            await asyncio.sleep(3)
            driver.get('https://stavmirea.ru/rasp_ochn.php')
            await asyncio.sleep(3)
            lection_buttons = driver.find_elements(by=By.CSS_SELECTOR, value='a.btn.btn-success')
            if len(lection_buttons) <= 1:
                logger2.error("Нет кнопки входа в лекцию", exc_info=True)
                driver.close()

                await asyncio.sleep(240)
                continue
            for a in lection_buttons:
                a.click()
            logger2.info("Лекцию удалось посетить")
            f = False
            driver.minimize_window()
        except Exception as er:

            logger2.error("Не удалось зайти на лекцию", exc_info=True)

        cnt += 1
        await asyncio.sleep(240)
    logger2.info("Цикл входа в лекцию закончен")


async def main():
    #https://github.com/jsnjack/chromedriver/releases
    while True:
        now = datetime.datetime.now()
        now_time = now.time()
        if now_time > LECTION_TIME:
            logger2.info("Запущен вход в лекцию")
            #os.system("shutdown -s -t 7200")
            await open_lection()
            break
        logger2.info("Итерация проверки")
        await asyncio.sleep(120)


if __name__ == '__main__':
    asyncio.run(main())


