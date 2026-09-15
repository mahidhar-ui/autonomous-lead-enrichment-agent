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





Technologies Used
Python
Playwright
Pydantic
LLM API
BeautifulSoup / DOM text extraction
Regular Expressions
JSON
Environment Variables
Git and GitHub
Architecture

The project follows a modular architecture:

Company Domains
      |
      v
Website Crawler
      |
      v
Homepage + Relevant Subpages
      |
      v
Clean Text / DOM Extraction
      |
      v
Text Pre-processing
      |
      v
LLM Extraction
      |
      v
Pydantic Structured Output
      |
      v
Confidence Score
      |
      v
output.json
How the Agent Works
1. Input

The application accepts company domains from the command line.

Example:

python -m src.main postman.com supabase.com vapi.ai --output output.json

A single domain can also be processed:

python -m src.main supabase.com --output test_supabase.json
2. Website Crawling

The scraper attempts to access the company homepage and relevant pages such as:

/about
/company
/team
/contact
/pricing
/customers
/solutions
/products

Playwright is used for browser automation so that JavaScript-rendered websites can also be handled.

3. Content Pre-processing

The project does not send the complete raw HTML tree to the LLM.

Instead, webpage content is converted into useful text by removing unnecessary elements such as:

Scripts
CSS
SVG elements
Navigation boilerplate
Unnecessary HTML markup

This reduces the amount of information sent to the LLM and helps reduce token usage.

4. Information Extraction

The LLM is used to extract structured company intelligence.

The expected fields include:

Company overview
Target audience / ICP
Public contact emails
Leadership / team members
Job titles
LinkedIn URLs
Confidence score
5. Structured Output

Pydantic models are used to validate the extracted information.

The final information is stored as JSON.

Example structure:

{
  "domain": "example.com",
  "company_overview": "Company description...",
  "target_audience": "Target customers...",
  "contact_emails": [],
  "leadership": [],
  "confidence_score": 0.0
}
Error Handling

The scraper is designed to handle common website problems such as:

Connection timeouts
DNS problems
404 pages
Missing pages
JavaScript loading problems
Empty webpage content
Website blocking
Missing emails
Missing leadership information

A failure on one company should not stop processing of the remaining companies.

For example, if postman.com fails because of a network timeout, the agent can continue processing supabase.com and vapi.ai.

Environment Setup
Step 1: Create Virtual Environment
python -m venv venv
Step 2: Activate Virtual Environment
.\venv\Scripts\Activate.ps1
Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Configure Environment Variables

Create a .env file in the project root.

Example:

LLM_API_KEY=your_api_key_here

Use the variable names expected by the project configuration.

Never commit API keys to GitHub.

Running the Project

Process all three test companies:

python -m src.main postman.com supabase.com vapi.ai --output output.json

Process one company:

python -m src.main supabase.com --output test_supabase.json
Output

The generated results are saved to:

output.json

A separate test output can also be generated:

test_supabase.json
Network Resilience

During development, some target websites may be inaccessible because of local network routing, DNS, IPv4/IPv6 connectivity, firewall restrictions, CDN behavior, or website-side protection.

The project therefore treats website access failures as recoverable errors instead of allowing the complete pipeline to crash.

The project also includes locally captured HTML test files:

postman_test.html
supabase_test.html
vapi_test.html

These can be useful for validating extraction logic independently from live network availability.

GitHub Submission

The repository should contain:

src/
.env.example
.gitignore
requirements.txt
README.md
LOOM_SCRIPT.md
OPERATIONS_ANSWER.md
output.json

The .env file containing actual API keys must NOT be uploaded to GitHub.

Future Improvements

Possible future improvements include:

Search-engine integration using Tavily or SerpAPI
External LinkedIn discovery
LangGraph-based agent orchestration
Browser-use integration
Token and API cost tracking
Better website prioritization
Concurrent crawling
Persistent company database
LLM observability
Automated evaluation of extraction quality
Conclusion

This project demonstrates an end-to-end approach to autonomous lead enrichment using browser automation, webpage text extraction, LLM-based structured information extraction, Pydantic validation, and resilient error handling.
