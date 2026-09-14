# Week 2 Demo Video — Suggested Speaking Guide

Hello, my name is Irfan Shah. This is my Week 2 individual project,
AI-Assisted Website Quality Auditor for Lifestyle Websites.

The purpose of this project is to combine deterministic website checks
with AI-generated judgment while keeping the two clearly separated.

First, I enter 3 to 5 authorized/public Lifestyle website URLs.

The Python audit engine uses Requests and BeautifulSoup to fetch the
homepage and detect factual signals such as internal links, contact
information, contact forms, social links, CTA elements, HTTPS, and
basic mobile-responsiveness indicators.

Next, LangChain sends those collected signals and a short text summary
to the AI model. The model generates a score from 0 to 100, problems,
missing features, recommendations, and priority.

An important design decision is that the application labels the
deterministic signals as Automatically Detected Facts and the model
output as AI-Generated Judgment. This reduces confusion between
observable evidence and subjective evaluation.

Now I will run the audit and show the results for each website.

After reviewing the results manually, I identified two cases where I
would adjust the AI's judgment. I explain those differences in my
manual review and use them to improve the prompt or logic.

This project helped me understand how LangChain can be used as the
AI orchestration layer while Python handles deterministic QA checks.
