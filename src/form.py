import requests
import random
import time
from typing import Dict, Any
import json
from loguru import logger
import uuid

from config import FORM_ID, CAPTCHA_API_KEY, CAPTCHA_SITE_KEY

class TypeformSubmitter:
    def __init__(self, form_id: str, proxy: str = None):
        self.form_id = form_id
        self.session = requests.Session()
        if proxy:
            self.session.proxies = {
                "http": proxy,
                "https": proxy
            }
        self.base_url = f"https://ywnom4oq1na.typeform.com"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        })
        self.response_id = None
        self.signature = None
        self.landed_at = int(time.time())

    def _generate_fingerprint(self):
        return str(uuid.uuid4())

    def start_submission(self) -> None:
        logger.debug("Starting submission")
        url = f"{self.base_url}/forms/{self.form_id}/start-submission"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/to/{self.form_id}",
        }
        data = {
            "visit_response_id": self._generate_random_id(),
            "browser_fingerprint": self._generate_fingerprint()
        }
        
        time.sleep(random.uniform(3, 5))
        try:
            response = self.session.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            self.signature = response_json["signature"]
            self.response_id = response_json["submission"]["response_id"]
            self.landed_at = response_json["submission"]["landed_at"]
            logger.debug(f"Submission started. Response ID: {self.response_id}")
        except Exception as e:
            logger.error(f"Error in start_submission: {str(e)}")
            logger.debug(f"Response content: {response.text}")
            logger.debug(f"Request headers: {headers}")
            logger.debug(f"Request data: {data}")
            raise

    def see_field(self, field_id: str, previous_field_id: str) -> None:
        logger.debug(f"Seeing field: {field_id}")
        url = f"{self.base_url}/forms/{self.form_id}/insights/events/v3/see"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/to/{self.form_id}",
        }
        data = {
            "form_id": self.form_id,
            "field_id": field_id,
            "previous_seen_field_id": previous_field_id,
            "response_id": self.response_id,
            "user_agent": self.user_agent,
            "version": "1"
        }
        
        time.sleep(random.uniform(0.5, 1.5))
        
        try:
            response = self.session.post(url, headers=headers, data=data)
            response.raise_for_status()
            logger.debug(f"Field {field_id} seen successfully")
        except Exception as e:
            logger.error(f"Error in see_field: {str(e)}")
            logger.debug(f"Response content: {response.text}")
            raise

    def submit_form(self, data: list, captcha_token: str) -> Dict[str, Any]:
        logger.debug("Submitting form")
        url = f"{self.base_url}/forms/{self.form_id}/complete-submission"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/to/{self.form_id}",
        }
        
        payload = {
            "signature": self.signature,
            "form_id": self.form_id,
            "landed_at": self.landed_at,
            "answers": data,
            "thankyou_screen_ref": "afd1dc99-dc16-4129-a95f-a9c3815d9bf4",
            "respondent_validation": {
                "recaptcha_v2": captcha_token
            }
        }
        
        time.sleep(random.uniform(1, 3))
        
        try:
            response = self.session.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.success("Form submitted successfully")
            return response.json()
        except Exception as e:
            logger.error(f"Error in submit_form: {str(e)}")
            logger.debug(f"Response content: {response.text}")
            logger.debug(f"Request headers: {headers}")
            logger.debug(f"Request payload: {payload}")
            raise

    def _generate_random_id(self) -> str:
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=12))


