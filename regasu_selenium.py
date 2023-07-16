import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
site_packages_dir = os.path.join(current_dir, 'site-packages')
sys.path.append(site_packages_dir)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import linebot.v3.messaging
from linebot.v3.messaging.models.push_message_request import PushMessageRequest
from linebot.v3.messaging.rest import ApiException
from linebot.v3.messaging import TextMessage
from dotenv import load_dotenv

load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
USER_ID = os.environ['USER_ID']
PASSWORD = os.environ['PASSWORD']

def lambda_handler(event, context):
    driver = webdriver.Chrome()
    driver.get('https://user.shinjuku-shisetsu-yoyaku.jp')
    driver.get('https://user.shinjuku-shisetsu-yoyaku.jp/regasu/reserve/gin_menu')

    elem = driver.find_element(By.XPATH, '//*[@id="contents"]/ul[1]/li[2]/dl/dt/form/input[2]')
    elem.click()
    elem = driver.find_element(By.NAME, "g_riyoushabangou")
    elem.send_keys(USER_ID)
    elem = driver.find_element(By.NAME, "ansyono")
    elem.send_keys(PASSWORD)
    elem = driver.find_element(By.XPATH, '//*[@id="login-area"]/form/p/input')
    elem.click()
    elem = driver.find_element(By.XPATH, '//*[@id="local-navigation"]/dd/ul/li[6]/a')
    elem.click()
    elem = driver.find_element(By.ID, 'btnOK')
    elem.click()
    elem = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div/div/ul[1]/li/a/img')
    elem.click()

    link_texts = ["次施設", "次施設", "翌月", "前施設", "前施設", "翌月", "次施設", "次施設", "翌月", "前施設", "前施設", "翌月"]
    available_dates = []

    for link_text in link_texts:
        try:
            elem = driver.find_element(By.CLASS_NAME, "timetable")
            table = elem.find_element(By.TAG_NAME, 'table')
            tbodies = table.find_elements(By.TAG_NAME, 'tbody')

            for tbody in tbodies:
                date = tbody.find_element(By.TAG_NAME, "th").text
                tds = tbody.find_elements(By.TAG_NAME, "td")
                print(tds[3].text)
                try:
                    elem = tds[3].find_element(By.TAG_NAME, "input")
                except NoSuchElementException as e:
                    # print(e)
                    continue

                available_dates.append(date)

            elem = driver.find_element(By.LINK_TEXT, link_text)
            elem.click()
        except Exception as e:
            print(e)
            break

    configuration = linebot.v3.messaging.Configuration(access_token = CHANNEL_ACCESS_TOKEN)
    user_id = 'U02e32863905dff2c6c9403207a0bc0fd'
    message = f'利用可能な日時: {",".join(available_dates)}'
    with linebot.v3.messaging.ApiClient(configuration) as api_client:
        api_instance = linebot.v3.messaging.MessagingApi(api_client)
        push_message_request = linebot.v3.messaging.PushMessageRequest(to=user_id, messages=[TextMessage(text=message)])

        try:
            api_instance.push_message(push_message_request)
        except Exception as e:
            print("Exception when calling MessagingApi->push_message: %s\n" % e)

    print('end')

    return {
        'statusCode': 200,
        'body': 'done!'
    }
