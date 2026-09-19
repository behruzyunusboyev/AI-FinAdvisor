import os
from pathlib import Path
from dotenv import load_dotenv
import requests

root = Path(r'C:\Users\user\OneDrive\Desktop\loyha hakathone')
load_dotenv(root / '.env')

print('=== KEY STATUS ===')
for name in ['GEMINI_API_KEY', 'GEMINI_API_KEY2', 'GROQ_API_KEY']:
    value = os.getenv(name)
    print(f'{name}: present={bool(value)} len={len(value) if value else 0}')

print('\n=== GEMINI TESTS ===')
for name in ['GEMINI_API_KEY', 'GEMINI_API_KEY2']:
    key = os.getenv(name)
    if not key:
        print(f'{name}: MISSING')
        continue
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}'
    payload = {'contents':[{'parts':[{'text':'Salom. O‘zbek tilida qisqacha javob bering.'}]}]}
    try:
        r = requests.post(url, json=payload, timeout=20)
        print(f'{name}: status={r.status_code}')
        print(f'{name}: body={r.text[:250]}')
    except Exception as e:
        print(f'{name}: ERROR {type(e).__name__}: {str(e)[:250]}')

print('\n=== GROQ TEST ===')
key = os.getenv('GROQ_API_KEY')
if not key:
    print('GROQ_API_KEY: MISSING')
else:
    try:
        from groq import Groq
        client = Groq(api_key=key)
        resp = client.chat.completions.create(
            model='llama-3.1-70b-versatile',
            messages=[{'role': 'user', 'content': 'Salom. O‘zbek tilida qisqacha javob bering.'}],
            max_tokens=25,
            temperature=0.2,
        )
        text = resp.choices[0].message.content
        print('GROQ_API_KEY: OK')
        print(f'GROQ_API_KEY: reply={text[:200]}')
    except Exception as e:
        print(f'GROQ_API_KEY: ERROR {type(e).__name__}: {str(e)[:400]}')
