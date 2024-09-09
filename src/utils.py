import logging
import os
from typing import List, Tuple
from config import LOGGING_FORMAT, LOGGING_LEVEL, LOG_FILE, LOG_RESULT_DIR

def setup_logger():
    os.makedirs(LOG_RESULT_DIR, exist_ok=True)

    logger = logging.getLogger(__name__)
    logger.setLevel(LOGGING_LEVEL)

    formatter = logging.Formatter(LOGGING_FORMAT)

    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()

def read_file_lines(filename: str) -> List[str]:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return []

def read_proxies(filename: str) -> List[str]:
    return read_file_lines(filename)

def read_login_password(filename: str) -> List[Tuple[str, str]]:
    lines = read_file_lines(filename)
    result = []
    for line in lines:
        parts = line.split(':')
        if len(parts) >= 2:
            result.append((parts[0], parts[1]))
        else:
            logger.warning(f"Ignoring invalid line in {filename}: {line}")
    return result

def write_account_result(filename: str, account: str):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{account}\n")

def read_account_results(filename: str) -> List[Tuple[str, str]]:
    lines = read_file_lines(filename)
    return [tuple(line.split(':')) for line in lines if ':' in line]

def read_referral_methods(filename: str) -> List[str]:
    return read_file_lines(filename)

def read_additional_info(filename: str) -> List[str]:
    return read_file_lines(filename)