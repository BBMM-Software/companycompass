from flask import Flask, request
from urllib.parse import urlparse
from gptFunctions import *

app = Flask("chatbot-api")

@app.route('/scrape', methods=['POST']) # company_site => generate csv 
def scrape():
  url = request.args.get('company_website_url')
  if not url:
    return 'Failed to provide company_website_url query param!'
  domain = urlparse(url).netloc
  print(url, domain)
  crawl(url)
  createCsv(domain, domain)

  return 'Success'
  
@app.route('/ask') # question => response
def ask():
  return 'Hello from Server'

app.run(port=1280, debug=True)
