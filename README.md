### MDI AI Capstone: Evaluating Source-Grounded Question Answering in a Generative AI Nonprofit Document Assistant

University of Rochester | Simon Business School

Master of Science in Business Analytics & Applied AI

Course: GBA 475P — Capstone Project

Organization: Mission Document Intelligence AI, LLC (MDI AI)

Project: AI Nonprofit Document Assistant

Development Environment: Visual Studio Code (VS Code), Python, Streamlit

AI Evaluation Tools: Arize Phoenix, DeepEval

Data Visualization: Tableau

1. Project Overview
This capstone project evaluates the accuracy, source-grounded faithfulness, answer relevancy, and response latency of the AI Nonprofit Document Assistant, a generative AI application developed by Mission Document Intelligence AI, LLC (MDI AI).

The application uses a hybrid Retrieval-Augmented Generation (RAG) pipeline to retrieve information from nonprofit organizational documents and generate responses grounded in retrieved content.

The broader MDI AI platform is designed to support three interconnected nonprofit workflows:
- Document Management: Organizing and accessing nonprofit organizational knowledge.
- Document Creation: Generating drafts of nonprofit documents using organizational context.
- Document Intelligence: Retrieving, interpreting, and answering questions about organizational documents.
This capstone focuses specifically on evaluating source-grounded question answering.

The existing Streamlit-based RAG application was developed before the capstone. The primary new technical and analytical contribution is the integration of AI observability and evaluation tools, development of a structured testing methodology, and quantitative analysis of the RAG system's performance.

2. Business Problem Statement
Nonprofit organizations frequently manage large collections of strategic plans, program evaluations, policies, operational manuals, volunteer records, and advocacy documents.

Retrieving accurate information from these documents can require considerable administrative effort, particularly when information is distributed across multiple files.

Although generative AI can help organizations retrieve and summarize information, its responses may contain factual inaccuracies, unsupported statements, incomplete answers, or incorrect citations.

These limitations create potential risks for nonprofit organizations that rely on documented policies, program outcomes, and evidence-based reporting.
Primary Business Objective
Evaluate the reliability of the AI Nonprofit Document Assistant's hybrid RAG pipeline in answering questions using nonprofit organizational documents.

The evaluation focuses on four questions:
1. How consistently are generated answers supported by retrieved organizational documents?
2. How relevant are generated answers to users' questions?
3. How quickly does the language model generate responses?
4. What limitations and opportunities for improvement can be identified through AI observability and evaluation?
3. Technology Stack
Technology	Role
Python	Primary programming language
Visual Studio Code	Local development and debugging environment
Streamlit	Web application and evaluation dashboard
OpenAI API	Language model inference and embeddings
Hybrid RAG	Document retrieval and source-grounded answer generation
Arize Phoenix	AI observability, tracing, and latency monitoring
DeepEval	Automated LLM evaluation
Tableau	Business analytics and results visualization
GitHub	Version control and technical artifact repository

```
Technical Architecture
Nonprofit PDF Documents
          |
          v
Document Processing and Indexing
          |
          v
Hybrid RAG Retrieval Pipeline
          |
          v
Relevant Document Context
          |
          v
OpenAI Language Model
          |
          v
Source-Grounded Answer
          |
          +----------------------+
          |                      |
          v                      v
    Arize Phoenix            DeepEval
    Observability            Evaluation
          |                      |
          +-----------+----------+
                      |
                      v
              Evaluation Results
                      |
             +--------+--------+
             |                 |
             v                 v
       Streamlit           Tableau
       Dashboard           Dashboard
```

Arize Phoenix captures observable model activity and traces. DeepEval evaluates recorded answers using retrieved context. The results are exported for quantitative analysis and visualization.
4. Evaluation Methodology
4.1 Evaluation Design
The project uses a single-system evaluation methodology.

The objective was to establish measurable evidence of the application's current performance and identify opportunities for future improvement.
4.2 Evaluation Dataset
The evaluation used eight fictional Northbridge Community Alliance nonprofit documents covering strategic planning, program evaluation, food access operations, volunteer management, advocacy, and content integrity.

