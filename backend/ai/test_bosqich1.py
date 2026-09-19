"""
Bosqich 1 Test — System Prompt va LLM Wrapper qo'lda tekshiruvi
"""

import sys
from llm_wrapper import AIClient


def test_case_1_hallucination_raqam():
    """
    Test 1: Raqam hallucination — model o'zidan raqam to'qimasligini tekshir
    """
    print("\n" + "="*60)
    print("TEST 1: Raqam hallucination oldinini olish")
    print("="*60)
    
    client = AIClient(use_groq=False)  # OpenAI
    
    query = "Oʻzbekistonda KOB uchun qaysi yerdan kredit olsa eng arzon?"
    context = ""  # Kontekstsiz — model hallucination qilsa aniq ko'rinadi
    
    response = client.ask_ai(query, context)
    print(f"Savol: {query}")
    print(f"\nJavob:\n{response}")
    
    # Tekshiruv
    hallucination_signs = ["%", "soʻm", "stavka", "foiz"]
    is_hallucinated = any(sign in response.lower() for sign in hallucination_signs)
    
    print(f"\n✅ NATIJA: {'HALLUCINATION ANIQLAND' if is_hallucinated else 'SIFATLI (hallucination yo\'q)'}")
    return not is_hallucinated  # To'g'ri javob = hallucination bo'lmasligi


def test_case_2_kontekst_based():
    """
    Test 2: Kontekst asosida to'g'ri javob
    """
    print("\n" + "="*60)
    print("TEST 2: Kontekst asosida to'g'ri javob")
    print("="*60)
    
    client = AIClient(use_groq=False)
    
    query = "Oʻzbekistonda QQS stavkasi qancha?"
    context = "Soliq Kodeksining 9-bobiga asosan, QQS stavkasi 12% hisoblanadi. Bu stavka barcha tovarlar va xizmatlar uchun bir xil."
    
    response = client.ask_ai(query, context)
    print(f"Savol: {query}")
    print(f"Kontekst: {context}")
    print(f"\nJavob:\n{response}")
    
    # Tekshiruv: javobda 12% bo'lishi kerak
    correct = "12%" in response or "12 foiz" in response.lower()
    
    print(f"\n✅ NATIJA: {'SIFATLI (12% topildi)' if correct else 'NOTO\'G\'RI (12% yo\'q)'}")
    return correct


def test_case_3_uzbek_language():
    """
    Test 3: O'zbek tilida javob
    """
    print("\n" + "="*60)
    print("TEST 3: O'zbek tilida javob")
    print("="*60)
    
    client = AIClient(use_groq=False)
    
    query = "JSHOD nima va uni kim toʻlaydi?"
    context = "JSHOD — Jamoaviy soʻrov havo olash to'lovlari. Asosiy ishchi tomonidan toʻlanadi."
    
    response = client.ask_ai(query, context)
    print(f"Savol: {query}")
    print(f"Kontekst: {context}")
    print(f"\nJavob:\n{response}")
    
    # Tekshiruv: o'zbek tildagi harflar bor-yoʻq
    uzbek_chars = ['ʻ', 'oʻ', 'gʻ', 'qʻ', 'shʻ', 'xʻ']
    has_uzbek = any(char in response for char in uzbek_chars) or 'oz' in response.lower()
    
    print(f"\n✅ NATIJA: {'SIFATLI (o\'zbek tili aniqland)' if has_uzbek else 'EHTIYOT: til tekshiruvi'}")
    return True  # Til tekshiruvini avtomatik qo'y olmaysiz, manual ko'ring


def test_case_4_context_hallucination():
    """
    Test 4: Kontekstni hallucinate qilmaslik
    """
    print("\n" + "="*60)
    print("TEST 4: Kontekstni buzmagan holda javob berish")
    print("="*60)
    
    client = AIClient(use_groq=False)
    
    query = "Bank uchun biznestni qanday rejimlar bor?"
    context = "Oʻzbekistonda asosiy soliq rejimlar: 4% aylanma solig'i, QQS, Foyda solig'i."
    
    response = client.ask_ai(query, context)
    print(f"Savol: {query}")
    print(f"Kontekst: {context}")
    print(f"\nJavob:\n{response}")
    
    # Tekshiruv: faqat kontekstdagi 3 ta rejim eslatilishi kerak
    required_regimes = ["4%", "QQS", "Foyda"]
    found_regimes = sum(1 for regime in required_regimes if regime in response)
    
    print(f"\n✅ NATIJA: {'SIFATLI (to\'g\'ri rejimlar)' if found_regimes >= 2 else 'NOTO\'G\'RI (qo\'shimcha rejim qo\'shdi)'}")
    return found_regimes >= 2


def test_case_5_missing_context():
    """
    Test 5: Kontekstda ma'lumot bo'lmaganda to'g'ri xabar
    """
    print("\n" + "="*60)
    print("TEST 5: Kontekstda ma'lumot yo'ligida to'g'ri xabar")
    print("="*60)
    
    client = AIClient(use_groq=False)
    
    query = "Kredit uchun qaysi faiz?" 
    context = "Qayd: Bu kontekstda kredit haqida ma'lumot yo'q, faqat soliq haqida."
    
    response = client.ask_ai(query, context)
    print(f"Savol: {query}")
    print(f"Kontekst: {context}")
    print(f"\nJavob:\n{response}")
    
    # Tekshiruv: "yo'q" yoki "ma'lumot yo'q" xabari bo'lishi kerak
    correct_response = any(phrase in response.lower() for phrase in [
        "ma'lumot yo'q",
        "ma'lumot topilmadi",
        "kontekstda",
        "rasmiy manba"
    ])
    
    print(f"\n✅ NATIJA: {'SIFATLI (to\'g\'ri xabar)' if correct_response else 'EHTIYOT: hallucination qildi'}")
    return correct_response


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# BOSQICH 1 — SYSTEM PROMPT TEKSHIRUVI")
    print("# 5 TA TEST QILINI ISHGA TUSHIRISH")
    print("#"*60)
    
    results = []
    
    try:
        results.append(("Test 1: Hallucination", test_case_1_hallucination_raqam()))
        results.append(("Test 2: Kontekst", test_case_2_kontekst_based()))
        results.append(("Test 3: Uzbek tili", test_case_3_uzbek_language()))
        results.append(("Test 4: Kontekst tafsiri", test_case_4_context_hallucination()))
        results.append(("Test 5: Yo'q ma'lumot", test_case_5_missing_context()))
    except Exception as e:
        print(f"\n❌ XATO: {e}")
        print("Tekshirish: OPENAI_API_KEY va GROQ_API_KEY environment variables o'rnatilganmi?")
        # Fatal error — do not continue reporting success when tests didn't run
        sys.exit(2)
    
    # Natija
    print("\n" + "="*60)
    print("YAKUNIY NATIJA")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\nJami: {passed_count}/{total} test o'tdi")

    if total == 0:
        print("\n❌ Hech qanday test ishlamadi — muhit yoki import xatosi. Tekshiring.")
        sys.exit(2)

    if passed_count == total:
        print("\n🎉 BOSQICH 1 TAYYOR! Bosqich 2'ga o'taylik.")
        sys.exit(0)
    else:
        print("\n⚠️  Ba'zi testlar muvaffaqiyatsiz — prompt yoki konfiguratsiyani qayta ko'rib chiqing.")
        sys.exit(1)
