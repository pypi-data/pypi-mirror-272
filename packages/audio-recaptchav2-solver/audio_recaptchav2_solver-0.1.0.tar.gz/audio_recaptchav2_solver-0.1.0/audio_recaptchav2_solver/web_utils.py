import selenium
from selenium.webdriver.common.by import By
import requests
import time
import os
from .transcriber import transcribe

def record_recaptcha_audio(driver, url, output_filename):
    try:
        driver.execute_script(f"window.open('{url}', '_blank')")
        driver.switch_to.window(driver.window_handles[-1])
        print("recording recaptcha")
        time.sleep(2)
        cookies = driver.get_cookies()
        s = requests.Session()

        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        
        response = s.get(url)

        with open(output_filename, 'wb') as f:
            f.write(response.content)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return True
    except:
        return False
def click_checkbox(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"))
    driver.find_element(By.ID, "recaptcha-anchor-label").click()
    driver.switch_to.default_content()

def request_audio(driver):
    driver.switch_to.default_content()
    time.sleep(1)
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    driver.find_element(By.XPATH, '''//*[@id="recaptcha-audio-button"]''').click()

def solve_audio_captcha(driver,index,recaptcha_audio_location):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    link = driver.find_element(By.XPATH, '''//audio[@id='audio-source']''').get_attribute('src')
    time.sleep(1.5)

    if not os.path.exists(recaptcha_audio_location):
        os.makedirs(recaptcha_audio_location)

    recaptcha_location = rf'{recaptcha_audio_location}\payload_{index}.mp3'
    output = record_recaptcha_audio(driver,driver.find_element(By.XPATH, '''//audio[@id='audio-source']''').get_attribute('src'),recaptcha_location)
    text = transcribe(recaptcha_location)
    print("transcribed audio",text)
    driver.switch_to.default_content()
    time.sleep(1.5)
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    driver.find_element(By.ID, 'audio-response').send_keys(text)
    driver.find_element(By.XPATH, '''//*[@id="recaptcha-verify-button"]''').click()
    driver.switch_to.default_content()

    return output