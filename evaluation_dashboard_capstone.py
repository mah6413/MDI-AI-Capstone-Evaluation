"""Single-system evaluation dashboard for Phoenix-derived DeepEval data."""
import io
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title='MDI AI | Hybrid RAG Evaluation', layout='wide')
st.title('MDI AI — Hybrid RAG Evaluation')
st.caption('Single-system assessment of the existing hybrid RAG pipeline. No baseline/enhanced comparison.')
file = st.file_uploader('Upload Phoenix-derived DeepEval JSONL or judged JSON', type=['jsonl', 'json'])
review_file = st.file_uploader('Optional: upload completed manual review CSV', type=['csv'])
if file is None:
    st.info('Upload results/MDI_AI_DeepEval_Input.jsonl to inspect 15 answers, or the *_judged.json output to show DeepEval scores.')
    st.stop()
try:
    raw = file.getvalue().decode('utf-8-sig')
    rows = ([json.loads(line) for line in raw.splitlines() if line.strip()]
            if file.name.lower().endswith('.jsonl') else json.loads(raw))
    if not isinstance(rows, list):
        raise ValueError('Expected a list of records')
except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
    st.error(f'Cannot read file: {exc}')
    st.stop()

records = []
for index, row in enumerate(rows, 1):
    judge = row.get('judge') or {}
    meta = row.get('metadata') or {}
    if not isinstance(meta, dict):
        meta = {}
    contexts = row.get('retrieval_context', row.get('citations', []))
    if isinstance(contexts, str):
        contexts = [contexts]
    if not isinstance(contexts, list):
        contexts = []
    records.append({
        'Test ID': row.get('id') or f'Q{index:02}',
        'Question': row.get('input') or row.get('question'),
        'Answer': row.get('actual_output') or row.get('answer'),
        'Reference answer': row.get('expected_output') or row.get('reference_answer'),
        'Retrieved context': '\n\n'.join(str(c.get('excerpt') or c) if isinstance(c, dict) else str(c) for c in contexts),
        'Trace ID': meta.get('trace_id') or row.get('trace_id'),
        'LLM latency (s)': meta.get('latency_seconds') or row.get('latency_seconds'),
        'Faithfulness': (judge.get('faithfulness') or {}).get('score'),
        'Answer relevance': (judge.get('answer_relevancy') or {}).get('score'),
        'Faithfulness reason': (judge.get('faithfulness') or {}).get('reason'),
        'Relevance reason': (judge.get('answer_relevancy') or {}).get('reason'),
    })
df = pd.DataFrame(records)
for col in ['LLM latency (s)', 'Faithfulness', 'Answer relevance']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

if review_file is not None:
    try:
        review = pd.read_csv(review_file)
        st.caption('Manual review uploaded. Scores are displayed only if the CSV includes a numeric correctness or citation-support field.')
        candidates = {c.lower().strip().replace(' ', '_'): c for c in review.columns}
        key = next((candidates[k] for k in ('test_id', 'id', 'question_id') if k in candidates), None)
        if key is None:
            st.warning('Manual review CSV has no Test ID column; it was not joined to the results.')
        else:
            review = review.rename(columns={key: 'Test ID'})
            review['Test ID'] = review['Test ID'].astype(str)
            df['Test ID'] = df['Test ID'].astype(str)
            for normalized, label in [('answer_correctness', 'Manual correctness'), ('correctness', 'Manual correctness'), ('citation_support', 'Manual citation support'), ('citation_accuracy', 'Manual citation support')]:
                if normalized in candidates and label not in df.columns:
                    review[label] = pd.to_numeric(review[candidates[normalized]], errors='coerce')
            cols = ['Test ID'] + [c for c in ['Manual correctness', 'Manual citation support'] if c in review]
            if len(cols) > 1:
                df = df.merge(review[cols].drop_duplicates('Test ID'), on='Test ID', how='left')
            else:
                st.info('Manual review labels were not found in numeric columns; you can still inspect the file separately.')
    except Exception as exc:
        st.warning(f'Could not process manual review CSV: {exc}')

st.subheader('Evaluation summary')
cols = st.columns(4)
cols[0].metric('Answers recorded', len(df))
for col, label, slot in [('Faithfulness', 'Mean faithfulness', 1), ('Answer relevance', 'Mean answer relevance', 2), ('LLM latency (s)', 'Mean LLM latency', 3)]:
    valid = df[col].dropna()
    cols[slot].metric(label, f'{valid.mean():.3f}' + (' s' if slot == 3 else '') if len(valid) else 'N/A')

for label in ['Manual correctness', 'Manual citation support']:
    if label in df:
        valid = df[label].dropna()
        st.metric(f'Mean {label.lower()}', f'{valid.mean():.3f}' if len(valid) else 'N/A')

available = [c for c in ['Faithfulness', 'Answer relevance', 'LLM latency (s)', 'Manual correctness', 'Manual citation support'] if c in df and df[c].notna().any()]
if available:
    metric = st.selectbox('Metric by question', available)
    st.bar_chart(df.set_index('Test ID')[[metric]], y_label=metric)
else:
    st.info('No scored metrics yet. Run DeepEval to populate faithfulness and relevance.')

st.subheader('Per-question results')
st.dataframe(df, hide_index=True, use_container_width=True)
st.download_button('Download evaluation CSV', df.to_csv(index=False).encode('utf-8'), 'mdi_ai_hybrid_rag_evaluation.csv', 'text/csv')
st.caption('DeepEval faithfulness/relevance are model-judged scores, not verified factual correctness. Citation-support must be checked against the underlying PDFs. Latency is the LLM span, not end-to-end RAG time.')
