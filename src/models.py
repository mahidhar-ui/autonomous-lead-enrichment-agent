import json
import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from openai import OpenAI


load_dotenv()


# =========================================================
# PYDANTIC MODELS
# =========================================================

class LeadershipMember(BaseModel):

    name: str = ""

    role: str = ""

    linkedin_url: str = ""


class CompanyIntelligence(BaseModel):

    company_overview: str = Field(
        default="",
        description="Concise two-sentence company overview."
    )

    target_audience_icp: str = Field(
        default="",
        description="Ideal customer profile and target audience."
    )

    contact_points: List[str] = Field(
        default_factory=list,
        description="Public generic company emails."
    )

    leadership: List[LeadershipMember] = Field(
        default_factory=list,
        description="Leadership/team members found in website content."
    )

    confidence_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )


# =========================================================
# CREATE CLIENT
# =========================================================

def create_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:

        raise ValueError(
            "GROQ_API_KEY is missing from .env"
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )


# =========================================================
# LLM EXTRACTION
# =========================================================

def extract_company_intelligence(
    domain: str,
    website_text: str,
    emails: List[str]
):

    client = create_client()

    # Limit input to avoid excessive tokens
    website_text = website_text[:60000]

    system_prompt = """
You are an expert B2B lead enrichment analyst.

Analyze the provided public website content.

Extract ONLY information supported by the provided content.

Do not invent names, emails, roles, LinkedIn URLs,
customers, or business claims.

Return structured JSON matching the requested schema.

For confidence_score:

1.0 = highly complete and strongly supported
0.8 = good information with minor gaps
0.6 = moderate information
0.4 = limited information
0.2 = very little information
0.0 = almost no usable information
"""

    user_prompt = f"""
Company domain:

{domain}

Public emails already detected:

{json.dumps(emails, indent=2)}

Website content:

{website_text}

Extract:

1. Company Overview
   - Exactly two concise sentences.

2. Target Audience / ICP
   - Explain who the company builds its products/services for.

3. Contact Points
   - Include generic/public emails found in the supplied content.
   - Examples: contact@, sales@, support@.
   - Do not invent emails.

4. Key Leadership / Team Members
   - Extract names and roles only when supported.
   - Include LinkedIn URLs only if present in the content.

5. Confidence Score
   - Between 0.0 and 1.0.
"""

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0,

        response_format={
            "type": "json_object"
        }
    )

    content = response.choices[0].message.content

    data = json.loads(content)

    # Validate using Pydantic
    validated = CompanyIntelligence.model_validate(
        data
    )

    return validated.model_dump()