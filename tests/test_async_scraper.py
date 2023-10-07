import aiohttp

import pytest

import logging

from scraping import ScrapingForEducation


@pytest.mark.asyncio
async def test_most_populated_country():
    logging.info("Starting test_most_populated_country")

    scraper = ScrapingForEducation('websites.txt')

    html = await scraper.fetch_data(url='https://www.scrapethissite.com/pages/simple/')

    result = await scraper.extract_population(html)

    logging.info(len(result))

    assert 'China' in result


@pytest.mark.asyncio
async def test_how_much_books():
    logging.info("Starting test_how_much_books")

    scraper = ScrapingForEducation('websites.txt')

    html = await scraper.fetch_data(url='https://books.toscrape.com/catalogue/category/books/autobiography_27/index.html')

    result = await scraper.how_much_books(html)

    logging.info(result)

    assert int(result[1]) >= 0


@pytest.mark.asyncio
async def test_find_python_programmer_job_for_entry_level():
    scraper = ScrapingForEducation('websites.txt')

    html = await scraper.fetch_data(url='https://realpython.github.io/fake-jobs/')

    result = await scraper.find_python_programmer_job_for_entry_level(html)

    logging.info(result)

    assert result >= 0


@pytest.mark.asyncio
async def test_launch_all_websites():
    with open('websites.txt', 'r') as file:
        content = file.readlines()

    for url in content:
        logging.info(f"Testing accessibility of {url}")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200, f"Failed to access {url}"

    logging.info("Finished test_websites_accessibility")
