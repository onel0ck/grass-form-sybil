import os
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
LOG_RESULT_DIR = BASE_DIR / 'log_result'

LOG_RESULT_DIR.mkdir(exist_ok=True)

TIMEOUT_BETWEEN_ACCOUNTS = 52  #seconds
TIMEOUT_BETWEEN_REQUESTS = 3  #seconds

CAPTCHA_API_KEY = "api_key"
CAPTCHA_SITE_KEY = "6Ld7p4MpAAAAAGAOAWjUjWlWQNtGusrmEWStu0Jm"

FORM_ID = "JuHDsxyx"

LOG_FILE = LOG_RESULT_DIR / 'log.txt'

#path
PROXY_FILE = DATA_DIR / 'proxies.txt'
LOGIN_PASSWORD_FILE = DATA_DIR / 'login_password.txt'
SUCCESSFUL_ACCOUNTS_FILE = LOG_RESULT_DIR / 'successful_accounts.txt'
FAILED_ACCOUNTS_FILE = LOG_RESULT_DIR / 'failed_accounts.txt'
REFERRAL_METHODS_FILE = DATA_DIR / 'referral_methods.txt'
ADDITIONAL_INFO_FILE = DATA_DIR / 'additional_info.txt'
