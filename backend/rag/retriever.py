"""
Simple retrieval module for RAG using keyword overlap scoring.
Functions:
- load_chunks_from_json(path) -> List[str]
- retrieve_context(query, chunks, top_k=5) -> List[dict]

This is intentionally lightweight and dependency-free as a first pass.
"""
from typing import List, Dict
import json
import re

try:
    from .embeddings_fallback import get_embeddings, similarity
except Exception:
    from embeddings_fallback import get_embeddings, similarity

STOP_WORDS = {
    'bu', 'uchun', 'bilan', 'ham', 'yoki', 'va', 'qanday', 'qancha', 'qaysi', 'bo', 'chiq',
    'uch', 'juda', 'har', 'hisob', 'barcha', 'haqida', 'boz', 'siz', 'biz', 'u', 'bu', 'men', 'sen',
    'qachon', 'nima', 'ozi', 'yilda', 'keyingi', 'oyda', 'oy', 'uchun', 'bunda', 'boshqa', 'oldin'
}


def load_chunks_from_json(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('chunks', [])


def _normalize_word(word: str) -> str:
    word = word.lower().strip()
    word = word.replace('’', "'")
    return re.sub(r"[^a-z0-9%]+", '', word)


def _tokenize(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r"\b[\w%']+\b", text)
    tokens = [_normalize_word(t) for t in tokens]
    return [t for t in tokens if t and len(t) > 1 and t not in STOP_WORDS]


def _query_terms(query: str) -> List[str]:
    return _tokenize(query)


def retrieve_context(query: str, chunks: List[str], top_k: int = 5) -> List[Dict]:
    """
    Return top_k chunks most relevant to query using boosted word-overlap score.
    Each result is dict: { 'chunk': str, 'score': float, 'index': int }
    """
    if not query or not chunks:
        return []

    q_tokens = _query_terms(query)
    if not q_tokens:
        return []

    q_set = set(q_tokens)
    scored = []
    q_text = query.lower().replace('?', '').strip()

    for i, chunk in enumerate(chunks):
        c_tokens = _tokenize(chunk)
        if not c_tokens:
            continue

        c_text = chunk.lower()
        c_set = set(c_tokens)
        inter = q_set.intersection(c_set)

        # boost common domain terms and exact phrase matches
        phrase_bonus = 0.0
        if 'qqs' in q_text and 'qqs' in c_text:
            phrase_bonus += 1.5
        if 'soliq' in q_text and 'soliq' in c_text:
            phrase_bonus += 1.0
        if 'stavka' in q_text and 'stavka' in c_text:
            phrase_bonus += 1.25
        if 'foiz' in q_text and 'foiz' in c_text:
            phrase_bonus += 1.25
        if 'jshod' in q_text and 'jshod' in c_text:
            phrase_bonus += 1.25

        exact_overlap = sum(1 for w in q_tokens if w in c_set)
        overlap_score = len(inter) / max(1, len(q_set))
        term_score = exact_overlap / max(1, len(q_tokens))
        score = overlap_score * 2.0 + term_score * 1.5 + phrase_bonus

        # If a very short query has no word overlap but starts with a key term, still return best effort.
        if score > 0:
            scored.append({'chunk': chunk, 'score': score, 'index': i})

    if not scored:
        # Best-effort fallback: return first few chunks sorted by overlap on the longest query token.
        for i, chunk in enumerate(chunks[:min(top_k, len(chunks))]):
            scored.append({'chunk': chunk, 'score': 0.01, 'index': i})

    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:top_k]


def retrieve_context_with_embeddings(query: str, chunks: List[str], top_k: int = 5) -> List[Dict]:
    """
    Retrieve using embeddings (OpenAI if available, otherwise TF fallback).
    Returns list of dicts: {'chunk': str, 'score': float, 'index': int}
    """
    if not query or not chunks:
        return []

    texts = [query] + chunks
    embs = get_embeddings(texts)
    if not embs or len(embs) < 2:
        return retrieve_context(query, chunks, top_k=top_k)

    q_emb = embs[0]
    chunk_embs = embs[1:]
    scored = []
    for i, ce in enumerate(chunk_embs):
        try:
            sc = similarity(q_emb, ce)
        except Exception:
            sc = 0.0
        if sc > 0:
            scored.append({'chunk': chunks[i], 'score': sc, 'index': i})

    if not scored:
        return retrieve_context(query, chunks, top_k=top_k)

    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:top_k]


if __name__ == '__main__':
    # smoke test using test_chunks.json
    import os
    path = os.path.join(os.path.dirname(__file__), 'test_chunks.json')
    if os.path.exists(path):
        chunks = load_chunks_from_json(path)
        results = retrieve_context('QQS stavkasi qancha', chunks, top_k=3)
        for r in results:
            print('Score:', r['score'])
            print(r['chunk'][:200])
            print('---')
    else:
        print('No test_chunks.json found; run test_rag.py first.')
