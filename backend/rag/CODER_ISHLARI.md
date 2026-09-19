# Coder ishlari — Modul 3 (RAG)

Bu fayl RAG bo'yicha bajarilgan ishlar va siz bajarishingiz kerak bo'lgan keyingi
amallarni qayd etadi. Har bir qadam sifat tekshiruvisiz keyingisiga o'tmaydi.

## Bajarilgan

- [x] Rasmiy Markaziy bank manbasi tanlandi va manba metama'lumotlari bilan
  `sources/central_bank_policy_rate_2026-07-29.md` fayliga kiritildi.
- [x] `chunk_text()` yozildi; qisqa, uzun va qator oralig'i bo'lgan 3 xil
  inputda tekshirildi. So'zlar bo'linmasligi tasdiqlandi.
- [x] `index_documents()` yozildi; bo'sh input, API kaliti yo'qligi va manba
  metama'lumoti yo'qligi holatlari tekshirildi.

## Hozirgi qadam — ChromaDB'ga real yuklash

### Siz qilishingiz kerak

1. `backend/.env` faylini yarating. Uni Gitga qo'shmang.
2. Quyidagilarni haqiqiy kalitlar bilan to'ldiring:

   ```env
   OPENAI_API_KEY=...
   GROQ_API_KEY=...
   ```

3. Kalit qo'yilganini xabar qiling. Kalitning o'zini chatga yubormang.

## Bosqich 2 jonli test holati

- [x] Groq wrapperi rasmiy Markaziy bank konteksti bilan jonli so'rovga qadar
  yetib bordi.
- [ ] Groq API `401 invalid_api_key` qaytardi. `GROQ_API_KEY` qiymatini Groq
  konsolidan qayta yarating yoki xatosiz nusxalang, keyin `.env` faylida
  almashtiring. Kalitni chatga yubormang.
- [ ] `GROQ_API_KEY` tuzatilgach, bir xil savol bilan Groq va (bo'lsa) OpenAI
  javoblari o'zbekcha sifati bo'yicha solishtiriladi.

## Muhit eslatmasi

- [x] `groq` va `python-dotenv` o'rnatildi.
- [x] Groq 0.4.1 uchun test muhitida mos `httpx<0.28` o'rnatildi.
- [ ] `requirements.txt`ga versiya qotirish kiritilmadi: u `/ai` va `/rag`
  doirasidan tashqarida hamda leader bilan kelishishni talab qiladi.

## Gemini tekshiruvi — 2026-09-18

- [x] Gemini API kaliti va `gemini-3.6-flash` modeliga ulanish tekshirildi.
- [x] Aniq kontekst savolida 14 foiz to'g'ri qaytdi.
- [x] Kontekstda ma'lumot yo'q holatida to'g'ri rad javobi qaytdi.
- [ ] Prompt-injection holatida model barqaror, mazmunli rad javobini bermadi;
  faqat yo'riqnoma parchasi qaytdi. Shu sabab Gemini hozircha wrapperga
  qo'shilmaydi va OpenAI o'rnini bosa olmaydi.
- [ ] RAG embeddinglari uchun OpenAI `text-embedding-3-small` talab qilinadi.
  OpenAI API kaliti olinib, `.env`dagi `OPENAI_API_KEY`ga qo'yilishi kerak.

## OpenAI tekshiruvi — 2026-09-18

- [x] `OPENAI_API_KEY` format jihatidan qabul qilindi va `gpt-4o-mini` so'rovi
  OpenAI API'ga yetib bordi.
- [ ] API `429 credit_balance_exhausted` qaytardi. OpenAI Platform billing
  sahifasiga kredit qo'shilmaguncha chat va `text-embedding-3-small` ishlamaydi.

## Bosqich 1 — prompt-injection kuchaytirishi

- [x] System promptga ichki qoidalarni oshkor qilmaslik bandi qo'shildi.
- [x] Foydalanuvchi savoli `<user_input>` teglariga ajratildi va bu teg ichidagi
  matn buyruq emasligi aniq belgilandi.
- [x] 8 xil injection formulasi bilan lokal strukturaviy test o'tdi.
- [ ] 8 ta jonli LLM testi hali o'tkazilmadi: to'liq ichki system promptni
  tashqi Gemini xizmatiga yuborish uchun foydalanuvchining aniq ruxsati kerak.

### Jonli Gemini injection testi — 2026-09-18

- [x] Foydalanuvchi ruxsati bilan 8 ta jonli test boshlandi.
- [x] 1, 2 va 5-holatlarda Gemini `Men bunga yordam bera olmayman.` deb to'g'ri
  rad etdi.
- [ ] 3-holatda belgilangan rad javobi to'liq qaytmadi.
- [ ] 4, 6, 7 va 8-holatlarda Gemini `429` rate limit qaytardi.
- [ ] 8/8 sifat tekshiruvi o'tmagani uchun Gemini `llm_wrapper.py`ga asosiy
  provayder sifatida almashtirilmadi.

### Coder qiladigan ish

- [ ] Rasmiy manbaning chunklarini `text-embedding-3-small` bilan ChromaDB'ga
  yuklash.
- [ ] ChromaDB'dagi yozuv soni va manba URL metama'lumotini tekshirish.
- [ ] Soliq Kodeksining amaldagi matnidan faqat manba bilan qo'lda tasdiqlangan
  bo'laklarni qo'shish. Tekshirilmagan soliq stavkasi yuklanmaydi.

## Keyingi bosqichga o'tish sharti

ChromaDB'da saqlangan har bir raqam yoki stavka asl rasmiy manba bilan
solishtirilgandan keyingina retrieval funksiyasi (Bosqich 4) boshlanadi.
