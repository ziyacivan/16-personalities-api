from typing import List
import requests
from bs4 import BeautifulSoup
import json

from models import Answer

class PersonalitiesClient:
    URL = "https://www.16personalities.com/tr/test-sonu%C3%A7lar%C4%B1"
    URL_API = "https://www.16personalities.com/api/session"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Referer": "https://www.16personalities.com/tr/isfp-ki%C5%9Fili%C4%9Fi",
        "sec-ch-ua": "'Chromium';v='106', 'Google Chrome';v='106', 'Not;A=Brand';v='99'",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "'Windows'",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def send_answers(self, answers: List[dict], gender="Male"):
        payload = {
            "questions": answers,
            "gender": gender,
            "inviteCode": "",
            "teamInviteKey": "",
            "extraData": [],
        }

        request = requests.post(self.URL, headers=self.headers, json=payload)
        cookies = request.headers["set-cookie"]
        cookies = cookies[cookies.find("testResults=") :]

        test_results = cookies[: cookies.find("; expires")]

        headers_for_api = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "tr",
            "cache-control": "max-age=0",
            "cookie": test_results,
            "sec-ch-ua": "'Chromium';v='106', 'Google Chrome';v='106', 'Not;A=Brand';v='99'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "'Windows'",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "referer": "https://www.16personalities.com/tr/isfp-ki%C5%9Fili%C4%9Fi",
        }

        request = requests.get(self.URL_API, headers=headers_for_api)

        response_dict = {}
        response_dict = json.loads(request.text)

        try:
            response_dict = response_dict["user"]
        except Exception:
            return None

        html_result = requests.get(
            response_dict["localized"]["profileUrl"], headers=headers_for_api
        ).text
        soup = BeautifulSoup(html_result, "html.parser")

        element = soup.find("standalone-profile-page-guest")
        data = element[":data"]
        decoded_data = json.loads(data)
        return decoded_data