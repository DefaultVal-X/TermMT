
from typing import List
import requests
import uuid
from tenacity import retry
from joblib import Parallel, delayed

import os
import json

# Load Bing API key from environment variable
BING_SUBSCRIPTION_KEY = os.getenv("BING_TRANSLATOR_KEY", "")
BING_TRANSLATOR_REGION = os.getenv("BING_TRANSLATOR_REGION", "")

def translate_text_with_bing(text: str) -> str:
    '''
    Copied from: https://github.com/MicrosoftTranslator/Text-Translation-Code-Samples
    '''

    # Add your subscription key and endpoint
    subscription_key = BING_SUBSCRIPTION_KEY
    endpoint = "https://api.cognitive.microsofttranslator.com"

    if not subscription_key or subscription_key == "YOUR_BING_TRANSLATION_KEY":
        raise RuntimeError("BING_TRANSLATOR_KEY is not set")
    
    # Region may differ by resource. Keep it configurable.
    # For some Translator resources, this header can be omitted.
    location = BING_TRANSLATOR_REGION
    path = '/translate'
    constructed_url = endpoint + path
    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': 'zh'
    }
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    if location:
        headers['Ocp-Apim-Subscription-Region'] = location

    # You can pass more than one object in body.
    body = [{'text': text}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body, timeout=30)
    request.raise_for_status()
    response = request.json()

    # Success payload is a list; error payload is usually a dict with an "error" field.
    if isinstance(response, dict):
        err = response.get("error", {})
        code = err.get("code", "unknown")
        message = err.get("message", str(response))
        raise RuntimeError(f"Bing translate API error ({code}): {message}")

    if not isinstance(response, list) or len(response) == 0:
        raise RuntimeError(f"Unexpected Bing response: {response}")

    first = response[0]
    translations = first.get("translations", []) if isinstance(first, dict) else []
    if not translations:
        raise RuntimeError(f"Bing response missing translations: {response}")

    text_out = translations[0].get("text", "")
    if text_out == "":
        raise RuntimeError(f"Bing translated text is empty: {response}")
    return text_out

def translate_text_with_bing_batch(text: List[str]) -> List[str]:
    ret = Parallel(n_jobs=16, backend="threading")(delayed(translate_text_with_bing)(t) for t in text)
    return ret

# print(translate_text_with_bing("Hi"))