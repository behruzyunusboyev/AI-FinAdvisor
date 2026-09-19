"""
Test both Gemini keys (GEMINI_KEY_1 and GEMINI_KEY_2) and print concise results.
Usage: set env vars GEMINI_KEY_1 and GEMINI_KEY_2, then run:
    python test_gemini_keys.py
"""
import os
from gemini_wrapper import test_key


def run_tests():
    # Read the keys that are present in .env: GEMINI_API_KEY and GEMINI_API_KEY2
    keys = [
        ("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY")),
        ("GEMINI_API_KEY2", os.getenv("GEMINI_API_KEY2"))
    ]

    prompt = "Salom. Iltimos qisqacha: qanday qilib kichik biznes uchun soliq rejimini tanlash kerak? (O'zbekcha)"

    results = []
    for name, key in keys:
        print(f"\n--- Testing {name} ---")
        if not key:
            print(f"{name} not set in environment.")
            results.append((name, False, {"error": "not set"}))
            continue

        success, resp = test_key(key, prompt=prompt)
        print(f"Success: {success}")
        # Print brief safe preview
        if isinstance(resp, dict) and resp:
            preview = str(resp)[:800]
        else:
            preview = str(resp)
        print(preview)
        results.append((name, success, resp))

    # Summary
    print("\n=== Summary ===")
    for name, success, _ in results:
        print(f"{name}: {'OK' if success else 'FAIL'}")

    return results


if __name__ == "__main__":
    run_tests()
