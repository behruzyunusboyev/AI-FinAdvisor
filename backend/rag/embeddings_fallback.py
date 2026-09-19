from typing import List
import os
import math
import re
from collections import Counter


def _tokenize(text: str) -> List[str]:
    text = text.lower()
    return re.findall(r"\b[\w']+\b", text)


def _cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Return vector embeddings for a list of texts.

    Preferred: use OpenAI embeddings when `OPENAI_API_KEY` present.
    Fallback: simple TF (term-frequency) vector over token vocabulary.
    """
    if not texts:
        return []

    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
            # resp.data is list of {'embedding': [...]} or client-specific object
            embeddings = []
            for item in getattr(resp, 'data', resp.get('data') if isinstance(resp, dict) else []):
                emb = item.get('embedding') if isinstance(item, dict) else getattr(item, 'embedding', None)
                embeddings.append(emb)
            if embeddings and len(embeddings) == len(texts):
                return embeddings
        except Exception:
            # fall back to local method
            pass

    # Local TF fallback
    token_lists = [_tokenize(t) for t in texts]
    vocab = []
    vocab_set = set()
    for toks in token_lists:
        for t in toks:
            if t not in vocab_set:
                vocab_set.add(t)
                vocab.append(t)

    vecs = []
    for toks in token_lists:
        cnt = Counter(toks)
        vec = [float(cnt.get(v, 0)) for v in vocab]
        # normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        vecs.append(vec)

    return vecs


def similarity(a: List[float], b: List[float]) -> float:
    return _cosine(a, b)
