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
import re
logger = logging.getLogger(__name__)

URL = "https://www.crisilratings.com/en/home/our-business/ratings.html"


class CrisilGet:

    def extract_date_from_outlook(self, outlook_text):
        """
        regex function helper to extract the date from the outlook value
        """
        if outlook_text:
            # Use regular expression to find date string
            match = re.search(
                r'(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b)',
                outlook_text)
            if match:
                return match.group(0)
        return None

    def get_crisil_info(self, company_name: str) -> dict[str, Any]:
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
        with sync_playwright() as play_instance:
            playground = play_instance.chromium.launch(headless=False, slow_mo=300)
            web_page = playground.new_page()
            web_page.goto(URL)
            # searching the search box
            web_page.locator("input.sme_rating_search_input").fill(company_name)
            web_page.wait_for_timeout(1000)

            # checking if any suggestions land up
            suggestions = web_page.locator('.ui-menu-item')
            if suggestions.count() > 0:
                # hitting the first suggestion in case of a suggestions list
                suggestions.first.click()
                logger.info(f"Found some suggestions relating to {company_name}")
                logger.info(f"Hitting the closest suggestion to the {company_name}")
            else:
                # if no suggestions then hitting enter just
                web_page.keyboard.press("Enter")

            try:
                # trying to locate Found 0 results : in case of found we will terminate the scraping further
                # this will take time in case of no results locator is not found

                no_results_found = web_page.locator('.sme-search-results-found')
                if no_results_found and no_results_found.inner_text().__contains__("Found 0 results"):
                    logger.error("Could not find any crisil results for the company name")
                    playground.close()
                    return {}
            except:
                pass

            # locating the company name
            company_name_locator = web_page.locator("h3.crisil-sub-heading")
            company_name = company_name_locator.text_content()
            result_dict = {'company_name': company_name}

            # getting the ratings item list
            items = web_page.query_selector_all('.comp-fs-instrument-container .item')

            crisil_scraped_data = []
            for item in items:
                # iterate over the items
                # instrument category
                instrument_element = item.query_selector('li:has(span:text("Instrument Category")) h4')
                instrument_category_text = instrument_element.inner_text() if instrument_element else None

                # rating category
                ratings_element = item.query_selector('li:has(span:text("Ratings")) h4')
                crisil_ratings_text = ratings_element.inner_text() if ratings_element else None

                # outlook category
                outlook_element = item.query_selector('li:has(span:text("Outlook")) h4')
                outlook_text = outlook_element.inner_text() if outlook_element else None

                # scrapping the outlook date from the outlook using regex
                outlook_date = self.extract_date_from_outlook(outlook_text)

                iteration_dict = {
                    'instrument': instrument_category_text,
                    'rating': crisil_ratings_text,
                    'outlook': outlook_text,
                    'outlook date': outlook_date
                }
                crisil_scraped_data.append(iteration_dict)

            result_dict |= {'ratings': crisil_scraped_data}

            # Click the button
            web_page.click('a.rr-doc-class')

            # Wait for navigation to complete
            web_page.wait_for_load_state('networkidle', timeout=30000)

            # Get the URL after clicking the button
            url_after_click = web_page.url
            result_dict |= {'rationale_url': url_after_click}

            # closing the web browser
            playground.close()

        logger.info(f"Extracted data for {company_name} is : {result_dict}")
        return {"Comapny Name": company_name, "Crisil Data": result_dict}


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
    crisil_get = CrisilGet()
    company_name = input(str)

    logger.info(f"Getting Crisil info for {company_name}")
    res_dict = crisil_get.get_crisil_info(company_name=company_name)
    print("Scraped data we got is: ", res_dict)
    logger.info(f"Crisil scraping completed for {company_name}")
    print("")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name) s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    main()
