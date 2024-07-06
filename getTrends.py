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
    trend_links = {}
    for element in trends:
        trend_link_tag = element.find('a', class_='trend-link')
        trend_name = trend_link_tag.text.strip()
        trend_link = trend_link_tag['href']
        trend_count[trend_name] += 1
        trend_links[trend_name] = trend_link
    return sorted(trend_count.items(), key=lambda x: x[1], reverse=True), trend_links

if __name__ == "__main__":
    country = "united-states"
    number_of_trends = 5
    top_trends = get_trends(country)
    trends, trend_links = format_trends(top_trends)
    trend_links_list = []
    for i in range(number_of_trends):
        trend_links_list.append(trend_links[trends[i][0]])

    trends_joined = ','.join(trend_links_list)
    
    result = subprocess.run(["python", "scrape.py", trends_joined], capture_output=True, text=True)
    print(result.stdout)



