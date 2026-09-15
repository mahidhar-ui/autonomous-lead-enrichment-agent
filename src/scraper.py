import re
import subprocess
import time
from typing import Dict, List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False


# Pages that are useful for company intelligence
IMPORTANT_PATHS = [
    "/about",
    "/company",
    "/team",
    "/contact",
    "/pricing",
    "/customers",
    "/solutions",
    "/products",
]


def normalize_url(domain: str) -> str:
    """
    Convert a domain such as supabase.com into:
    https://supabase.com/
    """

    domain = domain.strip()

    if not domain.startswith("http://") and not domain.startswith("https://"):
        domain = "https://" + domain

    return domain.rstrip("/") + "/"


def clean_text(html: str) -> str:
    """
    Convert raw HTML into clean text.

    Removes:
    - scripts
    - styles
    - SVG
    - navigation
    - footer
    - excessive whitespace
    """

    soup = BeautifulSoup(html, "html.parser")

    # Remove unnecessary elements
    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "nav",
        "footer",
        "form"
    ]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    lines = []

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            lines.append(line)

    # Remove duplicate consecutive lines
    cleaned = []
    previous = None

    for line in lines:
        if line != previous:
            cleaned.append(line)

        previous = line

    text = "\n".join(cleaned)

    # Token optimization
    return text[:15000]


def extract_emails(text: str) -> List[str]:
    """
    Extract public email addresses.
    """

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    emails = re.findall(pattern, text)

    # Remove duplicates
    emails = sorted(set(emails))

    return emails


def extract_links(html: str, base_url: str) -> List[str]:
    """
    Extract useful internal links from HTML.
    """

    soup = BeautifulSoup(html, "html.parser")

    base_domain = urlparse(base_url).netloc.replace("www.", "")

    useful_links = []

    for a in soup.find_all("a", href=True):

        href = a.get("href")

        if not href:
            continue

        full_url = urljoin(base_url, href)

        parsed = urlparse(full_url)

        # Only HTTP/HTTPS
        if parsed.scheme not in ["http", "https"]:
            continue

        link_domain = parsed.netloc.replace("www.", "")

        # Only same website
        if link_domain != base_domain:
            continue

        path = parsed.path.lower()

        keywords = [
            "about",
            "company",
            "team",
            "contact",
            "pricing",
            "customer",
            "solution",
            "product",
            "leadership",
        ]

        if any(keyword in path for keyword in keywords):

            clean_url = full_url.split("#")[0]

            if clean_url not in useful_links:
                useful_links.append(clean_url)

    return useful_links


def fetch_with_curl(url: str) -> str:
    """
    Fallback downloader.

    Your current Windows/mobile-hotspot network works with
    curl.exe -6, so we use IPv6 when Playwright cannot connect.
    """

    print(f"    CURL fallback: {url}")

    try:

        result = subprocess.run(
            [
                "curl.exe",
                "-6",
                "-L",
                "--compressed",
                "--max-time",
                "30",
                "-A",
                "Mozilla/5.0",
                url,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=40,
        )

        if result.returncode != 0:
            print(
                f"    CURL failed with code {result.returncode}"
            )
            return ""

        html = result.stdout

        if not html:
            return ""

        print(
            f"    CURL success: {len(html):,} characters"
        )

        return html

    except subprocess.TimeoutExpired:
        print("    CURL timeout")
        return ""

    except Exception as e:
        print(f"    CURL error: {e}")
        return ""


def fetch_with_playwright(browser, url: str) -> str:
    """
    Try JavaScript-capable browser first.
    """

    try:

        print(f"    Playwright: {url}")

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"
            )
        )

        page.set_default_timeout(30000)

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000,
        )

        # Give JS applications a short time to render
        page.wait_for_timeout(2000)

        html = page.content()

        page.close()

        if html:
            print(
                f"    Playwright success: {len(html):,} characters"
            )

        return html

    except Exception as e:

        print(
            f"    Playwright failed: {str(e)[:180]}"
        )

        try:
            page.close()
        except Exception:
            pass

        return ""


