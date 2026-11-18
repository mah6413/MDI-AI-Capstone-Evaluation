"""Streamlit dashboard for capstone evaluation JSON results (no fabricated scores)."""
import json
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title='MDI AI | RAG Evaluation', layout='wide')
st.title('MDI AI — RAG Evaluation Dashboard')
st.caption('Compare baseline and enhanced retrieval using actual evaluation results. Missing metrics are shown as unavailable, not zero.')
file = st.file_uploader('Upload evaluation_results.json or evaluation_results_judged.json', type=['json'])
def load_rows(source):
    data = json.load(source)
    if not isinstance(data, list):
        raise ValueError('Expected a JSON array of evaluation records')
    return data
if file is None:
    st.info('Run `python evaluation.py --dataset eval_cases.example.jsonl --output evaluation_results.json`, then upload the output here. Optional: run `python deepeval_scoring.py evaluation_results.json` for faithfulness and answer relevance scores (API charges may apply).')
    st.stop()
try:
    rows = load_rows(file)
except (ValueError, json.JSONDecodeError) as exc:
    st.error(f'Unable to read results: {exc}')
    st.stop()
if not rows:
    st.warning('No evaluation records found.')
    st.stop()
records=[]
for row in rows:
    judge=row.get('judge') or {}
    records.append({
        'Test ID':row.get('id'), 'Configuration':row.get('configuration'),
        'Question':row.get('question'), 'Answer':row.get('answer'),
        'Reference answer':row.get('reference_answer'),
        'Latency (s)':row.get('latency_seconds'),
        'Citation token validity':row.get('citation_id_validity'),
        'Citation source precision':row.get('citation_source_precision'),
        'Retrieval recall@k':row.get('retrieval_recall_at_k'),
        'Faithfulness (LLM judge)':(judge.get('faithfulness') or {}).get('score'),
        'Answer relevance (LLM judge)':(judge.get('answer_relevancy') or {}).get('score'),
        'Fallback':row.get('fallback_used'),
    })
df=pd.DataFrame(records)
metrics=['Citation token validity','Citation source precision','Retrieval recall@k','Faithfulness (LLM judge)','Answer relevance (LLM judge)','Latency (s)']
for col in metrics:
    df[col]=pd.to_numeric(df[col], errors='coerce')
options=sorted(df['Configuration'].dropna().unique().tolist())
selected=st.multiselect('Configurations', options, default=options)
view=df[df['Configuration'].isin(selected)]
if view.empty:
    st.warning('Select at least one configuration.')
    st.stop()
st.subheader('Evaluation summary')
summary=view.groupby('Configuration', dropna=False)[metrics].mean().T
st.dataframe(summary.style.format('{:.3f}', na_rep='N/A'), use_container_width=True)
metric=st.selectbox('Metric to visualize', metrics, index=1)
chart=view.groupby('Configuration')[metric].mean().dropna()
if chart.empty:
    st.info('This metric has not been measured in the uploaded results.')
else:
    st.bar_chart(chart, y_label=metric)
if metric=='Citation source precision':
    st.caption('Citation source precision measures overlap with annotated supporting chunk IDs; it is not claim-level semantic citation verification.')
if metric=='Citation token validity':
    st.caption('Citation token validity verifies that referenced citation IDs exist, not that the passages support the answer.')
st.subheader('Per-question comparison')
st.dataframe(view[['Test ID','Configuration','Question']+metrics+['Fallback']], hide_index=True, use_container_width=True)
st.download_button('Download summary CSV', view.to_csv(index=False).encode('utf-8'), file_name='mdi_ai_evaluation_summary.csv', mime='text/csv')
st.caption('Missing correctness or claim-level citation-support scores are not inferred. Add independently graded labels or a dedicated claim-level citation evaluator before reporting these as capstone outcomes.')
