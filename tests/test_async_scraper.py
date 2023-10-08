import aiohttp

import asyncio

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

    timeout = aiohttp.ClientTimeout(total=10)

    tasks = [asyncio.create_task(help_launch_all_websites(url=url, timeout=timeout))
             for url in content]
    await asyncio.gather(*tasks)

    logging.info("Finished test_websites_accessibility")


async def help_launch_all_websites(url, timeout):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, timeout=timeout) as response:
            logging.info(url)
            assert response.status == 200, f"Failed to access {url}"
