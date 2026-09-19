from retriever import load_chunks_from_json
from embeddings_fallback import get_embeddings, _tokenize, similarity

chunks = load_chunks_from_json('test_chunks.json')
print('Chunks count', len(chunks))
q='QQS stavkasi qancha'
import re
print('Query tokens:', re.findall(r"\b[\w']+\b", q.lower()))
print('First chunk sample:', chunks[0][:300])
print('First chunk tokens:', re.findall(r"\b[\w']+\b", chunks[0].lower())[:50])
embs = get_embeddings([q, chunks[0]])
print('Emb len', len(embs))
print('Emb 0 len', len(embs[0]))
print('Emb 1 len', len(embs[1]))
print('Similarity', similarity(embs[0], embs[1]))
