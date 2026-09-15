# Autonomous Lead Enrichment Agent

An AI-powered Python agent that automatically crawls public company websites, extracts useful business information, and uses an LLM to generate structured company intelligence.

The system accepts one or more company domains as input and produces structured JSON output containing:

- Company Overview
- Target Audience / Ideal Customer Profile (ICP)
- Public Contact Emails
- Key Leadership / Team Members
- LinkedIn Profile URLs
- Data Confidence Score

---

## Features

- Automated website crawling using Playwright
- Headless browser automation for JavaScript-rendered websites
- Discovers relevant company pages such as:
  - Homepage
  - About
  - Company
  - Team
  - Contact
  - Pricing
  - Customers
  - Solutions
  - Products
- Extracts clean webpage text instead of sending raw HTML to the LLM
- Removes unnecessary scripts, CSS, SVG and navigation content
- Uses Pydantic models for structured LLM output
- Extracts publicly available contact emails
- Extracts leadership/team information
- Extracts LinkedIn profile URLs when available
- Generates a confidence score between 0.0 and 1.0
- Handles website failures and timeouts without stopping the entire pipeline
- Supports processing multiple company domains
- Saves results in JSON format

---

## Project Architecture

```text
autonomous-lead-enrichment-agent/
│
├── src/
│   ├── config.py
│   ├── extractor.py
│   ├── main.py
│   ├── models.py
│   └── scraper.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── LOOM_SCRIPT.md
├── OPERATIONS_ANSWER.md
│
├── output.json
├── postman_test.html
├── supabase_test.html
└── vapi_test.html
