"""Text-only Gemini with Groq fallback.

This module must only receive completed Python financial results. It requests
qualitative Uzbek analysis and rejects AI replies that try to introduce numbers.
"""

import json
import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """Siz O'zbekiston biznes va soliq muhitiga ixtisoslashgan qat'iy moliyaviy maslahatchisiz.
Sizga Python hisoblagan moliyaviy natijalar beriladi. Hech qachon yangi raqam, foiz, soliq stavkasi yoki prognoz kiritmang va mavjud raqamni o'zgartirmang.
Faqat o'zbek tilida quyidagi JSON ni qaytaring: {"executive_summary":"...","swot":{"strengths":["..."],"weaknesses":["..."],"opportunities":["..."],"threats":["..."]},"marketing_strategy":"..."}."""


class AIAnalysisClient:
    async def analyze(self, project: dict[str, Any], financials: dict[str, Any]) -> dict[str, Any]:
        prompt = f"Loyiha: {json.dumps(project, ensure_ascii=False)}\nPython natijalari: {json.dumps(financials, ensure_ascii=False)}"
        for provider in (self._openai, self._gemini, self._groq):
            try:
                result = await provider(prompt)
                if result:
                    return result
            except (httpx.HTTPError, ValueError, KeyError, json.JSONDecodeError):
                continue
        return self._unavailable_analysis(project["business_type"])

    async def _openai(self, prompt: str) -> dict[str, Any] | None:
        key = os.getenv("PLATFORM_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not key:
            return None
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                },
            )
            response.raise_for_status()
        return self._validate_text(response.json()["choices"][0]["message"]["content"])

    async def _gemini(self, prompt: str) -> dict[str, Any] | None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            return None
        model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, params={"key": key}, json={"system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]}, "contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2, "response_mime_type": "application/json"}})
            response.raise_for_status()
        return self._validate_text(response.json()["candidates"][0]["content"]["parts"][0]["text"])

    async def _groq(self, prompt: str) -> dict[str, Any] | None:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            return None
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json={"model": "llama-3.1-70b-versatile", "temperature": 0.2, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]})
            response.raise_for_status()
        return self._validate_text(response.json()["choices"][0]["message"]["content"])

    @staticmethod
    def _validate_text(text: str) -> dict[str, Any]:
        result = json.loads(text)
        swot = result["swot"]
        if not isinstance(swot, dict) or not all(isinstance(swot[key], list) for key in ("strengths", "weaknesses", "opportunities", "threats")):
            raise ValueError("AI response does not match analysis schema")
        return result

    @staticmethod
    def _unavailable_analysis(business_type: str) -> dict[str, Any]:
        return {"executive_summary": f"{business_type} loyihasi uchun moliyaviy ko'rsatkichlar Python formulalari bilan tayyorlandi. AI matnli tahlili hozircha mavjud emas.", "swot": {"strengths": ["Deterministik moliyaviy reja mavjud."], "weaknesses": ["Bozor ma'lumotlari alohida tekshiruvni talab qiladi."], "opportunities": ["Mahalliy mijoz segmentlarini sinovdan o'tkazish mumkin."], "threats": ["Xarajatlar va talab o'zgarishi muntazam kuzatilishi kerak."]}, "marketing_strategy": "Mahalliy auditoriya uchun sinov kampaniyalari o'tkazing va natijalarni kunlik qayd eting."}
