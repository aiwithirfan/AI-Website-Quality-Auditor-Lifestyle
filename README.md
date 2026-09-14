# AI-Assisted Website Quality Auditor for Lifestyle Websites

Week 2 individual project.

## Objective

This project audits 3–5 authorized/public Lifestyle website homepages and separates:

1. **Automatically detected facts** — collected with Python, Requests, and BeautifulSoup.
2. **AI-generated judgment** — generated with LangChain + an LLM from the collected facts and a short page-text summary.

## Features

The auditor detects:

- HTTP status
- HTTPS
- page/internal-link count
- contact information indicators
- contact form
- social-media links
- CTA buttons/links
- viewport meta tag
- basic responsive CSS indicators
- page title and heading samples

The AI produces:

- Score (0–100)
- Problems
- Missing Features
- Recommendations
- Priority

## Technology

- Python
- Streamlit
- Requests
- BeautifulSoup
- LangChain
- Groq API
- Pydantic structured output

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload all project files from this folder.
3. In Streamlit Community Cloud, create a new app.
4. Select the repository and `app.py`.
5. Add the secret:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

6. Deploy.
7. Enter 3–5 authorized/public Lifestyle URLs and click **Run Website Audit**.

## Important: authorized/public websites

Only analyze websites that you are authorized to audit or that the assignment explicitly permits you to analyze. The tool makes normal HTTP requests to the supplied public homepage; it is not a vulnerability scanner.

## Methodology

### Stage 1 — deterministic checks

`audit_engine.py` fetches each homepage and extracts observable signals. These values are displayed under **Automatically Detected Facts**.

### Stage 2 — AI judgment

`ai_analyzer.py` uses LangChain to send the extracted signals and a short text summary to the AI model. The AI returns a structured object containing score, problems, missing features, recommendations, and priority.

The application deliberately labels these outputs **AI-Generated Judgment** so facts and interpretation are not mixed.

## Limitations

- Internal link count is a homepage link count, not a complete crawl of the entire domain.
- Mobile responsiveness is estimated from HTML/CSS indicators; it is not a real browser/device test.
- JavaScript-rendered content may not appear in Requests/BeautifulSoup.
- Contact/social/CTA detection is heuristic.
- The AI score is judgment-based and should be manually reviewed.

## Manual review requirement

For the final assignment, record at least two cases where your own review differs from the AI score or recommendation. Explain why and then improve the prompt or logic.

Suggested table:

| Website | AI Score | Your Score | Difference | Why | Prompt/Logic Improvement |
|---|---:|---:|---:|---|---|
| Site 1 |  |  |  |  |  |
| Site 2 |  |  |  |  |  |

## Demo video checklist

Show:

1. GitHub repository
2. Streamlit application
3. 3–5 URLs entered
4. Audit run
5. Automatically Detected Facts
6. AI-Generated Judgment
7. Score/problems/missing features/recommendations/priority
8. Explain LangChain's role
9. Explain facts vs AI judgment
10. Explain two manual-review adjustments
