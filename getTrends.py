import requests
import subprocess
from collections import defaultdict
from bs4 import BeautifulSoup

def get_trends(country):
    url = f'https://trends24.in/{country}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    trends = soup.find_all('div', {'class': 'list-container'})
    recent_trends = []
    for x in range(23):
        recent_trends += trends[x].find_all('span', {'class': 'trend-name'})

    return recent_trends

def format_trends(trends):
    trend_count = defaultdict(int)
    for element in trends:
        trend_link_tag = element.find('a', class_='trend-link')
        trend_name = trend_link_tag.text
        trend_link = trend_link_tag['href']
        trend_name = trend_link_tag.text.strip()
        trend_count[trend_name] += 1
    return sorted(trend_count.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    country = "united-states"
    top_trends = get_trends(country)
    trends = format_trends(top_trends)
    for trend in trends:
        print(trend)

    links = []

    #pipeline test
    # for x in range(5):
    #     trend_link_tag = top_trends[x].find('a', class_='trend-link')
    #     if trend_link_tag:
    #         trend_link = trend_link_tag['href']
    #         links.append(trend_link)


    # concat_links = ','.join(links)

    # result = subprocess.run(["python", "scrape.py", concat_links], capture_output=True, text=True)
    # print(result.stdout)
    


