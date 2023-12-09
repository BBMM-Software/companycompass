from flask import Flask, request

app = Flask("chatbot-api")

@app.route('/scrape', methods=['POST']) # company_site => generate csv 
def scrape():
  if request.method == 'POST':
    return 'Server Works!'
  
@app.route('/ask') # question => response
def ask():
  return 'Hello from Server'

app.run(port=1280, debug=True)
