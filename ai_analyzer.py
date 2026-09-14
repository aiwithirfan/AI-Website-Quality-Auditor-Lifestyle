import os
from typing import List

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class WebsiteJudgment(BaseModel):
    score: int = Field(
        ge=0,
        le=100,
        description="Overall professionalism, completeness, and business-function score."
    )
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
            """You are a professional website quality auditor for Lifestyle businesses.

Evaluate the website based ONLY on the automatically detected facts
and the supplied page text summary.

IMPORTANT RULES:

1. Clearly distinguish observable facts from AI judgment.
2. Do NOT invent facts or claim that a feature exists or does not exist
   unless the supplied evidence supports that conclusion.
3. Do NOT assume that every Lifestyle website needs e-commerce,
   checkout, live chat, user accounts, subscription systems, or a help center.
4. Consider the likely business model of the website.
   An editorial, magazine, fashion, entertainment, or content website
   does not automatically require an online shop.
5. If a feature cannot be verified from the supplied evidence,
   do NOT call it a missing feature.
6. When evidence is insufficient, use wording such as
   "Not verified by the automated audit."
7. Base the score mainly on observable signals such as:
   navigation/link structure, contact accessibility, social presence,
   CTA availability, HTTPS, mobile/responsive indicators,
   page completeness, and quality of the supplied page content.
8. The score is an AI-generated judgment, NOT an automatically detected fact.
9. Recommendations must be relevant to the website's apparent business model.
10. Keep the output concise, realistic, and actionable.

Priority must be exactly one of:
Low, Medium, High."""
        ),
        (
            "human",
            """Audit this Lifestyle website.

AUTOMATICALLY DETECTED FACTS:
{facts}

PAGE TEXT SUMMARY:
{summary}

SCORING GUIDANCE:

90-100:
Highly professional, complete, strong business functionality,
and very few observable weaknesses.

75-89:
Professional website with some minor or moderate improvements needed.

60-74:
Usable/basic website with several observable weaknesses.

40-59:
Weak website with significant professionalism or functionality issues.

0-39:
Major observable problems affecting usability, completeness,
professionalism, or business functionality.

IMPORTANT:
Do not reduce the score simply because an unverified feature such as
e-commerce, live chat, checkout, user accounts, or subscription pricing
was not detected.

Return:
- Score
- Problems
- Missing Features
- Recommendations
- Priority

Only include problems and missing features that are supported by
the supplied evidence."""
        ),
    ])

    llm = ChatGroq(
        model=model_name,
        temperature=0,
        api_key=os.environ["GROQ_API_KEY"],
    )

    structured_llm = llm.with_structured_output(WebsiteJudgment)

    safe_facts = {
        k: v
        for k, v in facts.items()
        if k != "text_summary"
    }

    result = (prompt | structured_llm).invoke({
        "facts": safe_facts,
        "summary": facts.get("text_summary", ""),
    })

    return result.model_dump()
