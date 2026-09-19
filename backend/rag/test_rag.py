"""
Simple test for the RAG ingest skeleton (no external deps).
"""
from ingest import chunk_text, write_chunks_to_json


def build_sample_corpus():
    sample = """
    QQS (Qabul qilinuvchi qiymat solig'i) stavkasi O'zbekistonda 12% ni tashkil etadi.
    Soliq kodeksining tegishli bo'limlari bo'yicha QQS hisoblashda mahsulotlar qiymati asos bo'lib xizmat qiladi.
    4% aylanma solig'i kichik va o'rta biznesga ma'lum imtiyozlar beradi.
    Foyda solig'i 15% bo'lib korxona foydasidan olinadi.
    JSHOD (jamoaviy sug'urta to'lovi) ish haqi hisobidan ajratiladi.
    Ijara to'lovi va kredit to'lovi biznes kassasini kamaytiradi.
    Kreditni olishda yilgi foiz stavkasi, muddat va to'lov sxemasi muhim omillardir.
    Oylik cash-flow hisobi kredit to'lovlari, soliqlar va ijara xarajatlarini hisobga olgan holda yuritiladi.
    Kichik biznesda qimmatli aktivlarni kengaytirishdan oldin ishlab chiqarish hajmi va foyda prognozi tekshirilishi kerak.
    """.strip()
    return sample


def run_test():
    sample = build_sample_corpus()
    chunks = chunk_text(sample, chunk_size=500, overlap=120)
    print('Produced chunks:', len(chunks))
    write_chunks_to_json(chunks, 'test_chunks.json')
    print('Wrote test_chunks.json')


if __name__ == '__main__':
    run_test()
