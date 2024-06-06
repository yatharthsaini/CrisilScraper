"""
Use Python Playwright to scrape data from the Crisil website.
Make sure to verify your requirements.txt file before submitting your code. You can use Python 3.11>= for this coding
challenge.

Ideally your code should work simply by running the main.py file.

This is a sample file to get you started. Feel free to add any other functions, classes, etc. as you see fit.
This coding challenge is designed to test your ability to write python code and your ability to figure things out.
This coding challenge is designed to take 2-4 hours. Account for edge cases, test a few companies, write tests and list
issues.
"""

from playwright.sync_api import sync_playwright
from typing import Any
import logging

logger = logging.getLogger(__name__)

URL = "https://www.crisilratings.com/en/home/our-business/ratings.html"


def get_crisil_info(company_name: str) -> dict[str, Any]:
    """
    :param company_name: The name of the company to search for.

    :return: A dictionary containing the following information about the company:
        - Company Name
        - Company Rating
        - Company Rating Type
        - Company Rating Date
        - Company Rating Outlook
        - Company Rating Rationale URL : URL to the Crisil website where the rating rationale can be found.

    If the company is not found, return an empty dictionary.
    """
    logger.info(f"Getting Crisil info for {company_name}")
    # TODO: Implement me
    # Use Python Playwright to scrape data from the Crisil website.

    return {}


def main():
    """
    Sample Output for the function get_crisil_info("Reliance Jio Infocomm") should look like this:
    {
    "company_name": "Reliance Jio Infocomm",
    "ratings": [{
        "instument": "Long Term",
        "rating": "CRISIL AAA",
        "outlook": "Stable",
        },
        {
        "instument": "Short Term",
        "rating": "CRISIL A1+",
        "outlook": ""
        }
        ],
    "rating_date": "September 11, 2023", # Date can be any format
    }
    """
    get_crisil_info(company_name="Reliance Jio Infocomm")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name) s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    main()
