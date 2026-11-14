"""Reproducible QA and citation evaluation against an annotated JSONL dataset.

Run: python evaluation.py --dataset eval_cases.jsonl --output results.json
Each record: {"id": "Q01", "question": "...", "documents": ["tests/doc.txt"],
              "reference_answer": "...", "supporting_chunk_ids": ["doc_1_chunk_1"]}
Document paths are relative to dataset location. Use synthetic data only.
"""
import argparse
import json
import os
import re
import time
from pathlib import Path

from observability import initialize_observability
initialize_observability()
from hybrid_rag_pipeline import run_nonprofit_assistant

CITATION_PATTERN = re.compile(r'\[(C\d+)\](?:\([^)]*\))?')


def extract_cited_ids(answer):
    return sorted(set(CITATION_PATTERN.findall(answer)))


def evaluate_case(case, root, configuration):
    paths = [str((root / p).resolve()) for p in case['documents']]
    started = time.perf_counter()
    result = run_nonprofit_assistant(
        user_query=case['question'], uploaded_file_paths=paths,
        mode='qa', api_key=os.environ.get('OPENAI_API_KEY'),
        semantic_weight=configuration['semantic_weight'],
        keyword_weight=configuration['keyword_weight'],
    )
    elapsed = time.perf_counter() - started
    citation_map = {c['id']: c for c in result.get('citations', [])}
    cited = extract_cited_ids(result['answer'])
    valid = [cid for cid in cited if cid in citation_map]
    gold = set(case.get('supporting_chunk_ids', []))
    retrieved = {c['chunk_id'] for c in citation_map.values()}
    cited_chunks = {citation_map[cid]['chunk_id'] for cid in valid}
    return {
        'id': case['id'], 'configuration': configuration['name'],
        'question': case['question'], 'answer': result['answer'],
        'reference_answer': case.get('reference_answer', ''),
        'latency_seconds': round(elapsed, 3),
        'citation_tokens': cited, 'valid_citation_tokens': valid,
        'citation_id_validity': len(valid)/len(cited) if cited else None,
        'retrieval_recall_at_k': len(retrieved & gold)/len(gold) if gold else None,
        'citation_source_precision': len(cited_chunks & gold)/len(cited_chunks) if cited_chunks and gold else None,
        'retrieved_chunk_ids': sorted(retrieved), 'cited_chunk_ids': sorted(cited_chunks),
        'ground_truth_chunk_ids': sorted(gold),
        'citations': result.get('citations', []),
        'fallback_used': result.get('fallback_used', False),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--output', default='evaluation_results.json')
    args = parser.parse_args()
    dataset = Path(args.dataset).resolve()
    cases = [json.loads(line) for line in dataset.read_text(encoding='utf-8').splitlines() if line.strip()]
    configurations = [
        {'name': 'baseline', 'semantic_weight': .68, 'keyword_weight': .32},
        {'name': 'keyword_emphasis', 'semantic_weight': .45, 'keyword_weight': .55},
    ]
    results = []
    for config in configurations:
        for case in cases:
            results.append(evaluate_case(case, dataset.parent, config))
            print(f"{config['name']} {case['id']}: done")
    Path(args.output).write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f'Wrote {len(results)} case results to {args.output}')

if __name__ == '__main__':
    main()
