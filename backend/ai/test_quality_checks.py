"""
Run quality checks (Bosqich 6) and print concise report.
"""
from qa_quality_checks import run_adversarial_prompts
import json


def main():
    report = run_adversarial_prompts()
    for item in report:
        print(f"\n--- Case {item['case']} ---")
        if item['schema_issues']:
            print("Schema issues:")
            for s in item['schema_issues']:
                print(' -', s)
        else:
            print('Schema: OK')
        if item['hallucinations']:
            print('Hallucinations found:')
            for h in item['hallucinations']:
                print(' -', h)
        else:
            print('Hallucination check: OK')
        if item['language_issues']:
            print('Language issues:')
            for l in item['language_issues']:
                print(' -', l)
        else:
            print('Language: OK')

if __name__ == '__main__':
    main()
