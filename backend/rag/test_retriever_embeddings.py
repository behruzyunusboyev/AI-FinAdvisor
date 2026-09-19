from retriever import load_chunks_from_json, retrieve_context_with_embeddings
import os

print('\nRunning embedding-based retriever smoke test...')
path = os.path.join(os.path.dirname(__file__), 'test_chunks.json')
if not os.path.exists(path):
    print('No test_chunks.json — run test_rag.py first to create chunks.')
    raise SystemExit(0)

chunks = load_chunks_from_json(path)
res = retrieve_context_with_embeddings('QQS stavkasi qancha', chunks, top_k=3)
print('Results:')
for r in res:
    print(r['score'])
    print(r['chunk'][:200])
    print('---')
