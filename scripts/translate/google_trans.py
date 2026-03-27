import os
from typing import List

import requests


# Google Cloud Translation API v2 endpoint (API key auth)
GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")


def _translate_with_google_api(texts: List[str], target: str = "zh", model: str = "nmt") -> List[str]:
    if GOOGLE_TRANSLATE_API_KEY == "":
        raise RuntimeError("GOOGLE_TRANSLATE_API_KEY is not set")

    if len(texts) == 0:
        return []

    payload = {
        "q": texts,
        "target": target,
        "format": "text",
        "model": model,
        "key": GOOGLE_TRANSLATE_API_KEY,
    }

    response = requests.post(GOOGLE_TRANSLATE_ENDPOINT, data=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    if "data" not in data or "translations" not in data["data"]:
        raise RuntimeError(f"Unexpected Google Translate response: {data}")

    return [item.get("translatedText", "") for item in data["data"]["translations"]]


def translate_text_with_google(text: str, target: str = "zh", model: str = "nmt") -> str:
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    return _translate_with_google_api([text], target=target, model=model)[0]


def translate_text_with_google_batch(text: List[str], target: str = "zh", model: str = "nmt") -> List[str]:
    return _translate_with_google_api(text, target=target, model=model)