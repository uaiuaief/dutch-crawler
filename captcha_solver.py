from config import TWOCAPTCHA_API_KEY
from twocaptcha import TwoCaptcha

twocaptcha_config = {
        'server': '2captcha.com',
        'apiKey': TWOCAPTCHA_API_KEY,
        'softId': 123,
        #'callback': 'https://your.site/result-receiver',
        'defaultTimeout': 120,
        'recaptchaTimeout': 600,
        'pollingInterval': 10,
        }

solver = TwoCaptcha(**twocaptcha_config)
