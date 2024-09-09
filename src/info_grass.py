import requests

def login_grass(email: str, password: str, proxy: str = None):
    session = requests.Session()
    
    if proxy:
        session.proxies = {
            "http": proxy,
            "https": proxy
        }
    
    headers = {
        "authority": "api.getgrass.io",
        "accept": "*/*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://app.getgrass.io",
        "referer": "https://app.getgrass.io/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    
    login_data = {
        "username": email,
        "password": password
    }
    
    login_response = session.post("https://api.getgrass.io/login", headers=headers, json=login_data)
    
    if login_response.status_code != 200:
        return {"error": "Login failed", "status_code": login_response.status_code}
    
    login_data = login_response.json()
    access_token = login_data["result"]["data"]["accessToken"]
    
    headers["authorization"] = access_token
    headers["accept"] = "application/json, text/plain, */*"
    
    user_response = session.get("https://api.getgrass.io/retrieveUser", headers=headers)
    
    if user_response.status_code != 200:
        return {"error": "Failed to retrieve user data", "status_code": user_response.status_code}
    
    user_data = user_response.json()
    
    return {
        "login_response": login_data,
        "user_data": user_data
    }
