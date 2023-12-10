from flask import Flask, request
from urllib.parse import urlparse
import crawl_service
from openai import OpenAI
from dotenv import load_dotenv
import os
from ask_service import *

app = Flask("chatbot-api")
load_dotenv()

askServiceMap = {}
client = OpenAI(
	api_key=os.getenv('OPEN_AI_KEY'),
)
crawl_service.client = client

@app.route('/scrape', methods=['POST']) # company_site => generate csv 
def scrape():
  url = request.args.get('company_website_url')
  if not url:
    return 'Failed to provide company_website_url query param!'
  domain = urlparse(url).netloc
  print(url, domain)
  crawl_service.crawl(url)
  crawl_service.createCsv(domain, domain)

  return 'Success'
  
@app.route('/ask') # question => response
def ask():
  company_name = request.args.get("company_name")
  company_site = request.args.get("company_site")
  question = request.args.get("question")
  if company_site not in askServiceMap:
    askServiceMap[company_site] = AskService(company_name, company_site, client)
  
  askService = askServiceMap[company_site]
  return askService.ask_question(question)

@app.route('/', methods=['GET'])
def index():
  return 'API OK'

app.run(port=1280, debug=True)
