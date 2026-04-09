from ai_models import LegalAIProcessor
import json

with open('sample_documents/employment_contract.txt', 'r') as f:
    text = f.read()

processor = LegalAIProcessor()
clauses = processor.extract_clauses(text)

print('Direct AI processor test - clauses found:', len(clauses))
for i, clause in enumerate(clauses[:5]):
    print(f'{i+1}: {clause["clause_text"][:50]}...')
