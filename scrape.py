from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from generateTweets import generate_tweets
import argparse 
import time


def get_tweets(driver, search_url, tweet_count):
    driver.get(search_url)
    time.sleep(5)  
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(8):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    # parse with bs
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    tweets = []
    tweet_elements = soup.find_all('article', {'role': 'article'})
    for tweet_element in tweet_elements[:tweet_count]:
        tweet_text = tweet_element.find('div', {'lang': True}).get_text(strip=True)
        tweets.append(tweet_text)

    return tweets

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("search_urls", type=str, help="Comma-separated list of search URLs")
    args = parser.parse_args()
    search_urls = args.search_urls.split(',')

    tweet_count = 5 #number of tweets per topic

    # initialize selenium
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    webdriver_service = ChromeService()
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # log in (automate?)
    driver.get('https://x.com/login')
    input(" \n \n log in to Twitter, press Enter to continue... \n \n ")

    # get tweets for each search URL
    for search_url in search_urls:
        tweets = get_tweets(driver, search_url.strip(), tweet_count)
        all_tweets.extend(tweets)

    driver.quit()

    # Combine all tweets into a single string
    all_tweets_string = "\n".join(all_tweets)

    print(all_tweets_string)

    # Run generate_tweets on the combined tweets string
    generated_tweet = generate_tweets(all_tweets_string)

    # Print the returned string value
    print(generated_tweet)
