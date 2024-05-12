from .web_utils import request_audio,solve_audio_captcha,click_checkbox
import time

class captcha_solver:

    def __init__(self,driver,recaptcha_audio_location='audio_solver') -> None:
        self.driver = driver
        self.recaptcha_audio_location = recaptcha_audio_location

    def solve(self):
        time.sleep(2.5)
        request_audio(self.driver)
        time.sleep(1.5)
        status = solve_audio_captcha(self.driver,"audio_recaptcha_library",self.recaptcha_audio_location)
        time.sleep(1.5)

        return status

        
