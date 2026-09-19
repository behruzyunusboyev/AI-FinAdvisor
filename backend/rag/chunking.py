"""RAG manbalarini ChromaDB'ga yuklashdan oldin bo'laklash vositasi."""


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    """Matnni so'z chegarasini buzmasdan, qisman ustma-ust bo'laklarga ajratadi.

    Args:
        text: Bo'laklanadigan manba matni.
        chunk_size: Har bir bo'lakdagi maksimal belgi soni.
        overlap: Qo'shni bo'laklar o'rtasida saqlanadigan belgi soni.

    Returns:
        Bo'sh bo'lmagan, tartiblangan matn bo'laklari.

    Raises:
        ValueError: O'lchamlar mantiqan noto'g'ri bo'lsa.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size musbat bo'lishi kerak")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 0 dan kichik bo'lmasligi va chunk_size dan kichik bo'lishi kerak")

    normalized_text = " ".join(text.split())
    if not normalized_text:
        return []

    chunks: list[str] = []
    start = 0
    text_length = len(normalized_text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        if end < text_length:
            boundary = normalized_text.rfind(" ", start, end + 1)
            if boundary > start:
                end = boundary

        chunk = normalized_text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end == text_length:
            break

        next_start = end - overlap
        previous_space = normalized_text.rfind(" ", start, next_start + 1)
        if previous_space >= start:
            next_start = previous_space + 1
        else:
            next_space = normalized_text.find(" ", next_start, end)
            next_start = next_space + 1 if next_space != -1 else end

        start = max(next_start, start + 1)

    return chunks
