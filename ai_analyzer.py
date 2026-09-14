
import os
from typing import List

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class WebsiteJudgment(BaseModel):
    score: int = Field(ge=0, le=100, description="Overall professionalism/business-function score.")
    problems: List[str] = Field(min_length=1, max_length=6)
    missing_features: List[str] = Field(min_length=1, max_length=6)
    recommendations: List[str] = Field(min_length=1, max_length=6)
    priority: str = Field(description="One of Low, Medium, High.")


def generate_ai_judgment(
    facts: dict,
    model_name: str = "openai/gpt-oss-120b"
) -> dict:
    if not os.getenv("GROQ_API_KEY"):
        return None

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a website quality auditor for Lifestyle businesses.
Evaluate professionalism, completeness, and business functionality.
Use ONLY the supplied factual signals and page summary. Do not invent features.
Return a balanced score from 0 to 100.
The score is a judgment, not a directly detected fact.
Priority must be Low, Medium, or High.
Keep each list concise and actionable."""
        ),
        (
            "human",
            """Audit this Lifestyle website.

AUTOMATICALLY DETECTED FACTS:
{facts}

PAGE TEXT SUMMARY:
{summary}

Scoring guidance:
- 90-100: highly professional and complete
- 75-89: professional with minor gaps
- 60-74: usable/basic with several gaps
- 40-59: weak or outdated indicators
- 0-39: major functionality/completeness problems

Return the structured judgment."""
        ),
    ])

    llm = ChatGroq(
        model=model_name,
        temperature=0,
        api_key=os.environ["GROQ_API_KEY"],
    )
    structured_llm = llm.with_structured_output(WebsiteJudgment)

    safe_facts = {k: v for k, v in facts.items() if k != "text_summary"}

    result = (prompt | structured_llm).invoke({
        "facts": safe_facts,
        "summary": facts.get("text_summary", ""),
    })

    return result.model_dump()
