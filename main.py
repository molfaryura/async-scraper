import asyncio

from scraping import ScrapingForEducation

if __name__ == '__main__':
    scraping = ScrapingForEducation('websites.txt')
    asyncio.run(scraping.main())