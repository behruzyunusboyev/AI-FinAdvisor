# AI FinAdvisor — Loyiha qoidalari (Copilot uchun)

> Bu fayl `.github/copilot-instructions.md` nomi bilan repo ildizidagi `.github/` papkasiga qo'yiladi. GitHub Copilot (VS Code/JetBrains) buni avtomatik o'qib, kod takliflarini shu qoidalarga moslashtiradi.

## 1. Loyiha haqida

AI FinAdvisor — Oʻzbekistondagi KOB (kichik va oʻrta biznes) subyektlari uchun AI-asosidagi moliya, soliq va biznes-reja maslahatchisi. Hackathon: Umummilliy AI Xakaton, muammo №20.

**Asosiy funksiyalar:**
1. Generativ biznes-reja generatori (savol-javob → Executive Summary, SWOT, Marketing, Moliyaviy reja)
2. Aqlli kredit kalkulyatori (anuitet/differensial toʻlov + risk-analitika)
3. Soliq tizimi kalkulyatori (4% aylanma, QQS+Foyda solig'i, JSHOD/INPS)
4. PDF chiqarish (bankka topshirish uchun tayyor hujjat)

## 2. Tech stack (shundan chetga chiqmaslik)

- **Backend:** Python + FastAPI + Pydantic + Uvicorn
- **AI:** OpenAI `gpt-4o-mini` (asosiy) yoki Groq `llama-3.1-70b` (zaxira)
- **RAG:** ChromaDB + OpenAI embeddings (`text-embedding-3-small`)
- **PDF:** WeasyPrint (HTML/CSS → PDF)
- **DB:** SQLite (agar vaqt yetmasa) / PostgreSQL
- **Frontend:** React + Vite + TailwindCSS + React Router + React Hook Form + Axios
- Telegram bot — **YOʻQ**, faqat oddiy Web UI

## 3. Papka strukturasi

```
/backend
  /api          → FastAPI routerlar
  /core         → moliyaviy hisob-kitob funksiyalari (Modul 2)
  /rag          → ChromaDB, embedding, soliq bazasi (Modul 3)
  /pdf          → WeasyPrint shablonlari (Modul 4)
  /ai           → LLM prompt'lar, system prompt, chaqiruv logikasi (Modul 1)
  main.py
/frontend
  /src
    /components
    /pages
    /api        → backend bilan bog'lovchi funksiyalar (Axios)
```

**Muhim qoida:** har kim faqat OʻZ papkasida ishlaydi. Boshqa papkadagi faylga tegmaslik — konfliktni oldini oladi.

## 4. Kod yozish qoidalari

- O'zgaruvchi va funksiya nomlari — **inglizcha** (`calculate_loan_payment`, `taxRegime`), izohlar/comment — o'zbekcha yoki inglizcha, farqi yo'q
- Har bir funksiya kichik va bitta vazifani bajarishi kerak
- API endpoint nomlari: `/api/v1/loan/calculate`, `/api/v1/tax/estimate`, `/api/v1/business-plan/generate`, `/api/v1/pdf/export` kabi aniq va REST uslubida
- Har bir backend funksiya uchun Pydantic model bilan input/output aniq belgilangan bo'lishi kerak (Copilot shu asosda avtomatik to'g'ri kod taklif qiladi)
- Frontend'da har bir forma qadam (step) alohida komponent bo'lsin

## 5. Git ish qoidasi

- Hamma to'g'ridan-to'g'ri `main`ga push qiladi (branch shart emas)
- **Push qilishdan oldin doim `git pull origin main`**
- Kichik va tez-tez commit qiling (kuniga bir marta emas, har tugallangan funksiyadan keyin)
- Commit message: `[modul nomi] nima qilindi` — masalan `[pdf] shablon HTML tayyor`

## 6. QATʼIY QOIDALAR — Copilot oʻzbilarmonlik qilmasligi uchun

Bular **majburiy cheklovlar**. Copilot bu qoidalarni buzadigan taklif bersa — qabul qilmang, qo'lda tuzating.

1. **Faqat oʻz papkangizga tegishli fayllarni oʻzgartiring.** Boshqa modul papkasidagi (masalan `/rag`, `/pdf`) faylni Copilot "yaxshilash" uchun taklif qilsa ham — rad eting.
2. **Mavjud funksiya nomini, parametrlarini yoki qaytarish turini o'zgartirmang**, agar bu haqda leader bilan kelishmagan bo'lsangiz — chunki boshqa modul o'sha funksiyani chaqirayotgan bo'lishi mumkin.
3. **Yangi kutubxona/paket qo'shishdan oldin leaderga ayting.** Copilot ko'pincha "bu vazifa uchun X kutubxona bor" deb taklif qiladi — 2-bo'limdagi stackdan tashqari hech narsa avtomatik o'rnatilmasin.
4. **Copilot butun faylni qayta yozib tashlashini (full rewrite) qabul qilmang** — faqat kerakli qismni, kichik-kichik qilib qabul qiling. Katta avtomatik o'zgarishlar nazoratdan chiqishi oson.
5. **API endpoint nomi/yo'lini o'zingizcha o'zgartirmang** — 4-bo'limda kelishilgan nomlardan foydalaning, aks holda frontend/backend bir-birini topolmay qoladi.
6. **Raqamli hisob-kitob (kredit, soliq) kodini Copilot "soddalashtiraman" deb LLM chaqiruviga aylantirsa — rad eting.** Bu doim qattiq Python logikasi bo'lishi shart (5-bo'limga qarang).
7. **Har qanday katta o'zgarishdan (yangi fayl, yangi endpoint, struktura o'zgarishi) oldin — jamoa chatida bir og'iz yozib qo'ying.** Copilot buni bilmaydi, faqat odamlar bir-biriga aytishi kerak.
8. **Test qilinmagan kodni `main`ga push qilmang** — hech bo'lmasa o'zingiz ishga tushirib, xato chiqmasligini tekshiring.

## 7. AI/LLM ishlatish qoidasi

- System prompt har doim: "Siz Oʻzbekiston biznes va soliq muhitiga ixtisoslashgan moliyaviy maslahatchisiz" bilan boshlanadi
- Barcha AI javoblari o'zbek tilida (rus/ingliz — faqat qo'shimcha, asosiy emas)
- Raqamli hisob-kitoblarni (kredit, soliq) **hech qachon LLM'ga hisoblattirmaslik** — bu Python funksiyada (Modul 2) qattiq kod bilan bajariladi, LLM faqat tushuntirish/matn yozadi
