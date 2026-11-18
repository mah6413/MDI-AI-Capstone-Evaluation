"""Score recorded Phoenix-derived RAG answers without rerunning the RAG application.
Usage: py deepeval_scoring_capstone.py results/MDI_AI_DeepEval_Input.jsonl
Requires: pip install deepeval; OPENAI_API_KEY in environment (or local .env).
LLM-as-judge requests incur API charges. Output: *_judged.json
"""
import argparse
import json
from pathlib import Path


def load_rows(path):
    text = path.read_text(encoding='utf-8-sig')
    if path.suffix.lower() == '.jsonl':
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        rows = json.loads(text)
    if not isinstance(rows, list):
        raise ValueError('Expected a JSON array or JSONL records')
    return rows


def get_contexts(row):
    contexts = row.get('retrieval_context')
    if contexts is None:
        contexts = row.get('citations', [])
    if isinstance(contexts, str):
        contexts = [contexts]
    if not isinstance(contexts, list):
        return []
    return [str(c.get('excerpt') or c.get('text') or '') if isinstance(c, dict) else str(c)
            for c in contexts if c]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', type=Path)
    args = parser.parse_args()
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
    from deepeval.test_case import LLMTestCase
    rows = load_rows(args.dataset)
    for index, row in enumerate(rows, 1):
        question = row.get('input') or row.get('question') or ''
        answer = row.get('actual_output') or row.get('answer') or ''
        contexts = get_contexts(row)
        if not question or not answer or not contexts or row.get('fallback_used'):
            row['judge'] = {'skipped': 'Missing question, answer, context, or fallback'}
            continue
        test = LLMTestCase(input=question, actual_output=answer, retrieval_context=contexts)
        scores = {}
        for key, metric in [
            ('faithfulness', FaithfulnessMetric(include_reason=True)),
            ('answer_relevancy', AnswerRelevancyMetric(include_reason=True)),
        ]:
            try:
                metric.measure(test)
                scores[key] = {'score': metric.score, 'reason': metric.reason}
            except Exception as exc:
                scores[key] = {'error': str(exc)}
        row['judge'] = scores
        print(f'Scored {index}/{len(rows)}: {row.get("id", index)}', flush=True)
    output = args.dataset.with_name(args.dataset.stem + '_judged.json')
    output.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Saved {output}')


if __name__ == '__main__':
    main()
