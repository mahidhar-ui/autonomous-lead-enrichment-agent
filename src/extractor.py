import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


load_dotenv()


# ============================================================
# PYDANTIC STRUCTURED OUTPUT MODELS
# ============================================================

class LeadershipMember(BaseModel):

    name: str = ""

    role: str = ""

    linkedin_url: str = ""


class CompanyData(BaseModel):

    company_overview: str = ""

    target_audience: str = ""

    contact_points: List[str] = Field(
        default_factory=list
    )

    key_leadership: List[LeadershipMember] = Field(
        default_factory=list
    )

    confidence_score: float = 0.0


# ============================================================
# LLM EXTRACTION
# ============================================================

def extract_company_data(
    domain: str,
    website_text: str
) -> dict:

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:

        print(
            "WARNING: OPENAI_API_KEY not found."
        )

        return {
            "company_overview": "",
            "target_audience": "",
            "contact_points": [],
            "key_leadership": [],
            "confidence_score": 0.0,
        }

    client = OpenAI(
        api_key=api_key
    )

    # Keep prompt reasonably small
    website_text = website_text[:40000]

    prompt = f"""
You are an expert B2B lead enrichment analyst.

Analyze the following public website information.

Company domain:
{domain}

Website information:
{website_text}

Extract only information supported by the website content.

Requirements:

1. Company Overview
Write exactly two concise sentences explaining what the company does.

2. Target Audience / ICP
Identify who the company's product or service is primarily built for.

3. Contact Points
Extract publicly visible generic business emails such as:
contact@
sales@
support@
hello@
info@

Do not invent email addresses.

4. Key Leadership / Team Members
Extract names and roles when available.
Include LinkedIn URLs only if they appear in the provided website content.

Do not invent people or LinkedIn URLs.

5. Confidence Score
Give a number between 0.0 and 1.0 based on:
- amount of useful information found
- quality of evidence
- completeness of extraction

Return structured data only.
"""

    try:

        response = client.beta.chat.completions.parse(

            model="gpt-4o-mini",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract accurate structured "
                        "company intelligence. "
                        "Never invent missing information."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            response_format=CompanyData,
        )

        parsed = response.choices[0].message.parsed

        if parsed is None:

            return {
                "company_overview": "",
                "target_audience": "",
                "contact_points": [],
                "key_leadership": [],
                "confidence_score": 0.0,
            }

        result = parsed.model_dump()

        # Make sure confidence stays within 0-1
        score = result.get(
            "confidence_score",
            0.0
        )

        result["confidence_score"] = max(
            0.0,
            min(1.0, float(score))
        )

        return result

    except Exception as e:

        print(
            f"LLM extraction failed: {e}"
        )

        return {
            "company_overview": "",
            "target_audience": "",
            "contact_points": [],
            "key_leadership": [],
            "confidence_score": 0.0,
        }