The test corpus included the following document types:
Document type	Evaluation purpose

Strategic Plan	Strategic priorities and organizational objectives

Program Evaluation Report	Program outcomes and numerical evidence

Internal Operations FAQ	Pantry policies and procedures

Food Access Policy Brief	Community needs and policy recommendations

Volunteer Onboarding Manual	Volunteer certification and assignment requirements

Volunteer Policy Brief	Volunteer participation barriers and recommendations

Advocacy FAQ	Organizational advocacy positions

Content Integrity & Citation Standard	Citation requirements and evidence limitations

All eight documents were uploaded to the Streamlit application for question-answering evaluation.

4.3 Test Questions

A structured dataset of 15 nonprofit document questions was developed to assess four categories.

Category	Questions	Evaluation focus

Strategic planning and program evaluation	Q1–Q5	Numerical accuracy and cross-document reasoning

Food pantry operations and policies	Q6–Q9	Policy retrieval and procedural accuracy

Volunteer management and advocacy	Q10–Q13	Organizational policies and advocacy interpretation

Citation integrity and hallucination resistance	Q14–Q15	Evidence attribution and unsupported claims

Each test question included an expected answer and an identified source document or combination of documents.

The test questions included single-document retrieval, cross-document synthesis, numerical interpretation, and questions requiring the assistant to acknowledge insufficient evidence.

The exported evaluation records use identifiers Q02–Q16. These identifiers should be reconciled with the original Q1–Q15 test-question numbering before making question-specific claims.

4.4 Evaluation Procedure

The following methodology was used:
1. Launch the AI Nonprofit Document Assistant locally using Streamlit.
2. Upload the eight Northbridge nonprofit PDF documents.
3. Select the Question Answering workflow.
4. Submit the 15 predefined evaluation questions.
5. Record model execution traces using Arize Phoenix.
6. Export the 15 question-answering records in JSONL format.
7. Prepare the recorded answers and retrieved context for DeepEval.
8. Evaluate faithfulness and answer relevancy using DeepEval.
9. Export evaluation results to CSV.
10. Analyze and visualize the results using Streamlit and Tableau.
The evaluation was conducted on recorded responses rather than requiring repeated generation of the same questions during automated scoring.

5. AI Observability: Arize Phoenix
Arize Phoenix is an open-source AI observability platform used to inspect and monitor LLM application behavior.

Phoenix was integrated into the local development environment to capture execution traces from the AI Nonprofit Document Assistant.
Observability Data
The recorded traces provided information about:
- User questions and model inputs.
- Generated answers.
- Retrieved context, where captured.
- Model execution activity.
- Response latency.
- Trace and span identifiers.
Phoenix enabled inspection of the underlying model activity rather than relying solely on the text displayed in Streamlit.
Phoenix Evaluation Workflow
```
Streamlit Application
        |
        v
Hybrid RAG Question Answering
        |
        v
Phoenix Tracing
        |
        v
15 ChatCompletion Records
        |
        v
JSONL Export
        |
        v
DeepEval Scoring
```

6. Automated Evaluation: DeepEval
DeepEval is an open-source framework for evaluating large language model applications.

It was used to assess two primary metrics.
Faithfulness
Faithfulness measures whether generated answers are supported by the retrieved context.

A higher score indicates that the answer is more consistent with the evidence provided to the language model.
Answer Relevancy
Answer relevancy measures how directly the generated response addresses the user's question.

A response may be grounded in source material but still receive a lower relevancy score if it does not adequately address the requested information.
Important Evaluation Distinction
Faithfulness and answer relevancy are automated LLM evaluation metrics.

They do not independently establish that every factual claim is correct or that every cited document and page number is accurate.

A separate manual source-citation review is necessary to validate citation integrity.

