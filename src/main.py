import argparse
import json
import os
from typing import List

from dotenv import load_dotenv

from .scraper import scrape_domain


load_dotenv()


def main():

    parser = argparse.ArgumentParser(
        description="Autonomous Lead Enrichment Agent"
    )

    parser.add_argument(
        "domains",
        nargs="+",
        help="Company domains to process"
    )

    parser.add_argument(
        "--output",
        default="output.json",
        help="Output JSON file"
    )

    args = parser.parse_args()

    all_results = []

    print()
    print("=" * 60)
    print("AUTONOMOUS LEAD ENRICHMENT AGENT")
    print("=" * 60)

    for domain in args.domains:

        print()
        print(
            f"PROCESSING: {domain}"
        )

        try:

            result = scrape_domain(
                domain,
                max_pages=8
            )

            all_results.append(
                result
            )

        except Exception as e:

            print()
            print(
                f"ERROR processing {domain}: {e}"
            )

            # Important:
            # One failed company must NOT stop
            # the remaining companies.

            all_results.append(
                {
                    "domain": domain,
                    "error": str(e),
                    "page_count": 0,
                    "pages": [],
                    "combined_text": "",
                    "emails": [],
                }
            )

    # ---------------------------------------------------------
    # SAVE OUTPUT
    # ---------------------------------------------------------

    output_data = {
        "companies": all_results
    }

    with open(
        args.output,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output_data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)

    print(
        f"Results saved to: {args.output}"
    )

    print(
        f"Companies processed: "
        f"{len(all_results)}"
    )


if __name__ == "__main__":
    main()