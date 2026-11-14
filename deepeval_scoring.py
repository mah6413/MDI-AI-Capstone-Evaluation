"""Optional LLM-as-judge evaluation of recorded results. May incur API charges.

Usage: python deepeval_scoring.py evaluation_results.json
"""
import json
import sys
from pathlib import Path


def main():
    from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
    from deepeval.test_case import LLMTestCase
    source = Path(sys.argv[1])
    rows = json.loads(source.read_text(encoding='utf-8'))
    for row in rows:
        contexts = [c['excerpt'] for c in row['citations']]
        if not contexts or row['fallback_used']:
            row['judge'] = {'skipped': 'No retrieved context or fallback'}
            continue
        test = LLMTestCase(input=row['question'], actual_output=row['answer'], retrieval_context=contexts)
        scores = {}
        for name, metric in [('faithfulness', FaithfulnessMetric(include_reason=True)), ('answer_relevancy', AnswerRelevancyMetric(include_reason=True))]:
            try:
                metric.measure(test)
                scores[name] = {'score': metric.score, 'reason': metric.reason}
            except Exception as exc:
                scores[name] = {'error': str(exc)}
        row['judge'] = scores
    output = source.with_name(source.stem + '_judged.json')
    output.write_text(json.dumps(rows, indent=2), encoding='utf-8')
    print(output)

if __name__ == '__main__':
    main()
