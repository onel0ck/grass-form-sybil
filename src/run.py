import time
import random
from typing import Dict, Any, List
from loguru import logger
from utils import (
    read_proxies, read_login_password, write_account_result,
    read_referral_methods, read_additional_info
)
from config import (
    PROXY_FILE, LOGIN_PASSWORD_FILE, SUCCESSFUL_ACCOUNTS_FILE,
    FAILED_ACCOUNTS_FILE, TIMEOUT_BETWEEN_ACCOUNTS,
    REFERRAL_METHODS_FILE, ADDITIONAL_INFO_FILE
)
from info_grass import login_grass
from form import submit_typeform

def process_account(email: str, password: str, proxies: List[str], referral_method: str, additional_info: str) -> bool:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            proxy = random.choice(proxies)
            grass_data = login_grass(email, password, proxy)
            if "error" in grass_data:
                logger.error(f"Failed to get data for {email}: {grass_data['error']}")
                time.sleep(random.uniform(30, 60))
                continue

            time.sleep(random.uniform(15, 30))

            form_data = {
                "username": grass_data["user_data"]["result"]["data"]["username"],
                "email": email,
                "walletAddress": grass_data["user_data"]["result"]["data"]["walletAddress"],
                "referralCount": grass_data["user_data"]["result"]["data"]["referralCount"],
                "referral_methods": referral_method,
                "additional_info": additional_info,
                "qualifiedReferrals": grass_data["user_data"]["result"]["data"]["qualifiedReferrals"]
            }

            result = submit_typeform(form_data, proxies)
            if "error" in result:
                if "400 Client Error" in str(result["error"]) or "DUPLICATE_ERROR" in str(result["error"]) or "404" in str(result["error"]):
                    logger.warning(f"Attempt {attempt + 1}/{max_retries}: Error for {email}. Error: {result['error']}. Retrying with a different proxy.")
                    time.sleep(random.uniform(60, 120))
                    continue
                else:
                    logger.error(f"Failed to submit form for {email}: {result['error']}")
                    return False

            logger.success(f"Successfully processed account {email}")
            return True
        except Exception as e:
            logger.error(f"An unexpected error occurred while processing {email}: {str(e)}")
            if attempt < max_retries - 1:
                logger.debug(f"Retrying with a different proxy. Attempt {attempt + 2}/{max_retries}")
                time.sleep(random.uniform(90, 180))
            else:
                return False
    
    logger.error(f"Failed to process account {email} after {max_retries} attempts")
    return False

def main():
    try:
        proxies = read_proxies(PROXY_FILE)
        accounts = read_login_password(LOGIN_PASSWORD_FILE)
        referral_methods = read_referral_methods(REFERRAL_METHODS_FILE)
        additional_infos = read_additional_info(ADDITIONAL_INFO_FILE)
    except Exception as e:
        logger.error(f"Failed to read necessary files: {str(e)}")
        return

    if not accounts:
        logger.error("No valid accounts found in the login_password file.")
        return

    for i, account in enumerate(accounts):
        if len(account) != 2:
            logger.error(f"Invalid account data at index {i}: {account}")
            continue

        email, password = account
        try:
            referral_method = referral_methods[i % len(referral_methods)]
            additional_info = additional_infos[i % len(additional_infos)]
            
            success = process_account(email, password, proxies, referral_method, additional_info)
            
            if success:
                write_account_result(SUCCESSFUL_ACCOUNTS_FILE, f"{email}:{password}")
            else:
                write_account_result(FAILED_ACCOUNTS_FILE, f"{email}:{password}")
        except Exception as e:
            logger.error(f"Failed to process account {email}: {str(e)}")
            write_account_result(FAILED_ACCOUNTS_FILE, f"{email}:{password}")
        
        try:
            wait_time = random.uniform(TIMEOUT_BETWEEN_ACCOUNTS, TIMEOUT_BETWEEN_ACCOUNTS * 1.5)
            logger.info(f"Waiting {wait_time:.2f} seconds before next account...")
            time.sleep(wait_time)
        except KeyboardInterrupt:
            logger.info("Script interrupted by user. Exiting...")
            break

if __name__ == "__main__":
    logger.info("Starting Grass Form submission process...")
    try:
        main()
    except Exception as e:
        logger.error(f"An unexpected error occurred in the main function: {str(e)}")
    finally:
        logger.info("Script execution completed.")
