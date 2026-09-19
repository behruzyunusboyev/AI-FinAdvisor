"""
Compare OpenAI `gpt-4o-mini` vs Groq `llama-3.1-70b` responses for same prompt.
Usage:
  - If `OPENAI_API_KEY` and/or `GROQ_API_KEY` are set, real calls will be attempted.
  - If neither key is set, script runs in MOCK mode and prints example outputs.

Run:
  cd backend/ai
  python compare_llms.py
"""
import os
from llm_wrapper import AIClient

PROMPT = "Qo'shimcha kontekst: Hech qanday moliyaviy raqam to'ldirmang. \n\nSavol: KOB uchun soliq rejimini qanday tanlash kerak? 3-4 qadamda tushuntiring (o'zbekcha)."


def run_compare():
    openai_key = os.getenv("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    results = {}

    if not openai_key and not groq_key:
        print("API keys topilmadi — MOCK rejimda ishlayapti. Haqiqiy test uchun OPENAI_API_KEY yoki GROQ_API_KEY ni `.env` ga qo'shing.")
        results['openai'] = "(MOCK) 1) Loyihaning hajmini baholang; 2) Soliq rejimini tanlang; 3) Hisob-kitoblarni Modul 2 ga yuboring."
        results['groq'] = "(MOCK) 1) Aktiv daromadni baholang; 2) Soliq rejimini tekshiring; 3) Moliyaviy raqamlar backendda hisoblanadi."
        print("\n--- MOСK OpenAI ---\n", results['openai'])
        print("\n--- MOCK Groq ---\n", results['groq'])
        return results

    if openai_key:
        print("So'rov: OpenAI (gpt-4o-mini) ga yuborilmoqda...")
        client_o = AIClient(use_groq=False)
        try:
            resp_o = client_o.ask_ai(PROMPT, context="")
            results['openai'] = resp_o
            print("\n--- OpenAI javobi ---\n", resp_o)
        except Exception as e:
            results['openai'] = f"ERROR: {e}"
            print("OpenAI xato:", e)

    if groq_key:
        print("So'rov: Groq (llama-3.1-70b) ga yuborilmoqda...")
        client_g = AIClient(use_groq=True)
        try:
            resp_g = client_g.ask_ai(PROMPT, context="")
            results['groq'] = resp_g
            print("\n--- Groq javobi ---\n", resp_g)
        except Exception as e:
            results['groq'] = f"ERROR: {e}"
            print("Groq xato:", e)

    return results


if __name__ == "__main__":
    run_compare()
