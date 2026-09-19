"""
Minimal Gemini / Generative Language API wrapper using API key.
This script uses the Google Generative Language REST endpoint which accepts API keys.
If you actually have a different Gemini endpoint, replace `BASE_URL` accordingly.
"""
import os
import requests
from typing import Tuple, Optional

BASE_URL = "https://generativelanguage.googleapis.com/v1/models/text-bison-001:generateText"


def test_key(api_key: str, prompt: str = "Salom. Iltimos o'zbek tilida qisqacha javob bering.") -> Tuple[bool, Optional[dict]]:
    """
    Test a single API key against the Generative Language endpoint.

    Returns (success, response_json_or_None)
    """
    if not api_key:
        return False, {"error": "empty api key"}

    url = f"{BASE_URL}?key={api_key}"
    payload = {
        "prompt": {"text": prompt},
        "temperature": 0.2,
        "maxOutputTokens": 256
    }

    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        try:
            data = resp.json()
        except Exception:
            data = {"raw_text": resp.text}

        if resp.status_code == 200:
            return True, data
        else:
            return False, {"status_code": resp.status_code, "body": data}
    except Exception as e:
        return False, {"error": str(e)}


if __name__ == "__main__":
    k = os.getenv("GEMINI_KEY_1")
    ok, r = test_key(k)
    print("Key1 result:", ok)
    print(r)
