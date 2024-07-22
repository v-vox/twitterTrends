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


# def get_tweets(driver, search_url, tweet_count):
#     driver.get(search_url)
#     time.sleep(5)  
#     body = driver.find_element(By.TAG_NAME, 'body')
#     for _ in range(int(tweet_count)):
#         body.send_keys(Keys.PAGE_DOWN)
#         time.sleep(1)

#     # parse with bs
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     tweets = []
#     tweet_elements = soup.find_all('article', {'role': 'article'})
#     for tweet_element in tweet_elements[:tweet_count]:
#         if tweet_element.find('div', {'lang': True}) is not None:
#             tweet_text = tweet_element.find('div', {'lang': True}).get_text(strip=True)
#             tweets.append(tweet_text)

#     return tweets

def query_trends(driver, keyword):
    driver.get("https://chatgpt.com/g/g-QPodwH7wK-trends-expert")
    time.sleep(5)  

    chat_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-id='root']"))
    )

    # input prompt
    chat_input.send_keys(f'''
    analyze this trend: {keyword} 
     '''
    )
    chat_input.send_keys(Keys.RETURN)

    time.sleep(20)

    chat_input.send_keys(f'''
    #prompt for tweet generation
    ''')
    time.sleep(5)
    chat_input.send_keys(Keys.RETURN)
    chat_input.send_keys(Keys.RETURN)

    time.sleep(20)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-message-author-role='assistant']"))
    )
    response_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-message-author-role='assistant']")

    latest_response_element = response_elements[-1]

    # extract the text from the latest element
    response_text = latest_response_element.text


    return response_text 

def main(links, tweets):

    search_urls = links.split(',')
    tweet_count = tweets #number of tweets per topic

    # initialize selenium
    chrome_options = Options()
    chrome_options.add_argument(r"--chrome dadta directory") #e.g. chrome data directory 
    chrome_options.add_argument(r'--profile-directory=Profile 1') #e.g. insert profile name
    # chrome_options.add_argument("--headless") 

    webdriver_service = ChromeService()
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


    # get tweets for each search URL
    tweets = []

    # get tweets for each search URL
    for search_url in search_urls:
        tweets += query_trends(driver, search_url.strip())
        print(f"finished querying for {search_url}")

    print(tweets)

    driver.quit()

    return tweets
