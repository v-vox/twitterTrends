from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from generateTweets import generate_tweets
from bs4 import BeautifulSoup
import argparse 
import time

def get_tweets(driver, search_url, tweet_count):
    driver.get(search_url)
    time.sleep(4)  
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(int(tweet_count)):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    # parse with bs
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    tweets = []
    tweet_elements = soup.find_all('article', {'role': 'article'})
    for tweet_element in tweet_elements[:tweet_count]:
        tweet_text = tweet_element.find('div', {'lang': True}).get_text(strip=True)
        tweets.append(tweet_text)

    return tweets

def query_trends(driver, keyword): # using selenium to gataher trend information from custom gpt
    driver.get("https://chatgpt.com/g/g-QPodwH7wK-trends-expert")
    time.sleep(5)  

    chat_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-id='root']"))
    )

    # input prompt
    chat_input.send_keys(f"write a short summary of the current popular trend: {keyword}")
    chat_input.send_keys(Keys.RETURN)

    time.sleep(23)
    response_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-message-author-role='assistant']"))
    )

    # extract output
    response_text = response_element.text
    
    # driver.quit()

    return response_text 
    
def main(links, tweets):

    search_urls = links.split(',')
    tweet_count = tweets #number of tweets per topic

    # initialize selenium
    chrome_options = Options()
    chrome_options.add_argument(r"--user-data-dir=REPLACE_WITH_PATH") #e.g. chrome data directory 
    chrome_options.add_argument(r'--profile-directory=Profile 1') #e.g. insert profile name
    # chrome_options.add_argument("--headless") 

    webdriver_service = ChromeService()
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    
    # get tweets for each search URL
    all_tweets = []

    # get tweets for each search URL
    for search_url in search_urls:
        tweets = get_tweets(driver, search_url.strip(), tweet_count)
        tweets += f"\n trend summary: {query_trends(driver, search_url)} \n" # comment out this line to skip querying trends
        all_tweets.extend(tweets)

    driver.quit()

    # Combine all tweets into a single string
    all_tweets_string = "\n".join(all_tweets)

    # Run generate_tweets on the combined tweets string
    generated_tweet = generate_tweets(all_tweets_string)

    # Print the returned string value
    print(generated_tweet)

    return generated_tweet
