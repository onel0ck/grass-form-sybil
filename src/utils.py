from loguru import logger
import sys
from typing import List, Tuple
from config import LOG_FILE, LOG_RESULT_DIR

def setup_logger():
    LOG_RESULT_DIR.mkdir(exist_ok=True)

    logger.remove()
    
    logger.add(sys.stderr, format="{time} - {level} - {message}", level="DEBUG")
    
    logger.add(LOG_FILE, rotation="10 MB", compression="zip", level="DEBUG")

setup_logger()

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
