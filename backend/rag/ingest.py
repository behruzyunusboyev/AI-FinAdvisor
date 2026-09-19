"""
RAG ingestion skeleton.
- load_texts_from_dir(dir) -> list[(path, text)]
- chunk_text(text, chunk_size=1000, overlap=200) -> list[str]
- write_chunks_to_json(chunks, out_path)

NOTE: This is a portable skeleton. Do NOT auto-install or import ChromaDB here
unless you want native builds; leave actual vector DB ingestion to a later step
after confirming environment readiness.
"""
from typing import List, Tuple
import os
import json


def load_texts_from_dir(dir_path: str) -> List[Tuple[str, str]]:
    """Load .txt files from directory and return list of (filename, text)."""
    items = []
    for root, _, files in os.walk(dir_path):
        for fn in files:
            if fn.lower().endswith('.txt'):
                path = os.path.join(root, fn)
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                items.append((path, text))
    return items


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Simple sliding-window text chunker by characters.
    Returns list of chunks.
    """
    if chunk_size <= 0:
        raise ValueError('chunk_size must be > 0')
    if overlap >= chunk_size:
        raise ValueError('overlap must be smaller than chunk_size')

    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == text_len:
            break
        start = end - overlap
    return chunks


def write_chunks_to_json(chunks: List[str], out_path: str):
    payload = {
        'chunks_count': len(chunks),
        'chunks': chunks
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # Quick local smoke test if run directly
    sample = 'Bu test matni. ' * 200
    cs = chunk_text(sample, chunk_size=1000, overlap=200)
    print('Chunks produced:', len(cs))
    write_chunks_to_json(cs, 'sample_chunks.json')
    print('Wrote sample_chunks.json')