7. Evaluation Results
The evaluation produced the following results across 15 question-answering records.
Metric	Result
Total questions evaluated	15
Average faithfulness	99.26%
Average answer relevancy	93.86%
Average recorded LLM latency	2.10 seconds
Highest recorded LLM latency	3.954 seconds

7.1 Faithfulness Findings

The average faithfulness score was 99.26%.

Fourteen of the 15 evaluated responses received a perfect automated faithfulness score.

One response received approximately 88.89%.

These results suggest that the application generally generated answers consistent with the retrieved context in this test set.

However, the results should not be interpreted as a 99.26% independently verified factual accuracy rate.

7.2 Answer Relevancy Findings

The average answer relevancy score was 93.86%.

Although most responses achieved high relevancy scores, several questions demonstrated opportunities for improvement.

Notable recorded results included:
Recorded question ID	Answer relevancy
Q05	66.67%
Q03	77.78%
Q07	83.33%
Q14	85.71%

These scores indicate that some generated answers were less directly responsive to the corresponding questions, despite generally high faithfulness.
7.3 Response Latency Findings
Average recorded language model latency was approximately 2.10 seconds.

The highest recorded latency was approximately 3.954 seconds for Q13.

This metric reflects the recorded language model completion spans. It does not necessarily represent the complete user-facing response time, including document retrieval, preprocessing, and other application operations.

8. Tableau Data Visualization
   
Tableau was used to visualize and interpret the evaluation results.

Four worksheets were developed for the capstone analysis.
Worksheet 1: Faithfulness by Question
A bar chart displaying DeepEval faithfulness scores for each of the 15 evaluation questions.

Purpose: Identify responses with weaker grounding in retrieved context.
Worksheet 2: Answer Relevancy by Question
A bar chart comparing answer relevancy scores across the evaluation dataset.

Purpose: Identify questions for which the assistant generated less directly relevant answers.
Worksheet 3: Response Latency by Question
A bar chart displaying recorded language model response latency in seconds.

Purpose: Identify variation in model response times and unusually slow completions.
Worksheet 4: Answer Relevancy vs. Response Latency
A scatter plot examining the relationship between answer relevancy and response latency.

Purpose: Explore whether slower responses were associated with higher answer relevancy in the evaluation dataset.

Because the dataset contains only 15 observations, any apparent relationship should be treated as exploratory.

The four worksheets are consolidated into the MDI AI Hybrid RAG Evaluation Dashboard.

9. Key Findings and Business Insights
    
Finding 1: Strong automated source grounding

The high average faithfulness score indicates that the existing hybrid RAG system generally produced answers supported by retrieved document context during this evaluation.

Business implication: Source-grounded question answering may help nonprofit staff retrieve organizational information more consistently than relying on ungrounded generative AI responses.

Finding 2: Faithfulness and relevancy are different performance dimensions

Several answers received high faithfulness scores but lower answer relevancy scores.

This demonstrates that an answer can be supported by source material without fully addressing the user's question.

Business implication: MDI AI should evaluate both grounding and responsiveness when assessing the usefulness of its document intelligence capabilities.
Finding 3: Some questions require additional investigation
The lower-scoring questions provide opportunities to inspect retrieved passages, prompt construction, and answer generation behavior.

Business implication: Targeted improvements may be more useful than making broad modifications to the entire RAG pipeline.
Finding 4: Observability improves technical transparency
Phoenix traces provide a structured record of model execution and enable inspection of individual question-answering interactions.

Business implication: AI observability can support debugging, performance monitoring, and future quality assurance processes.

10. Project Limitations
    
This capstone has several limitations.

Small evaluation dataset: The evaluation included only 15 questions and eight representative nonprofit documents. The findings cannot establish performance across all nonprofit document types or real-world organizational environments.

Single-system evaluation: No baseline-versus-enhanced comparison was conducted. The project measures current system performance rather than demonstrating improvements from a new retrieval configuration.

Automated scoring limitations: DeepEval uses model-based judgments that may vary across evaluation models, prompts, and configurations.