def solve_captcha_with_capmonster(api_key: str, site_key: str, url: str) -> str:
    logger.debug("Starting captcha solving process with CapMonster")
    capmonster_url = "https://api.capmonster.cloud/createTask"
    get_result_url = "https://api.capmonster.cloud/getTaskResult"

    create_task_payload = {
        "clientKey": api_key,
        "task": {
            "type": "NoCaptchaTaskProxyless",
            "websiteURL": url,
            "websiteKey": site_key
        }
    }
    
    response = requests.post(capmonster_url, json=create_task_payload)
    response.raise_for_status()
    task_result = response.json()
    
    if task_result.get("errorId") > 0:
        error_msg = f"Error creating captcha task: {task_result.get('errorDescription')}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    task_id = task_result["taskId"]
    logger.debug(f"Captcha task created. Task ID: {task_id}")
    
    for attempt in range(30):
        time.sleep(2)
        get_result_payload = {
            "clientKey": api_key,
            "taskId": task_id
        }
        response = requests.post(get_result_url, json=get_result_payload)
        response.raise_for_status()
        result = response.json()
        
        if result.get("status") == "ready":
            logger.success("Captcha solved successfully")
            return result["solution"]["gRecaptchaResponse"]
        logger.debug(f"Waiting for captcha solution. Attempt {attempt + 1}/30")
    
    logger.error("Captcha solving timeout")
    raise Exception("Captcha solving timeout")

def submit_typeform(data: Dict[str, Any], proxy: str) -> Dict[str, Any]:
    submitter = TypeformSubmitter(FORM_ID, proxy)
    try:
        submitter.start_submission()

        fields = [
            ("WelcomeScreenID", "2VqJcP8bGV0U"),
            ("2VqJcP8bGV0U", "2LBfGiV3dViz"),
            ("2LBfGiV3dViz", "RKoA09chH2Sr"),
            ("RKoA09chH2Sr", "QMiTsYmFayJr"),
            ("QMiTsYmFayJr", "SlEgtoWxA8AK"),
            ("SlEgtoWxA8AK", "n0sPaB7vXRDW"),
            ("n0sPaB7vXRDW", "f0ksNMZzCaTw"),
            ("f0ksNMZzCaTw", "EgLlGtrhVMX5"),
            ("EgLlGtrhVMX5", "cXZkbpTb6ikJ"),
            ("cXZkbpTb6ikJ", "a08yncnElCMX"),
        ]

        for prev_field, current_field in fields:
            submitter.see_field(current_field, prev_field)
            time.sleep(random.uniform(1, 3))

        form_data = [
            {"field": {"id": "2VqJcP8bGV0U", "type": "short_text"}, "type": "text", "text": data.get("username", "")},
            {"field": {"id": "2LBfGiV3dViz", "type": "email"}, "type": "email", "email": data.get("email", "")},
            {"field": {"id": "RKoA09chH2Sr", "type": "short_text"}, "type": "text", "text": data.get("walletAddress", "")},
            {"field": {"id": "QMiTsYmFayJr", "type": "number"}, "type": "number", "number": data.get("qualifiedReferrals", 0)},
            {"field": {"id": "SlEgtoWxA8AK", "type": "number"}, "type": "number", "number": max(0, data.get("referralCount", 0) - data.get("qualifiedReferrals", 0))},
            {"field": {"id": "n0sPaB7vXRDW", "type": "long_text"}, "type": "text", "text": data.get("referral_methods", "")},
            {"field": {"id": "f0ksNMZzCaTw", "type": "yes_no"}, "type": "boolean", "boolean": True},
            {"field": {"id": "EgLlGtrhVMX5", "type": "yes_no"}, "type": "boolean", "boolean": False},
            {"field": {"id": "cXZkbpTb6ikJ", "type": "number"}, "type": "number", "number": random.randint(1, 3)},
            {"field": {"id": "a08yncnElCMX", "type": "short_text"}, "type": "text", "text": data.get("additional_info", "")}
        ]

        captcha_token = solve_captcha_with_capmonster(
            CAPTCHA_API_KEY,
            CAPTCHA_SITE_KEY,
            f"{submitter.base_url}/to/{FORM_ID}"
        )
        
        result = submitter.submit_form(form_data, captcha_token)
        logger.success("Form submission completed")
        return result
    except Exception as e:
        logger.error(f"An error occurred during form submission: {str(e)}")
        return {"error": str(e)}
