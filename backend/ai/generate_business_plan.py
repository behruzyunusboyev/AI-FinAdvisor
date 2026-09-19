"""
Generate business plan by combining user input + RAG context and calling LLM.
Outputs a JSON object matching API contract:
{
  "executive_summary": str,
  "swot": {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []},
  "marketing": str,
  "financial_plan": str,  # NOTE: no numeric calculations, only descriptions
  "notes": str
}

The LLM is instructed to ONLY return valid JSON with these keys.
If no API key is set, returns a mock response for local testing.
"""
import os
import json
from typing import Dict, List
try:
    from .system_prompt import get_system_prompt, prepend_context_to_prompt
    from .llm_wrapper import AIClient
except Exception:
    # Allow running as a script where package-relative imports may fail
    from system_prompt import get_system_prompt, prepend_context_to_prompt
    from llm_wrapper import AIClient


API_CONTRACT_KEYS = [
    "executive_summary",
    "swot",
    "marketing",
    "financial_plan",
    "notes",
]


def _build_prompt(user_input: Dict, rag_context: List[str]) -> str:
    """Construct the prompt to send to the LLM.

    The prompt asks the model to return JSON with the exact contract keys and to
    NOT invent or compute numeric financials.
    """
    project_title = user_input.get('project_title', "Noma'lus loyiha")
    audience = user_input.get('audience', 'bank')
    short_desc = user_input.get('description', '')

    context_text = "\n\n--- RAG CONTEXT ---\n"
    context_text += "\n\n".join(rag_context) if rag_context else "(Kontekst mavjud emas)"

    # Describe the JSON contract and constraints
    instruction = (
        "Sizga quyidagi struktura bo'yicha faqat JSON shaklida javob qaytarish so'raladi."
        " Javobdagi barcha moliyaviy raqamlar yoki foizlarni hisoblamang yoki yaratmang;"
        " agar raqam kerak bo'lsa, uni 'TO_BE_FILLED_BY_FINANCIAL_MODULE' deb belgilang."
        " JSON faqat quyidagi kalitlarni o'z ichiga olsin:"
    )

    keys_description = json.dumps({
        'executive_summary': 'short paragraph describing the project and purpose',
        'swot': {'strengths': ['...'], 'weaknesses': ['...'], 'opportunities': ['...'], 'threats': ['...']},
        'marketing': 'marketing strategy and channels',
        'financial_plan': 'description of financial approach — DO NOT compute numbers',
        'notes': 'any additional notes or required actions'
    }, ensure_ascii=False, indent=2)

    prompt = (
        f"PROJECT_TITLE: {project_title}\n"
        f"AUDIENCE: {audience}\n"
        f"DESCRIPTION: {short_desc}\n\n"
        f"{instruction}\n{keys_description}\n\n"
        f"Kontekst: {context_text}\n\n"
        "Iltimos, faqat JSON formatida, hech qanday qo'shimcha matn yoki tushuntirishlarsiz javob bering."
    )

    return prompt


def generate_business_plan(user_input: Dict, rag_context: List[str]) -> Dict:
    """Generate the business plan using LLM or return mock response when API keys missing."""
    openai_key = os.getenv('OPENAI_API_KEY')
    groq_key = os.getenv('GROQ_API_KEY')

    prompt = _build_prompt(user_input, rag_context)

    # If no LLM keys available, return mock
    if not openai_key and not groq_key:
        mock = {
            "executive_summary": f"{user_input.get('project_title','Loyiha')} uchun qisqacha executive summary.",
            "swot": {
                "strengths": ["Mahsulot bozorda noyob", "Past kirish xarajatlari"],
                "weaknesses": ["Cheklangan tajriba", "Kichik marketing byudjeti"],
                "opportunities": ["Raqamli sotuv kanallari", "Mahalliy bozor kengayishi"],
                "threats": ["Raqobatchilar", "Qonunchilik o'zgarishi"]
            },
            "marketing": "Oson tushuniladigan marketing strategiyasi: onlayn reklama, mahalliy hamkorliklar, chegirmalar.",
            "financial_plan": "Moliyaviy reja — raqamlar Modul 2 orqali to`ldiriladi. TO_BE_FILLED_BY_FINANCIAL_MODULE",
            "notes": "Keyingi qadam: Modul 2 dan numerik ma'lumotlarni oling va PDF uchun formatlang."
        }
        return mock

    # Prefer OpenAI by default
    client = AIClient(use_groq=False) if openai_key else AIClient(use_groq=True)

    resp_text = client.ask_ai(prompt, context='')

    # Try to parse JSON from response
    try:
        parsed = json.loads(resp_text)
    except Exception:
        # If parsing fails, wrap the raw text
        return {'error': 'LLM returned non-JSON response', 'raw': resp_text}

    # Validate keys
    for key in API_CONTRACT_KEYS:
        if key not in parsed:
            parsed[key] = None
    return parsed


if __name__ == '__main__':
    # Quick mock run
    ui = {'project_title': "Qishloq savdo do'koni", 'description': 'Mahalliy mahsulotlarni sotish', 'audience': 'bank'}
    rag = ['QQS stavkasi 12% ekanligi haqida maʼlumot.', '4% aylanma rejimi haqida yozuv.']
    out = generate_business_plan(ui, rag)
    print(json.dumps(out, ensure_ascii=False, indent=2))
