from flask import Blueprint, request
from src.services.chat_service import ChatService

chat = Blueprint("chat", __name__)

chatServiceMap = {}


@chat.route("/")
def chat_bot():
    company_name = request.args.get("company_name")
    company_site = request.args.get("company_site")
    question = request.args.get("question")
    if company_site not in chatServiceMap:
        chatServiceMap[company_site] = ChatService(company_name, company_site)

    ask_service = chatServiceMap[company_site]
    return ask_service.ask(question)
