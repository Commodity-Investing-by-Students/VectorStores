import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser
from tqdm import tqdm


def get_news():
    url = 'https://tradingeconomics.com/rss/'
    base_url = 'https://tradingeconomics.com'

    page = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'})

    raw_data = page.text
    soup = BeautifulSoup(raw_data, 'html.parser')
    a_tags = soup.find_all('a')
    hrefs = [a.get('href') for a in a_tags]

    rss_feeds = {
        'Countries': [c for c in hrefs if str(c).endswith('/rss')],
        'Indicators': [c for c in hrefs if str(c).startswith('/rss/')],
    }

    fetched_feeds = {}
    for url in tqdm(rss_feeds['Countries']):
        country_name = url.split('/')[-2]
        country_name = ' '.join([w.capitalize() for w in country_name.split('-')])

        page2 = feedparser.parse(base_url + url)

        # iterate through the entries and save the data to a dataframe
        if page2.status == 200:
            df_data = []
            for entry in page2.entries:
                df_data.append({
                    'Title': entry.title,
                    'Link': entry.link,
                    'Published': entry.published,
                    'Summary': entry.summary,
                    'Country': country_name
                })
            fetched_feeds[country_name] = pd.DataFrame(df_data)
        else:
            print(f'Error fetching {country_name} RSS feed. Status code: {page2.status}')

    merged_country_news = pd.concat(list(fetched_feeds.values()))
    old_country_news = pd.read_parquet('country_news.parquet')

    country_news = pd.concat([old_country_news, merged_country_news]).drop_duplicates()

    country_news.to_parquet('country_news.parquet')

    return country_news