def scrape_domain(
    domain: str,
    max_pages: int = 8,
) -> Dict:

    base_url = normalize_url(domain)

    print()
    print("=" * 60)
    print(f"Starting crawl: {base_url}")
    print("=" * 60)

    pages = []

    visited = set()

    homepage_html = ""

    browser = None
    playwright = None

    # ---------------------------------------------------------
    # START PLAYWRIGHT
    # ---------------------------------------------------------

    if PLAYWRIGHT_AVAILABLE:

        try:

            playwright = sync_playwright().start()

            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    "--disable-quic",
                    "--disable-http2",
                ],
            )

            print("Playwright browser started.")

        except Exception as e:

            print(
                f"Playwright startup failed: {e}"
            )

            browser = None

    # ---------------------------------------------------------
    # FETCH HOMEPAGE
    # ---------------------------------------------------------

    print()
    print("Fetching homepage...")

    if browser:

        homepage_html = fetch_with_playwright(
            browser,
            base_url
        )

    # ---------------------------------------------------------
    # FALLBACK TO CURL
    # ---------------------------------------------------------

    if not homepage_html:

        print(
            "Playwright could not load homepage."
        )

        print(
            "Trying curl.exe IPv6 fallback..."
        )

        homepage_html = fetch_with_curl(
            base_url
        )

    # ---------------------------------------------------------
    # HOMEPAGE SUCCESS
    # ---------------------------------------------------------

    if homepage_html:

        homepage_text = clean_text(
            homepage_html
        )

        pages.append(
            {
                "url": base_url,
                "text": homepage_text,
            }
        )

        visited.add(base_url)

        print(
            f"Homepage extracted: "
            f"{len(homepage_text):,} characters"
        )

    else:

        print()
        print(
            "WARNING: Homepage could not be loaded."
        )

    # ---------------------------------------------------------
    # DISCOVER LINKS
    # ---------------------------------------------------------

    discovered_links = []

    if homepage_html:

        discovered_links = extract_links(
            homepage_html,
            base_url
        )

    # Add known important paths as fallback
    for path in IMPORTANT_PATHS:

        fallback_url = urljoin(
            base_url,
            path
        )

        if fallback_url not in discovered_links:

            discovered_links.append(
                fallback_url
            )

    # Remove duplicates
    final_links = []

    for link in discovered_links:

        if link not in final_links:

            final_links.append(link)

    # Limit pages
    remaining_slots = max_pages - len(pages)

    final_links = final_links[:remaining_slots]

    print()
    print(
        f"Discovered {len(final_links)} "
        f"additional page(s)."
    )

    # ---------------------------------------------------------
    # VISIT SUBPAGES
    # ---------------------------------------------------------

    for url in final_links:

        if url in visited:
            continue

        print()
        print(f"Visiting: {url}")

        html = ""

        # First Playwright
        if browser:

            html = fetch_with_playwright(
                browser,
                url
            )

        # Curl fallback
        if not html:

            print(
                "    Trying curl fallback..."
            )

            html = fetch_with_curl(
                url
            )

        if not html:

            print(
                f"    SKIPPED: Could not retrieve {url}"
            )

            continue

        text = clean_text(html)

        if len(text) < 50:

            print(
                "    Page contains very little text."
            )

            continue

        pages.append(
            {
                "url": url,
                "text": text,
            }
        )

        visited.add(url)

        print(
            f"    Extracted {len(text):,} characters"
        )

        # Small delay to avoid hammering the site
        time.sleep(0.5)

    # ---------------------------------------------------------
    # CLOSE BROWSER
    # ---------------------------------------------------------

    try:

        if browser:
            browser.close()

        if playwright:
            playwright.stop()

    except Exception:
        pass

    # ---------------------------------------------------------
    # COMBINE CONTENT
    # ---------------------------------------------------------

    combined_text_parts = []

    for page in pages:

        combined_text_parts.append(
            f"\nSOURCE URL: {page['url']}\n"
        )

        combined_text_parts.append(
            page["text"]
        )

    combined_text = "\n".join(
        combined_text_parts
    )

    # Final token limit
    combined_text = combined_text[:50000]

    # ---------------------------------------------------------
    # EMAIL EXTRACTION
    # ---------------------------------------------------------

    emails = extract_emails(
        combined_text
    )

    # ---------------------------------------------------------
    # RESULT
    # ---------------------------------------------------------

    result = {

        "domain": domain,

        "base_url": base_url,

        "pages": pages,

        "page_count": len(pages),

        "combined_text": combined_text,

        "emails": emails,

    }

    print()
    print("=" * 60)
    print(f"Crawl finished: {domain}")
    print(f"Pages crawled: {len(pages)}")
    print(f"Emails found: {len(emails)}")
    print("=" * 60)

    return result