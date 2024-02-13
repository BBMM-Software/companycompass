from flask import Blueprint, request
from ..services.chat_service import AskService

chat = Blueprint("chat", __name__)

askServiceMap = {}


@chat.route("/chat")
def chat_bot():
    company_name = request.args.get("company_name")
    company_site = request.args.get("company_site")
    question = request.args.get("question")
    if company_site not in askServiceMap:
        askServiceMap[company_site] = AskService(company_name, company_site)

    ask_service = askServiceMap[company_site]
    return ask_service.ask_question(question)
