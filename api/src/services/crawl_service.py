import os
import re
import urllib.request
from ast import literal_eval
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import requests
import tiktoken
from bs4 import BeautifulSoup
from src.openai_client import openai_client as client

HTTP_URL_PATTERN = r"^http[s]*://.+"


class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        # Create a list to store the hyperlinks
        self.hyperlinks = []

    # Override the HTMLParser's handle_starttag method to get the hyperlinks
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # If the tag is an anchor tag, and it has a href attribute, add the href attribute to the list of hyperlinks
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])


# Function to get the hyperlinks from a URL
def get_hyperlinks(url):
    # Try to open the URL and read the HTML
    try:
        req = urllib.request.Request(url)
        headers = {
            "authority": "httpbin.org",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            "sec-ch-ua-mobile": "?0",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/92.0.4515.107 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "/;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9",
        }
        for k1, k2 in headers.items():
            req.add_header(k1, k2)
        # Open the URL and read the HTML
        with urllib.request.urlopen(req) as response:
            # If the response is not HTML, return an empty list
            if not response.info().get("Content-Type").startswith("text/html"):
                return []

            # Decode the HTML
            html = response.read().decode("utf-8")
    except Exception as e:
        print(e)
        return []

    # Create the HTML Parser and then Parse the HTML to get hyperlinks
    parser = HyperlinkParser()
    parser.feed(html)

    return parser.hyperlinks


# Function to get the hyperlinks from a URL that are within the same domain
def get_domain_hyperlinks(local_domain, url):
    clean_links = []
    for link in set(get_hyperlinks(url)):
        clean_link = None

        # If the link is a URL, check if it is within the same domain
        if re.search(HTTP_URL_PATTERN, link):
            # Parse the URL and check if the domain is the same
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link

        # If the link is not a URL, check if it is a relative link
        else:
            if link.startswith("/"):
                link = link[1:]
            elif link.startswith("#") or link.startswith("mailto:"):
                continue
            clean_link = "https://" + local_domain + "/" + link

        if clean_link is not None:
            if clean_link.endswith("/"):
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)

    # Return the list of hyperlinks that are within the same domain
    return list(set(clean_links))


def crawl(url):
    # Parse the URL and get the domain
    local_domain = urlparse(url).netloc

    # Create a queue to store the URLs to crawl
    queue = deque([url])

    # Create a set to store the URLs that have already been seen (no duplicates)
    seen = {url}

    # Create a directory to store the text files
    if not os.path.exists("text/"):
        os.mkdir("text/")

    if not os.path.exists("text/" + local_domain + "/"):
        os.mkdir("text/" + local_domain + "/")

    # Create a directory to store the csv files
    if not os.path.exists("data/"):
        os.mkdir("data/")

    # While the queue is not empty, continue crawling
    while queue:
        # Get the next URL from the queue
        url = queue.pop()
        print(url)  # for debugging and to see the progress

        # Save text from the url to a <url>.txt file
        with open(
                "text/"
                + local_domain
                + "/"
                + url[8:].replace("/", "_").replace("?", "_").replace("&", "_")
                + ".txt",
                "w",
                encoding="utf-8",
        ) as f:
            # Get the text from the URL using BeautifulSoup
            soup = BeautifulSoup(requests.get(url).text, "html.parser")

            # Get the text but remove the tags
            text = soup.get_text()

            # If the crawler gets to a page that requires JavaScript, it will stop the crawl
            if "You need to enable JavaScript to run this app." in text:
                print(
                    "Unable to parse page " + url + " due to JavaScript being required"
                )

            # Otherwise, write the text to the file in the text directory
            f.write(text)

        # Get the hyperlinks from the URL and add them to the queue
        for link in get_domain_hyperlinks(local_domain, url):
            if link not in seen:
                queue.append(link)
                seen.add(link)


def remove_newlines(text):
    text = text.str.replace("\n", " ")
    text = text.str.replace("\\n", " ")
    text = text.str.replace("  ", " ")
    text = text.str.replace("  ", " ")
    return text


def create_csv(domain, file_name):
    if not os.path.exists("data/scraped"):
        os.mkdir("data/scraped")
    if not os.path.exists("data/embeddings"):
        os.mkdir("data/embeddings")

    # Create a list to store the text files
    texts = []
    file_count = 0
    # Get all the text files in the text directory
    for file in os.listdir("text/" + domain + "/"):
        file_count += 1
        # Open the file and read the text
        with open("text/" + domain + "/" + file, "r", encoding="utf-8") as f:
            text = f.read()

            # Omit the first 11 lines and the last 4 lines, then replace -, _, and #update with spaces.
            texts.append(
                (
                    file[11:-4]
                    .replace("-", " ")
                    .replace("_", " ")
                    .replace("#update", ""),
                    text,
                )
            )
        if file_count > 100:
            break
    # Create a dataframe from the list of texts
    df = pd.DataFrame(texts, columns=["fname", "text"])

    # Set the text column to be the raw text with the newlines removed
    df["text"] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv("data/scraped/" + file_name + ".csv")
    df.head()

    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv("data/scraped/" + file_name + ".csv", index_col=0)
    df.columns = ["title", "text"]

    # Tokenize the text and save the number of tokens to a new column
    df["n_tokens"] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    max_tokens = 500

    # Function to split the text into chunks of a maximum number of tokens
    def split_into_many(text, max_tokens=max_tokens):
        # Split the text into sentences
        sentences = text.split(". ")

        # Get the number of tokens for each sentence
        n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

        chunks = []
        tokens_so_far = 0
        chunk = []

        # Loop through the sentences and tokens joined together in a tuple
        for sentence, token in zip(sentences, n_tokens):
            # If the number of tokens so far plus the number of tokens in the current sentence is greater
            # than the max number of tokens, then add the chunk to the list of chunks and reset
            # the chunk and tokens so far
            if tokens_so_far + token > max_tokens:
                chunks.append(". ".join(chunk) + ".")
                chunk = []
                tokens_so_far = 0

            # If the number of tokens in the current sentence is greater than the max number of
            # tokens, go to the next sentence
            if token > max_tokens:
                continue

            # Otherwise, add the sentence to the chunk and add the number of tokens to the total
            chunk.append(sentence)
            tokens_so_far += token + 1

        # Add the last chunk to the list of chunks
        if chunk:
            chunks.append(". ".join(chunk) + ".")

        return chunks

    shortened = []

    # Loop through the dataframe
    for row in df.iterrows():
        # If the text is None, go to the next row
        if row[1]["text"] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]["n_tokens"] > max_tokens:
            shortened += split_into_many(row[1]["text"])

        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append(row[1]["text"])

    df = pd.DataFrame(shortened, columns=["text"])
    df["n_tokens"] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    df["embeddings"] = df.text.apply(
        lambda x: client.embeddings.create(input=x, model="text-embedding-ada-002")
        .data[0]
        .embedding
    )
    df.to_csv("data/embeddings/" + file_name + ".csv")

    df = pd.read_csv("data/embeddings/" + file_name + ".csv", index_col=0)
    df["embeddings"] = df["embeddings"].apply(literal_eval).apply(np.array)

    return df
