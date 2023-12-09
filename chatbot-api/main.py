from flask import Flask, request

app = Flask("chatbot-api")

askServiceMap = {}

@app.route('/scrape', methods=['POST']) # company_site => generate csv 
def scrape():
  if request.method == 'POST':
    return 'Server Works!'
  
@app.route('/ask') # question => response
def ask():
  company_name = request.args.get("company_name")
  company_site = request.args.get("company_site")
  question = request.args.get("question")
  if company_site not in askServiceMap:
    askServiceMap[company_site] = AskService(company_name, company_site, client)
  
  askService = askServiceMap[company_site]
  return askService.ask_question(question)

app.run(port=1280, debug=True)
