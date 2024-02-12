import os
from urllib.parse import urlparse
import crawl_service
from ask_service import AskService
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin
from openai import OpenAI

app = Flask("chatbot-api")
load_dotenv()
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

askServiceMap = {}
client = OpenAI(
    api_key=os.getenv("OPEN_AI_KEY"),
)
crawl_service.client = client

def check_true(qp: str):
    return qp.lower() == "true"


@app.route("/ask")  # question => response
@cross_origin()
def ask():
    company_name = request.args.get("company_name")
    company_site = request.args.get("company_site")
    question = request.args.get("question")
    if company_site not in askServiceMap:
        askServiceMap[company_site] = AskService(company_name, company_site, client)

    ask_service = askServiceMap[company_site]
    return ask_service.ask_question(question)


@app.route("/script")
@cross_origin()
def retrieve():
    domain = request.args.get("domain")

    with open("static/" + domain + ".js") as f:
        content = f.read()
        f.close()
    return content, 200


@app.route("/script/generate")
@cross_origin()
def generate():
    company_name = request.args.get("company_name")
    company_url = request.args.get("company_url")

    crawl = request.args.get("crawl", default=False, type=check_true)

    domain = urlparse(company_url).netloc
    file_path = "static/" + domain + ".js"

    company_name_pattern = "^company_name^"
    company_url_pattern = "^company_website_url^"

    with open("static/main.js", "r") as f:
        content = f.read()
        f.close()

    content = content.replace(company_name_pattern, '"' + company_name + '"')
    content = content.replace(company_url_pattern, '"' + company_url + '"')

    new_file = open(file_path, "w+")
    new_file.write(content)
    new_file.close()

    if crawl:
        crawl_service.crawl(company_url)
        crawl_service.createCsv(domain, domain)

    path_var = "script?domain=" + domain

    src = '<script src="' + os.getenv("API_URL") + path_var + '"></script>'

    return src, 201


app.run(port=8080, debug=True)
