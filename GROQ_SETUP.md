# Groq Setup

This version of the project uses **Groq + LangChain**, not OpenAI.

## Streamlit Cloud Secret

In your Streamlit app:

**Settings → Secrets**

Add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Do not put the key inside Python code or commit it to GitHub.

## Model

The default model is:

```text
openai/gpt-oss-120b
```

Groq currently recommends GPT-OSS models for newer workloads, while older Llama model IDs have been deprecated. You can change the model in the sidebar if your Groq account provides another supported model.

## Important

Your Groq API key must be valid and active. Keep it private.