Citation verification: Automated faithfulness scores do not substitute for manual verification of source documents, page references, and factual claims.

Latency measurement: Recorded completion latency does not represent full end-to-end application response time.

11. Recommendations and Future Improvements
    
The evaluation identifies several opportunities for future technical development.

1. Expand the evaluation dataset: Test more questions, nonprofit document types, and cross-document retrieval scenarios.
2. Improve answer relevancy: Investigate lower-scoring responses and consider targeted changes to retrieval, prompting, or response formatting.
3. Strengthen citation verification: Develop automated or human-reviewed checks that compare generated citations with the supporting source passages.
4. Evaluate retrieval performance: Introduce retrieval-specific metrics to assess whether the correct documents and passages were selected.
5. Measure end-to-end latency: Capture the complete workflow from question submission through retrieval and answer generation.
6. Repeat evaluations: Conduct additional testing across multiple runs to assess performance consistency.
These are recommendations for future work, not changes demonstrated by the current evaluation.

12. Recommended Repository Structure
```
MDI-AI-Capstone-Evaluation/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── app.py
├── hybrid_rag_pipeline.py
├── observability.py
├── deepeval_scoring_capstone.py
├── evaluation_dashboard_capstone.py
│
├── evaluation/
│   ├── evaluation_methodology.md
│   └── 15_test_questions.csv
│
├── test_docs/
│   └── Northbridge/
│
├── results/
│   ├── MDI_AI_DeepEval_Input.jsonl
│   ├── MDI_AI_DeepEval_Input_judged.json
│   └── MDI_AI_Tableau_Clean_15_Questions.csv
│
├── dashboards/
│   ├── MDI_AI_Tableau_Dashboard.twbx
│   └── dashboard_screenshot.png
│
├── reports/
│   └── MDI_AI_Capstone_Executive_Summary.pdf
│
└── presentation/
    ├── MDI_AI_Capstone_Presentation.pptx
    └── presentation_recording_link.md

```
This structure is recommended for the final repository. Some artifacts may still need to be added or renamed to match the files actually present in the project.

13. Capstone Deliverables
    
The final capstone includes the following technical and analytical artifacts:
- Working Streamlit AI Nonprofit Document Assistant.
- Existing hybrid RAG pipeline and relevant Python source code.
- Arize Phoenix observability integration.
- DeepEval scoring scripts and evaluation results.
- Fifteen-question evaluation dataset and methodology.
- Streamlit evaluation dashboard.
- Tableau evaluation dashboard.
- Two-page executive summary of business problems, findings, and impact.
- Recorded PowerPoint presentation.
- GitHub repository documenting the methodology and technical artifacts.
  
14. Business Impact
    
This project provides an initial, measurable assessment of the AI Nonprofit Document Assistant's source-grounded question-answering capabilities.

The evaluation demonstrates how open-source AI observability and evaluation tools can be integrated into an existing generative AI application to measure performance and identify potential weaknesses.

For MDI AI, the findings establish an early technical evaluation framework that can support future product development, testing, and quality assurance.

For nonprofit organizations, the research illustrates the potential of document-grounded AI systems to improve access to organizational knowledge while emphasizing the importance of reliable evidence, accurate citations, and transparent performance measurement.

The project does not establish verified staff time savings, production readiness, or performance improvements over an alternative RAG configuration. Those outcomes require additional evaluation.

15. Project Ownership and Academic Context
    
Mission Document Intelligence AI, LLC (MDI AI) is an independently developed AI startup focused on document intelligence for nonprofit organizations.

The AI Nonprofit Document Assistant prototype existed before the capstone project.

The new capstone contribution focuses on AI observability integration, systematic RAG evaluation, quantitative performance analysis, and business-oriented data visualization.

This repository documents the academic evaluation conducted as part of the University of Rochester Simon Business School's Master of Science in Business Analytics & Applied AI program.

Academic Institution: University of Rochester, Simon Business School
Course: GBA 475P — Capstone Project
Academic Term: Fall 2026
