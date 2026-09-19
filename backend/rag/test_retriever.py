"""
Test for retriever: loads test_chunks.json and runs a sample query.
"""
from retriever import load_chunks_from_json, retrieve_context
import os


def run_test():
    path = os.path.join(os.path.dirname(__file__), 'test_chunks.json')
    if not os.path.exists(path):
        print('test_chunks.json not found. Run test_rag.py first.')
        return
    chunks = load_chunks_from_json(path)
    query = 'QQS stavkasi qancha?'
    results = retrieve_context(query, chunks, top_k=5)
    print('Top results:')
    for r in results:
        print(f"index={r['index']} score={r['score']:.3f} preview={r['chunk'][:180]!r}")


if __name__ == '__main__':
    run_test()
