## 1. Introduction — 15 seconds

Hello, this is my Autonomous Lead Enrichment Agent.

The goal of this project is to take company domains as input, automatically crawl their public web presence, extract useful information, and use an LLM to convert that information into structured company intelligence.

The test companies provided for this assignment are Postman, Supabase, and Vapi.

---

## 2. Project Structure — 25 seconds

Here is the project structure.

Inside the `src` folder, I have separated the application into different modules.

`main.py` is responsible for running the application and processing the input domains.

`scraper.py` handles website crawling and webpage content retrieval.

`extractor.py` handles the extraction and LLM processing.

`models.py` contains the structured Pydantic models.

`config.py` handles configuration and environment variables.

I have also included:

- requirements.txt
- .env.example
- README.md
- output.json
- test HTML files
- operations answer

---

## 3. Crawling and Pre-processing — 35 seconds

The scraper uses Playwright for browser automation.

The agent attempts to visit the homepage and relevant company pages such as:

- About
- Company
- Team
- Contact
- Pricing
- Customers
- Solutions
- Products

Instead of sending the complete raw HTML to the LLM, the application extracts useful webpage text and removes unnecessary content such as scripts, CSS, SVGs, and other webpage boilerplate.

This helps reduce the amount of data sent to the LLM and improves efficiency.

---

## 4. Structured LLM Extraction — 35 seconds

After collecting the webpage content, the extracted information is passed to the LLM.

The model is instructed to return structured company intelligence.

The important fields include:

- Company overview
- Target audience or ICP
- Public contact emails
- Leadership and team members
- Roles and titles
- LinkedIn URLs when available
- Data confidence score

Pydantic models are used to validate the structured response.

---

## 5. Running the Application — 25 seconds

Now I will run the application using the three test domains.

The command is:
```powershell
python -m src.main postman.com supabase.com vapi.ai --output output.json