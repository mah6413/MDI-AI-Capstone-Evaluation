# MDI AI capstone evaluation

The original Streamlit document-generation and Q&A functions remain available. New files add **optional** Phoenix tracing and a reproducible evaluation harness. Existing code is not replaced by a new framework.

## Setup

1. Create a virtual environment and install `pip install -r requirements-observability.txt`.
2. Set `OPENAI_API_KEY` in your local `.env` (never commit it). Use **synthetic** documents and questions.
3. Start Phoenix in another terminal: `phoenix serve`.
4. Enable tracing with `MDI_ENABLE_TRACING=true` before launching `streamlit run app.py` or running evaluation. With tracing off, Phoenix is not needed.
5. Create a JSONL dataset following `eval_cases.example.jsonl`, using your own documents and verified answers.
6. Run `python evaluation.py --dataset eval_cases.jsonl --output results.json`.
7. Optional paid LLM judging: `python deepeval_scoring.py results.json`.

## What the metrics mean

- **Citation ID validity** checks that generated citation tokens refer to source records returned by retrieval; it does **not** establish factual support.
- **Retrieval recall@k** checks the proportion of annotated relevant chunk IDs present in retrieved results.
- **Citation source precision** checks whether cited chunk IDs match annotated gold chunks; it is a *proxy*, not claim-level citation faithfulness.
- **DeepEval faithfulness** estimates whether answers are supported by retrieved context; it does not individually validate each citation.
- **Answer relevancy** estimates whether the answer addresses the question; it is not reference-answer correctness.

For the capstone's **ground-source citation accuracy**, add a human-rated claim-by-claim rubric (claim, cited token, passage, supported yes/no) before reporting a final accuracy rate. Gold chunk IDs are sensitive to chunking changes, so keep chunk size and document order fixed when comparing weights. Results are not guaranteed to improve.

## Privacy and cost

Phoenix traces may contain source excerpts, prompts, and generated responses. Only use synthetic or explicitly approved, de-identified test data. OpenAI generation, embeddings, and LLM judge calls incur usage charges. The pipeline currently re-embeds files on every run, increasing cost. Do not expose tracing dashboards publicly.

## Evaluation dashboard
Install the dashboard dependency with `python -m pip install pandas` (Streamlit is already required), then run `streamlit run evaluation_dashboard.py`. Upload the JSON output produced by `evaluation.py` or the optional judged JSON produced by `deepeval_scoring.py`. The dashboard shows real recorded scores only; absent measures appear as N/A. Citation token validity and citation source precision are *not* claim-level citation support accuracy.
