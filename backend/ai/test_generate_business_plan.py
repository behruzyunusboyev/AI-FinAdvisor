"""
Test for generate_business_plan (mock mode if no API keys present).
"""
from generate_business_plan import generate_business_plan
import json


def run_test():
    ui = {
        'project_title': "Mahalliy oshxona",
        'description': "Oddiy kundalik taomlar ishlab chiqarish",
        'audience': 'bank'
    }
    rag = [
        'Soliq Kodeksi: QQS 12% haqida yozuv.',
        'Soliq maʼlumotlari: 4% aylanma rejimi.'
    ]
    res = generate_business_plan(ui, rag)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    run_test()
