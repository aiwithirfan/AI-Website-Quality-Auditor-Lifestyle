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



GROQ_API_KEY = "your_groq_api_key_here"

Deploy.
Enter 3–5 authorized/public Lifestyle URLs and click Run Website Audit.
Important: authorized/public websites
Only analyze websites that you are authorized to audit or that the assignment explicitly permits you to analyze. The tool makes normal HTTP requests to the supplied public homepage; it is not a vulnerability scanner.
