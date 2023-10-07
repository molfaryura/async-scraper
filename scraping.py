import aiohttp

import asyncio

from bs4 import BeautifulSoup


class ScrapingForEducation:

    def __init__(self, file_name) -> None:
        self.websites = ScrapingForEducation.take_websites_to_scrape(
            file_name=file_name)

    @staticmethod
    async def fetch_data(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                return None

    @staticmethod
    async def extract_population(html):
        soup = BeautifulSoup(html, 'html.parser')
        countries_population = {}

        all_countries = soup.select(".country")

        for country in all_countries:
            country_name = country.find(
                class_='country-name').get_text(strip=True)
            country_population = country.find(class_='country-population')
            if country_population:
                country_population = country_population.get_text(strip=True)
                countries_population[country_name] = country_population

        return countries_population

    @staticmethod
    async def how_much_books(html):

        soup = BeautifulSoup(html, 'html.parser')

        header = soup.find(class_='page-header action').get_text(strip=True)

        books = soup.find(
            class_='form-horizontal').get_text().lstrip().split()[0]

        return header, books

    @staticmethod
    async def find_python_programmer_job_for_entry_level(html):
        jobs_for_entry_level = 0
        soup = BeautifulSoup(html, 'html.parser')

        all_jobs = soup.find_all(class_="media-content")

        for job in all_jobs:
            if 'Entry' in job.text:
                jobs_for_entry_level += 1

        return jobs_for_entry_level

    @staticmethod
    def take_websites_to_scrape(file_name):
        websites = []

        with open(file_name, 'r') as file:
            content = file.readlines()
            for website in content:
                websites.append(website.strip())

        return websites

    @staticmethod
    async def scrape_website(url):
        html = await ScrapingForEducation.fetch_data(url)

        if html:
            if url == 'https://www.scrapethissite.com/pages/simple/':
                countries_population = await ScrapingForEducation.extract_population(html)

                if countries_population:
                    top_1_country_by_population = max(
                        countries_population.items(), key=lambda x: int(x[1]))
                    print(
                        f'{top_1_country_by_population[0]} is the most populated country with {top_1_country_by_population[1]} people')
                else:
                    print(f'From {url}: No population data found on the page.')

            elif url == 'https://realpython.github.io/fake-jobs/':
                jobs_for_entry_level = await ScrapingForEducation.find_python_programmer_job_for_entry_level(html)
                if jobs_for_entry_level:
                    print(
                        f"I can find {jobs_for_entry_level} opportunities for entry-level python developers")
                else:
                    print('Failed to get job data. Please check again.')

            elif 'https://books.toscrape.com/catalogue/category/books/':
                header, books = await ScrapingForEducation.how_much_books(html)
                print(f'{header} section contains {books} books')

            else:
                print(f'Do not have scraping method for {url} yet!')

        else:
            print(f'Failed to fetch data from {url}.')

    async def main(self):

        tasks = [asyncio.create_task(self.scrape_website(url))
                 for url in self.websites]
        await asyncio.gather(*tasks)
