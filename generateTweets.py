from openai import OpenAI
import os
# initialize openAI client

client = OpenAI(api_key="...") #swap out with open ai API key


def generate_tweets(transcript):
    prompt = """
    You will take the following tweets and topics, and find a way to incorporate our brand, ..., into these ideas to create a viral and trendy tweet. Provide multiple tweet ideas.
    ... 
    """ #add in details about brand
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": f"{transcript}"},
  ]
)
    tweets = response.choices[0].message.content
    return tweets 



