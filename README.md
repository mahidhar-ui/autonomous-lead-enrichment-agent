# Autonomous Lead Enrichment Agent

A Python-based autonomous lead enrichment agent that crawls public company websites, extracts useful business information, and uses an LLM to generate structured company intelligence.

## Project Objective

The objective of this project is to automate the process of researching companies from their public websites.

The agent accepts one or more company domains as input and attempts to:

- Crawl the company homepage and relevant subpages
- Extract clean webpage text instead of sending raw HTML to the LLM
- Identify company information
- Extract public contact emails
- Identify target audience / Ideal Customer Profile (ICP)
- Extract leadership and team information
- Find LinkedIn URLs when available
- Generate a confidence score
- Handle website failures without stopping the complete process

## Test Companies

The solution was tested against:

1. postman.com
2. supabase.com
3. vapi.ai

## Project Structure

```text
autonomous-lead-enrichment-agent/
│
├── src/
│   ├── __init__.py
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
├── vapi_test.html
└── test_supabase.json





tic validation, and resilient error handling.
