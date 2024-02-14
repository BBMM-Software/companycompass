import os
from urllib.parse import urlparse
from src.services.crawl_service import crawl, create_csv

from flask import Blueprint, request
from flask_api import status

script = Blueprint("script", __name__)


def check_true(text: str):
    return text.lower() == "true"


@script.route("/")
def retrieve():
    domain = request.args.get("domain")

    with open("static/" + domain + ".js") as f:
        content = f.read()
        f.close()
    return content, status.HTTP_200_OK


@script.route("/generate")
def generate():
    company_name = request.args.get("company_name")
    company_url = request.args.get("company_url")

    # TODO: detect if the site has been already crawled on and default false, rename crawl to update
    crawl_ = request.args.get("crawl", default=True, type=check_true)

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

    if crawl_:
        crawl(company_url)
        create_csv(domain, domain)

    path_var = "script?domain=" + domain

    src = '<script src="' + os.getenv("API_URL") + path_var + '"></script>'

    return src, status.HTTP_201_CREATED
